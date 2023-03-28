# -*- coding: utf-8 -*-

"""
这里我们实现了一个自动化工具, 可以创建用 CloudFormation StackSets 管理多个 AWS Accounts
所需要的 IAM Permission. 这里我们用的 Self Managed Advanced Mode 的模式, 也就是
Admin Role 和 Execution Role 都有多个, 是多对多的关系. 这种方式最复杂, 但也是最灵活的.

注意: 一个 Account 不能即是 Admin Account 又是 Target Account, 这样在 trusted entities
里面会出现冲突.

Reference:

- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html#stacksets-prereqs-advanced-perms
"""

# standard library
import typing as T
import dataclasses

# third party
from boto_session_manager import BotoSesManager
import cottonformation as cf
from cottonformation.res import iam
from boltons.strutils import under2camel
from rich import print as rprint


# ------------------------------------------------------------------------------
# Abstract data model for admin IAM role and execution IAM role.
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class AdminRole:
    aws_account_id: str = dataclasses.field()
    role_name: str = dataclasses.field()

    @property
    def key(self) -> str:
        return f"{self.aws_account_id}-{self.role_name}"


@dataclasses.dataclass
class ExecutionRole:
    aws_account_id: str = dataclasses.field()
    role_name: str = dataclasses.field()
    policy_document: dict = dataclasses.field()

    @property
    def key(self) -> str:
        return f"{self.aws_account_id}-{self.role_name}"


def preprocess(
    associations: T.List[T.Tuple[AdminRole, ExecutionRole]],
) -> T.Dict[str, T.List[cf.Resource]]:
    """
    Based on the given association relationship between admin role and execution role,
    create the CloudFormation resources declaration and group them by account.
    """
    # --------------------------------------------------------------------------
    # based on the given association relationship, extract the many to many
    # relationship.
    # --------------------------------------------------------------------------
    admin_role_mapper: T.Dict[str, AdminRole] = {}
    exec_role_mapper: T.Dict[str, ExecutionRole] = {}
    admin_to_exec_mapper: T.Dict[str, T.List[str]] = {}
    exec_to_admin_mapper: T.Dict[str, T.List[str]] = {}
    per_account_resources_mapper: T.Dict[str, T.List[cf.Resource]] = {}

    for admin_role, exec_role in associations:
        admin_role_mapper.setdefault(admin_role.key, admin_role)
        exec_role_mapper.setdefault(exec_role.key, exec_role)
        try:
            admin_to_exec_mapper[admin_role.key].append(exec_role.key)
        except KeyError:
            admin_to_exec_mapper[admin_role.key] = [exec_role.key]

        try:
            exec_to_admin_mapper[exec_role.key].append(admin_role.key)
        except KeyError:
            exec_to_admin_mapper[exec_role.key] = [admin_role.key]

    def add_resource(
        per_account_resources_mapper: T.Dict[str, list],
        aws_account_id: str,
        resource: cf.Resource,
    ):
        """
        We need to group the resources by AWS Account ID, so that we can deploy
        one CloudFormation stack per AWS Account. Because we only deploy
        IAM roles, which is a global resource, one CFT stack per account is OK.
        """
        try:
            per_account_resources_mapper[aws_account_id].append(resource)
        except KeyError:
            per_account_resources_mapper[aws_account_id] = [resource]

    # --------------------------------------------------------------------------
    # For each admin account, create the CloudFormation declaration
    # --------------------------------------------------------------------------
    for admin_role_key, exec_role_key_list in admin_to_exec_mapper.items():
        if len(exec_role_key_list) != len(set(exec_role_key_list)):
            raise ValueError(
                f"Found duplicate execution role in the Admin Role {admin_role_key!r} "
                f"associated execution role list."
            )

        admin_role = admin_role_mapper[admin_role_key]
        iam_role_admin = iam.Role(
            f"IamRole{under2camel(admin_role.role_name)}",
            p_RoleName=admin_role.role_name,
            rp_AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": [
                                "cloudformation.amazonaws.com",
                            ]
                        },
                        "Action": "sts:AssumeRole",
                    }
                ],
            },
        )
        add_resource(
            per_account_resources_mapper=per_account_resources_mapper,
            aws_account_id=admin_role.aws_account_id,
            resource=iam_role_admin,
        )

        iam_inline_policy_admin = iam.Policy(
            f"IamRole{under2camel(admin_role.role_name)}InlinePolicy",
            rp_PolicyName=admin_role.role_name,
            rp_PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": ["sts:AssumeRole"],
                        "Resource": [
                            (
                                f"arn:aws:iam::{exec_role_mapper[exec_role_key].aws_account_id}:role"
                                f"/{exec_role_mapper[exec_role_key].role_name}"
                            )
                            for exec_role_key in exec_role_key_list
                        ],
                        "Effect": "Allow",
                    }
                ],
            },
            p_Roles=[
                admin_role.role_name,
            ],
            ra_DependsOn=iam_role_admin,
        )
        add_resource(
            per_account_resources_mapper=per_account_resources_mapper,
            aws_account_id=admin_role.aws_account_id,
            resource=iam_inline_policy_admin,
        )

    # --------------------------------------------------------------------------
    # For each target account, create the CloudFormation declaration
    # --------------------------------------------------------------------------
    for exec_role_key, admin_role_key_list in exec_to_admin_mapper.items():
        if len(admin_role_key_list) != len(set(admin_role_key_list)):
            raise ValueError(
                f"Found duplicate admin role in the Execution Role {exec_role_key!r} "
                f"associated admin role list."
            )

        exec_role = exec_role_mapper[exec_role_key]
        iam_role_exec = iam.Role(
            f"IamRole{under2camel(exec_role.role_name)}",
            p_RoleName=exec_role.role_name,
            rp_AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": [
                                (
                                    f"arn:aws:iam::{admin_role_mapper[admin_role_key].aws_account_id}:role"
                                    f"/{admin_role_mapper[admin_role_key].role_name}"
                                )
                                for admin_role_key in admin_role_key_list
                            ]
                        },
                        "Action": "sts:AssumeRole",
                    }
                ],
            },
        )
        add_resource(
            per_account_resources_mapper=per_account_resources_mapper,
            aws_account_id=exec_role.aws_account_id,
            resource=iam_role_exec,
        )

        iam_inline_policy_exec = iam.Policy(
            f"IamRole{under2camel(exec_role.role_name)}InLinePolicy",
            rp_PolicyName=exec_role.role_name,
            rp_PolicyDocument=exec_role.policy_document,
            p_Roles=[
                exec_role.role_name,
            ],
            ra_DependsOn=iam_role_exec,
        )
        add_resource(
            per_account_resources_mapper=per_account_resources_mapper,
            aws_account_id=exec_role.aws_account_id,
            resource=iam_inline_policy_exec,
        )
    return per_account_resources_mapper


