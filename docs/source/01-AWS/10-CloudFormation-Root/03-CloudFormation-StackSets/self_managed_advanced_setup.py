# -*- coding: utf-8 -*-

"""
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
# 这里我们实现了一个自动化工具, 可以创建用 CloudFormation StackSets 管理多个 AWS Accounts
# 所需要的 IAM Permission. 这里我们用的 Self Managed Advanced Mode 的模式, 也就是
# Admin Role 和 Execution Role 都有多个, 是多对多的关系.
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


def prepare(
    stack_name: str,
    bsm_mapper: T.Dict[str, BotoSesManager],
    associations: T.List[T.Tuple[AdminRole, ExecutionRole]],
):
    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    admin_role_mapper: T.Dict[str, AdminRole] = {}
    exec_role_mapper: T.Dict[str, ExecutionRole] = {}
    admin_to_exec_mapper: T.Dict[str, T.List[str]] = {}
    exec_to_admin_mapper: T.Dict[str, T.List[str]] = {}
    per_account_resources_mapper: T.Dict[str, list] = {}

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
        try:
            per_account_resources_mapper[aws_account_id].append(resource)
        except KeyError:
            per_account_resources_mapper[aws_account_id] = [resource]

    # --------------------------------------------------------------------------
    #
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
    #
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

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    for aws_account_id, resources in per_account_resources_mapper.items():
        bsm = bsm_mapper[aws_account_id]
        template = cf.Template()
        for resource in resources:
            template.add(resource)
        # template.batch_tagging(
        #     tags=dict(CreatedBy="self-managed-stack-set-advanced-setup-script")
        # )
        # print("-" * 80)
        # print(aws_account_id)
        # print(template.to_json())
        env = cf.Env(bsm=bsm)
        print(f"deploy to {aws_account_id!r}")
        # env.deploy(
        #     stack_name=stack_name,
        #     template=template,
        #     include_named_iam=True,
        #     skip_prompt=True,
        #     timeout=120,
        #     change_set_timeout=120,
        # )
        env.delete(stack_name=stack_name, skip_prompt=True)


if __name__ == "__main__":
    stack_name = "self-managed-stack-set-advanced-setup"
    aws_profile_admin_account1 = "awshsh_app_dev_us_east_1"
    aws_profile_target_account1 = "awshsh_app_dev_us_east_1"
    aws_profile_target_account2 = "awshsh_ml_dev_us_east_1"
    bsm_admin_account1 = BotoSesManager(profile_name=aws_profile_admin_account1)
    bsm_target_account1 = BotoSesManager(profile_name=aws_profile_target_account1)
    bsm_target_account2 = BotoSesManager(profile_name=aws_profile_target_account2)
    bsm_mapper = {
        bsm_admin_account1.aws_account_id: bsm_admin_account1,
        bsm_target_account1.aws_account_id: bsm_target_account1,
        bsm_target_account2.aws_account_id: bsm_target_account2,
    }
    s3_full_access_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "cloudformation:*",
                    "s3:*",
                ],
                "Resource": "*",
            }
        ],
    }

    admin_account_1_role_1 = AdminRole(
        aws_account_id=bsm_admin_account1.aws_account_id,
        role_name="AWSCloudFormationStackSetAdministrationRole1",
    )

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

    target_account_2_role_1 = ExecutionRole(
        aws_account_id=bsm_target_account2.aws_account_id,
        role_name="AWSCloudFormationStackSetExecutionRole1",
        policy_document=s3_full_access_policy,
    )

    target_account_2_role_2 = ExecutionRole(
        aws_account_id=bsm_target_account2.aws_account_id,
        role_name="AWSCloudFormationStackSetExecutionRole2",
        policy_document=s3_full_access_policy,
    )

    associations = [
        (admin_account_1_role_1, target_account_1_role_1),
        (admin_account_1_role_1, target_account_1_role_2),
        (admin_account_1_role_1, target_account_2_role_1),
        (admin_account_1_role_1, target_account_2_role_2),
    ]

    prepare(
        stack_name=stack_name,
        bsm_mapper=bsm_mapper,
        associations=associations,
    )
