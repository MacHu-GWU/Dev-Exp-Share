# -*- coding: utf-8 -*-

# standard library
import typing as T
import dataclasses

# third party
from boto_session_manager import BotoSesManager
import cottonformation as cf
from cottonformation.res import s3
from rich import print as rprint


template = cf.Template()

s3_bucket = s3.Bucket(
    "S3BucketTest",
    p_BucketName=cf.Sub(
        "${aws_account_id}-${aws_region}-test-bucket",
        data=dict(
            aws_account_id=cf.AWS_ACCOUNT_ID,
            aws_region=cf.AWS_REGION,
        )
    )
)
template.add(s3_bucket)

stack_name = "self-managed-advanced-setup-test"
aws_profile_admin_account1 = "awshsh_app_dev_us_east_1"
aws_profile_target_account1 = "awshsh_ml_dev_us_east_1"
bsm_admin_account1 = BotoSesManager(profile_name=aws_profile_admin_account1)
bsm_target_account1 = BotoSesManager(profile_name=aws_profile_target_account1)


# response = bsm_admin_account1.cloudformation_client.create_stack_set(
#     StackSetName=stack_name,
#     TemplateBody=template.to_json(),
#     AdministrationRoleARN="arn:aws:iam::807388292768:role/AWSCloudFormationStackSetAdministrationRole1",
#     ExecutionRoleName="AWSCloudFormationStackSetExecutionRole1",
#     PermissionModel="SELF_MANAGED",
#     CallAs="SELF",
# )

response = bsm_admin_account1.cloudformation_client.create_stack_instances(
    StackSetName=stack_name,
    Accounts=[
        bsm_target_account1.aws_account_id,
    ],
    Regions=[
        "us-east-1",
    ],
    CallAs="SELF",
)
rprint(response)