def deploy(
    stack_name: str,
    bsm_mapper: T.Dict[str, BotoSesManager],
    associations: T.List[T.Tuple[AdminRole, ExecutionRole]],
):
    """
    批量将 self managed stack set 所需的 IAM Role 都部署到各个 AWS Account 中.
    """
    per_account_resources_mapper = preprocess(associations)

    for aws_account_id, resources in per_account_resources_mapper.items():
        bsm = bsm_mapper[aws_account_id]
        template = cf.Template()
        for resource in resources:
            template.add(resource)
        template.batch_tagging(
            tags=dict(CreatedBy="self-managed-stack-set-advanced-setup-script")
        )
        env = cf.Env(bsm=bsm)
        print(f"deploy stack {stack_name!r} to {aws_account_id!r}")
        env.deploy(
            stack_name=stack_name,
            template=template,
            include_named_iam=True,
            skip_prompt=True,
            timeout=120,
            change_set_timeout=120,
        )


def delete(
    stack_name: str,
    bsm_list: T.List[BotoSesManager],
):
    """
    批量将 self managed stack set 所需的 IAM Role 都删除掉. 做这件事之前一定要记得
    先把用这些 role 创建的 StackSet 都删除掉. 不然那些 StackSet 就不好删掉了.
    """
    for bsm in bsm_list:
        print(f"delete stack {stack_name!r} from {bsm.aws_account_id!r}")
        env = cf.Env(bsm=bsm)
        env.delete(
            stack_name=stack_name,
            skip_prompt=True,
            timeout=120,
        )


if __name__ == "__main__":
    # give your stack a name
    stack_name = "self-managed-stack-set-advanced-setup"

    # enumerate your AWS CLI profile for both admin and target accounts
    aws_profile_admin_account1 = "awshsh_infra_us_east_1"
    aws_profile_target_account1 = "awshsh_app_dev_us_east_1"

    # create boto session manager for each account
    bsm_admin_account1 = BotoSesManager(profile_name=aws_profile_admin_account1)
    bsm_target_account1 = BotoSesManager(profile_name=aws_profile_target_account1)

    # you need the bsm in dict view and list view later
    bsm_mapper = {
        bsm_admin_account1.aws_account_id: bsm_admin_account1,
        bsm_target_account1.aws_account_id: bsm_target_account1,
    }
    bsm_list = list(bsm_mapper.values())

    # define the execution role permission policy document
    # in this test, we only create CloudFormation Stack and S3 bucket
    s3_full_access_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Action": ["cloudformation:*", "s3:*"], "Resource": "*"}
        ],
    }

    # enumerate admin account roles
    admin_account_1_role_1 = AdminRole(
        aws_account_id=bsm_admin_account1.aws_account_id,
        role_name="AWSCloudFormationStackSetAdministrationRole1",
    )

    # enumerate execution account roles
    target_account_1_role_1 = ExecutionRole(
        aws_account_id=bsm_target_account1.aws_account_id,
        role_name="AWSCloudFormationStackSetExecutionRole1",
        policy_document=s3_full_access_policy,
    )

    target_account_1_role_2 = ExecutionRole(
        aws_account_id=bsm_target_account1.aws_account_id,
        role_name="AWSCloudFormationStackSetExecutionRole2",
        policy_document=s3_full_access_policy,
    )

    # enumerate the association (relationship),
    # which admin role can assume what execution role?
    associations = [
        (admin_account_1_role_1, target_account_1_role_1),
        (admin_account_1_role_1, target_account_1_role_2),
    ]

    # then deploy
    deploy(
        stack_name=stack_name,
        bsm_mapper=bsm_mapper,
        associations=associations,
    )

    # clean up, please make sure you delete all the stack set first
    # once those roles are deleted, you can't delete those stack set
    # delete(
    #     stack_name=stack_name,
    #     bsm_list=bsm_list,
    # )
