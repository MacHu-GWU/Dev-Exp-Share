# -*- coding: utf-8 -*-

"""
This automation scripts can quickly setup a delegated cross AWS Account access
using IAM Role.

Assuming you have a grantee AWS Account and multiple owner AWS Accounts.
The grantee AWS Account has an identity (IAM User or IAM Role) that needs to
assume IAM Role in the owner AWS Accounts to perform some tasks on owner
AWS Accounts.

Please scroll to the bottom (below the ``if __name__ == "__main__":`` section)
to see the example usage.

Pre-requisites:

- Python3.8+
- boto3
- to verify the assume role works, you need ``boto_session_manager>=1.5.2``

Reference:

- attach_group_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/attach_group_policy.html
- attach_user_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/attach_user_policy.html
- attach_role_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/attach_role_policy.html
- detach_group_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/detach_group_policy.html
- detach_user_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/detach_user_policy.html
- detach_role_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/detach_role_policy.html

- get_role: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_role.html
- get_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_policy.html
- create_role: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html
- create_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_policy.html
- delete_role: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/delete_role.html
- delete_policy: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/delete_policy.html
"""

import typing as T
import json
import dataclasses
from datetime import datetime
from functools import cached_property

import boto3


@dataclasses.dataclass
class Base:
    Tags: T.Optional[T.List[T.Dict[str, str]]] = dataclasses.field(default=None)

    @property
    def tags_dict(self) -> T.Dict[str, str]:
        if self.Tags is None:
            return {}
        else:
            return {tag["Key"]: tag["Value"] for tag in self.Tags}


@dataclasses.dataclass
class IamManagedPolicy(Base):
    PolicyName: T.Optional[str] = dataclasses.field(default=None)
    PolicyId: T.Optional[str] = dataclasses.field(default=None)
    Arn: T.Optional[str] = dataclasses.field(default=None)
    Path: T.Optional[str] = dataclasses.field(default=None)
    DefaultVersionId: T.Optional[str] = dataclasses.field(default=None)
    AttachmentCount: T.Optional[int] = dataclasses.field(default=None)
    PermissionsBoundaryUsageCount: T.Optional[int] = dataclasses.field(default=None)
    IsAttachable: T.Optional[bool] = dataclasses.field(default=None)
    Description: T.Optional[str] = dataclasses.field(default=None)
    CreateDate: T.Optional[datetime] = dataclasses.field(default=None)
    UpdateDate: T.Optional[datetime] = dataclasses.field(default=None)

    @classmethod
    def get(cls, iam_client, arn: str) -> T.Optional["IamManagedPolicy"]:
        try:
            return cls(**iam_client.get_policy(PolicyArn=arn)["Policy"])
        except Exception as e:
            if "not found" in str(e):
                return None
            else:  # pragma: no cover
                raise e


@dataclasses.dataclass
class IamRole(Base):
    Path: T.Optional[str] = dataclasses.field(default=None)
    RoleName: T.Optional[str] = dataclasses.field(default=None)
    RoleId: T.Optional[str] = dataclasses.field(default=None)
    Arn: T.Optional[str] = dataclasses.field(default=None)
    CreateDate: T.Optional[datetime] = dataclasses.field(default=None)
    AssumeRolePolicyDocument: T.Optional[str] = dataclasses.field(default=None)
    Description: T.Optional[str] = dataclasses.field(default=None)
    MaxSessionDuration: T.Optional[int] = dataclasses.field(default=None)
    PermissionsBoundary: T.Optional[dict] = dataclasses.field(default=None)
    RoleLastUsed: T.Optional[dict] = dataclasses.field(default=None)

    @classmethod
    def get(cls, iam_client, name: str) -> T.Optional["IamRole"]:
        try:
            return cls(**iam_client.get_role(RoleName=name)["Role"])
        except Exception as e:
            if "cannot be found" in str(e):
                return None
            else:  # pragma: no cover
                raise e


def get_aws_account_id(sts_client) -> str:
    return sts_client.get_caller_identity()["Account"]


def encode_tag(tags: T.Dict[str, str]) -> T.List[T.Dict[str, str]]:
    return [{"Key": k, "Value": v} for k, v in tags.items()]


