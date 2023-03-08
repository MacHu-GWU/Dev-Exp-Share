# -*- coding: utf-8 -*-

# third party
from boto_session_manager import BotoSesManager
import cottonformation as cf
from cottonformation.res import s3
from aws_console_url import AWSConsole
from rich import print as rprint


def tag_dict_to_list(tags: dict):
    return [dict(Key=key, Value=value) for key, value in tags.items()]


template = cf.Template()

s3_bucket_artifacts = s3.Bucket(
    "S3BucketArtifacts",
    p_BucketName=cf.Sub(
        "${aws_account_id}-${aws_region}-artifacts",
        data=dict(
            aws_account_id=cf.AWS_ACCOUNT_ID,
            aws_region=cf.AWS_REGION,
        ),
    ),
)
template.add(s3_bucket_artifacts)

s3_bucket_data = s3.Bucket(
    "S3BucketData",
    p_BucketName=cf.Sub(
        "${aws_account_id}-${aws_region}-data",
        data=dict(
            aws_account_id=cf.AWS_ACCOUNT_ID,
            aws_region=cf.AWS_REGION,
        ),
    ),
)
template.add(s3_bucket_data)

tags = dict(
    HumanCreator="Sanhe Hu",
    MachineCreator="awshsh-infra-stackset-admin",
)

# template.batch_tagging(tags=tags)

stack_set_name = "org-infra-common-tier"

aws_profile_admin = "awshsh_infra_us_east_1"
aws_profile_target_account1 = "awshsh_app_dev_us_east_1"

bsm_admin_account = BotoSesManager(profile_name=aws_profile_admin)
bsm_target_account1 = BotoSesManager(profile_name=aws_profile_target_account1)

aws_console = AWSConsole(
    aws_account_id=bsm_admin_account.aws_account_id,
    aws_region=bsm_admin_account.aws_region,
    bsm=bsm_admin_account,
)

# cf_env = cf.Env(bsm=bsm_admin_account)
# template_url, _ = cf_env.upload_template(
#     template=template,
#     bucket=f"{bsm_admin_account.aws_account_id}-{bsm_admin_account.aws_region}-artifacts",
# )

# ------------------------------------------------------------------------------
# create_stack_set
# ------------------------------------------------------------------------------
console_url = aws_console.cloudformation.filter_service_managed_stack_set(
    stack_set_name
)
print(f"preview stack set: {console_url}")
response = bsm_admin_account.cloudformation_client.create_stack_set(
    StackSetName=stack_set_name,
    TemplateBody=template.to_json(),
    PermissionModel="SERVICE_MANAGED",
    AutoDeployment=dict(
        Enabled=True,
        RetainStacksOnAccountRemoval=False,
    ),
    CallAs="DELEGATED_ADMIN",
    Tags=tag_dict_to_list(tags),
)
rprint(response)

# ------------------------------------------------------------------------------
# create_stack_instances
# ------------------------------------------------------------------------------
console_url = aws_console.cloudformation.get_stack_set_instances(
    stack_set_name, is_service_managed=True
)
print(f"preview stack set instances: {console_url}")
response = bsm_admin_account.cloudformation_client.create_stack_instances(
    StackSetName=stack_set_name,
    DeploymentTargets=dict(
        OrganizationalUnitIds=[
            "r-rkp6",
        ]
    ),
    Regions=[
        "us-east-1",
    ],
    CallAs="DELEGATED_ADMIN",
)
rprint(response)

# ------------------------------------------------------------------------------
# update_stack_set
# ------------------------------------------------------------------------------
console_url = aws_console.cloudformation.get_stack_set_info(
    stack_set_name, is_service_managed=True
)
print(f"preview stack set: {console_url}")
response = bsm_admin_account.cloudformation_client.update_stack_set(
    StackSetName=stack_set_name,
    TemplateBody=template.to_json(),
    PermissionModel="SERVICE_MANAGED",
    CallAs="DELEGATED_ADMIN",
    Tags=tag_dict_to_list(tags),
)
rprint(response)

# ------------------------------------------------------------------------------
# update_stack_instances
# ------------------------------------------------------------------------------
response = bsm_admin_account.cloudformation_client.update_stack_instances(
    StackSetName=stack_set_name,
    DeploymentTargets=dict(
        OrganizationalUnitIds=[
            "r-rkp6",
        ]
    ),
    Regions=[
        "us-east-1",
    ],
    CallAs="DELEGATED_ADMIN",
)
rprint(response)