@dataclasses.dataclass
class Plan:
    """
    :param grantee_boto_ses: the boto3 session of the grantee account
    :param owner_boto_ses_list: list of boto3 sessions of the owner accounts
    :param grantee_identity_arn: the arn of the identity on grantee account
        you want to grant cross account access to
    :param grantee_policy_name: the name of the policy to be created on grantee account
    :param owner_role_name: the name of the role to be created on owner accounts
    :param owner_policy_name: the name of the policy to be created on owner accounts
    :param owner_policy_document_list: list of policy documents to be defined on
        owner accounts' policies. The order of the list must match the order of
        owner_boto_ses_list.
    """

    grantee_boto_ses: boto3.session.Session
    owner_boto_ses_list: T.List[boto3.session.Session]
    grantee_identity_arn: str
    grantee_policy_name: str
    owner_role_name: str
    owner_policy_name: str
    owner_policy_document_list: T.List[dict]
    tags: T.Dict[str, str] = dataclasses.field(
        default_factory=lambda: {
            "meta:created_by": "cross-account-iam-role-access-manager"
        }
    )

    def __post_init__(self):
        if len(owner_boto_ses_list) != len(owner_policy_document_list):
            raise ValueError(
                "owner_boto_ses_list and owner_policy_document_list must have the same length"
            )
        if ":group/" in self.grantee_identity_arn:
            raise ValueError("You cannot use IAM group as grantee identity")

    @cached_property
    def grantee_iam_client(self):
        return self.grantee_boto_ses.client("iam")

    @cached_property
    def owner_iam_client_list(self) -> list:
        return [boto_ses.client("iam") for boto_ses in self.owner_boto_ses_list]

    @cached_property
    def grantee_account_id(self) -> str:
        return get_aws_account_id(self.grantee_boto_ses.client("sts"))

    @cached_property
    def owner_account_id_list(self) -> T.List[str]:
        return [
            get_aws_account_id(boto_ses.client("sts"))
            for boto_ses in self.owner_boto_ses_list
        ]

    @cached_property
    def grantee_policy_arn(self) -> str:
        return (
            f"arn:aws:iam::{self.grantee_account_id}:policy/{self.grantee_policy_name}"
        )

    @cached_property
    def owner_policy_arn_list(self) -> T.List[str]:
        return [
            f"arn:aws:iam::{owner_account_id}:policy/{self.owner_policy_name}"
            for owner_account_id in self.owner_account_id_list
        ]

    @cached_property
    def owner_role_arn_list(self) -> T.List[str]:
        return [
            f"arn:aws:iam::{owner_account_id}:role/{self.owner_role_name}"
            for owner_account_id in self.owner_account_id_list
        ]

    def setup_grantee_account(self):
        print(f"Setup grantee account {self.grantee_account_id}")
        print(
            f"  Create policy {self.grantee_policy_name!r} on "
            f"grantee account {self.grantee_account_id}"
        )
        policy = IamManagedPolicy.get(
            self.grantee_iam_client,
            arn=self.grantee_policy_arn,
        )
        if policy is None:
            policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "sts:AssumeRole",
                        "Resource": [
                            f"arn:aws:iam::{owner_account_id}:role/{self.owner_role_name}"
                            for owner_account_id in self.owner_account_id_list
                        ],
                    },
                ],
            }
            self.grantee_iam_client.create_policy(
                PolicyName=self.grantee_policy_name,
                PolicyDocument=json.dumps(policy_document),
                Tags=encode_tag(self.tags),
            )
            print("    Succeed!")
        else:
            print(
                f"    Grantee account already has the policy {self.grantee_policy_name!r}!"
            )

        print(
            f"  Attach Policy {self.grantee_policy_arn} to {self.grantee_identity_arn}"
        )
        if ":group/" in self.grantee_identity_arn:
            raise ValueError("You cannot use IAM group as grantee identity")
        elif ":user/" in self.grantee_identity_arn:
            self.grantee_iam_client.attach_user_policy(
                UserName=self.grantee_identity_arn.split("/")[-1],
                PolicyArn=self.grantee_policy_arn,
            )
        elif ":role/" in self.grantee_identity_arn:
            self.grantee_iam_client.attach_role_policy(
                RoleName=self.grantee_identity_arn.split("/")[-1],
                PolicyArn=self.grantee_policy_arn,
            )
        elif self.grantee_identity_arn.endswith(":root"):
            # grantee is root aws account, no need to attach anything
            pass
        else:
            raise NotImplementedError
        print("    Done!")

    def setup_one_owner_account(
        self,
        account_id: str,
        iam_client,
        policy_arn: str,
        policy_document: str,
        role_arn: str,
    ):
        print(f"  Setup owner account {account_id}")
        # Create Role
        print(f"    Create role {self.owner_role_name!r} on owner account {account_id}")
        role = IamRole.get(
            iam_client,
            name=self.owner_role_name,
        )
        if role is None:
            trusted_relationship_policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": [
                                self.grantee_identity_arn,
                            ]
                        },
                        "Action": "sts:AssumeRole",
                    },
                ],
            }
            iam_client.create_role(
                RoleName=self.owner_role_name,
                AssumeRolePolicyDocument=json.dumps(
                    trusted_relationship_policy_document
                ),
                Tags=encode_tag(self.tags),
            )
            print("    Succeed!")
        else:
            print(f"      Owner account already has the role {self.owner_role_name!r}!")

        # Create Policy
        print(
            f"    Create policy {self.owner_policy_name!r} on owner account {account_id}"
        )
        policy = IamManagedPolicy.get(
            iam_client,
            arn=policy_arn,
        )
        if policy is None:
            iam_client.create_policy(
                PolicyName=self.owner_policy_name,
                PolicyDocument=json.dumps(policy_document),
                Tags=encode_tag(self.tags),
            )
            print("      Succeed!")
        else:
            print(
                f"      Owner account already has the policy {self.owner_policy_name!r}!"
            )

        # Attach Policy
        print(f"    Attach Policy {policy_arn} to {role_arn}")
        iam_client.attach_role_policy(
            RoleName=self.owner_role_name,
            PolicyArn=policy_arn,
        )
        print("      Done!")

    def setup_owner_account(self):
        print("Setup owner accounts ...")
        for tp in zip(
            self.owner_account_id_list,
            self.owner_iam_client_list,
            self.owner_policy_arn_list,
            self.owner_policy_document_list,
            self.owner_role_arn_list,
        ):
            self.setup_one_owner_account(
                account_id=tp[0],
                iam_client=tp[1],
                policy_arn=tp[2],
                policy_document=tp[3],
                role_arn=tp[4],
            )

    def deploy(self):
        self.setup_grantee_account()
        self.setup_owner_account()

    def cleanup_owner_account(self):
        print("Clean up owner accounts ...")
        for (
            owner_account_id,
            owner_iam_client,
            owner_policy_arn,
            owner_role_arn,
        ) in zip(
            self.owner_account_id_list,
            self.owner_iam_client_list,
            self.owner_policy_arn_list,
            self.owner_role_arn_list,
        ):
            print(f"  Clean up owner account {owner_account_id}")
            role = IamRole.get(owner_iam_client, self.owner_role_name)
            print("    Detach policy from role")
            try:
                if role is not None:
                    owner_iam_client.detach_role_policy(
                        RoleName=self.owner_role_name,
                        PolicyArn=owner_policy_arn,
                    )
            except Exception as e:
                if "was not found" in str(e):
                    pass
                else:
                    raise e

            print(f"    Delete policy {owner_policy_arn}")
            if IamManagedPolicy.get(owner_iam_client, owner_policy_arn) is not None:
                owner_iam_client.delete_policy(PolicyArn=owner_policy_arn)

            print(f"    Delete role {owner_role_arn}")
            if role is not None:
                owner_iam_client.delete_role(RoleName=self.owner_role_name)

    def cleanup_grantee_account(self):
        print(f"Clean up grantee account {self.grantee_account_id} ...")
        print("  Detach policy from grantee identity")
        if ":group/" in self.grantee_identity_arn:
            raise ValueError("You cannot use IAM group as grantee identity")
        elif ":user/" in self.grantee_identity_arn:
            try:
                self.grantee_iam_client.detach_user_policy(
                    UserName=self.grantee_identity_arn.split("/")[-1],
                    PolicyArn=self.grantee_policy_arn,
                )
            except Exception as e:
                if "was not found" in str(e):
                    pass
                else:
                    raise e
        elif ":role/" in self.grantee_identity_arn:
            try:
                self.grantee_iam_client.detach_role_policy(
                    RoleName=self.grantee_identity_arn.split("/")[-1],
                    PolicyArn=self.grantee_policy_arn,
                )
            except Exception as e:
                if "was not found" in str(e):
                    pass
                else:
                    raise e
        elif self.grantee_identity_arn.endswith(":root"):
            # grantee is root aws account, no need to detach anything
            pass
        else:
            raise NotImplementedError

        print(f"  Delete policy {self.grantee_policy_arn}")
        if (
            IamManagedPolicy.get(self.grantee_iam_client, self.grantee_policy_arn)
            is not None
        ):
            self.grantee_iam_client.delete_policy(PolicyArn=self.grantee_policy_arn)

    def delete(self):
        self.cleanup_owner_account()
        self.cleanup_grantee_account()


def verify(plan: Plan):
    from boto_session_manager import BotoSesManager

    print("Verify cross account assume role ...")
    bsm = BotoSesManager(botocore_session=grantee_boto_ses._session)
    res = bsm.sts_client.get_caller_identity()
    grantee_principal_arn = res["Arn"]
    print(
        f"We are on grantee account {bsm.aws_account_id}, "
        f"using principal {grantee_principal_arn}"
    )
    for owner_role_arn in plan.owner_role_arn_list:
        print(f"Try to assume role {owner_role_arn} on owner account")
        bsm_new = bsm.assume_role(role_arn=owner_role_arn)
        res = bsm_new.sts_client.get_caller_identity()
        account_id = res["Account"]
        arn = res["Arn"]
        print(f"  now we are on account {account_id}, using principal {arn}")


if __name__ == "__main__":
    # --------------------------------------------------------------------------
    # update the following variables to your own values
    #  --------------------------------------------------------------------------
    # the boto3 session of the grantee account
    grantee_boto_ses = boto3.session.Session(profile_name="bmt_infra_us_east_1")

    # list of boto3 sessions of the owner accounts
    owner_boto_ses_list = [
        boto3.session.Session(profile_name="bmt_app_dev_us_east_1"),
    ]

    # the arn of the identity on grantee account you want to grant cross account access to
    grantee_account_id = get_aws_account_id(grantee_boto_ses.client("sts"))
    grantee_identity_arn = f"arn:aws:iam::{grantee_account_id}:user/sanhe"

    # the name of the policy to be created on grantee account
    grantee_policy_name = "cross-account-deployer-policy"

    # the name of the role to be created on owner accounts
    owner_role_name = "cross-account-deployer-role"

    # the name of the policy to be created on owner accounts
    owner_policy_name = "cross-account-deployer-policy"

    # list of policy documents to be defined on owner accounts' policies.
    # The order of the list must match the order of owner_boto_ses_list.
    # this example policy allow grantee account to get caller identity
    # so you can verify the assume role works
    owner_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": "sts:GetCallerIdentity",
                "Resource": "*",
            }
        ],
    }
    owner_policy_document_list = [
        owner_policy_document,
    ]
    # --------------------------------------------------------------------------
    # end of configuration
    # --------------------------------------------------------------------------
    plan = Plan(
        grantee_boto_ses=grantee_boto_ses,
        owner_boto_ses_list=owner_boto_ses_list,
        grantee_identity_arn=grantee_identity_arn,
        grantee_policy_name=grantee_policy_name,
        owner_role_name=owner_role_name,
        owner_policy_name=owner_policy_name,
        owner_policy_document_list=owner_policy_document_list,
    )

    plan.deploy() # deploy it
    # plan.delete() # clean up everything
    # verify(plan) # verify the cross account assume role works
