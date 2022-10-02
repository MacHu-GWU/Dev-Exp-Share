# -*- coding: utf-8 -*-

"""
Augmented AI as Code script. Allow you to quickly spin up required resources
to play with A2I, and then easily clean up all resource with one click.

Prerequisite:

- Create private human workforce:
    - go to https://console.aws.amazon.com/sagemaker/groundtruth?#/labeling-workforces, create a private team
    - invite new workers, validate their email

Ref:

- boto3 Sagemaker: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html
- boto3 a2i: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html
- boto3 iam: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
"""

import json
import boto3
import uuid
from pathlib import Path

dir_here = Path(__file__).parent


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
class Config:
    aws_profile = None
    aws_region = "us-east-1"
    project_name = "a2i_poc"
    hil_output_loc = "s3://aws-data-lab-sanhe-for-everything/2022-02-23-a2i"  # DO NOT end with "/"
    worker_team_arn = "arn:aws:sagemaker:us-east-1:669508176277:workteam/private-crowd/sanhe-labeling-workforce"

    @property
    def project_name_slug(self):
        return self.project_name.replace("_", "-")

    @property
    def a2i_execution_role_name(self):
        return f"{self.project_name}-a2i_execution_role"

    @property
    def a2i_execution_role_arn(self):
        return f"arn:aws:iam::{account_id}:role/{self.a2i_execution_role_name}"

    @property
    def a2i_execution_role_console_url(self):
        return f"https://console.aws.amazon.com/iamv2/home?region={self.aws_region}#/roles/details/{self.a2i_execution_role_name}?section=permissions"

    @property
    def a2i_execution_role_policy_name(self):
        return f"{config.a2i_execution_role_name}-inline-policy"

    @property
    def task_ui_name(self):
        return f"{self.project_name_slug}-task-ui"

    @property
    def task_ui_arn(self):
        return f"arn:aws:sagemaker:{config.aws_region}:{account_id}:human-task-ui/{config.task_ui_name}"

    @property
    def task_ui_console_url(self):
        return f"https://console.aws.amazon.com/a2i/home?region={config.aws_region}#/worker-task-templates/{config.task_ui_name}"

    @property
    def flow_definition_name(self):
        return f"{self.project_name_slug}-flow-def"

    @property
    def flow_definition_arn(self):
        return f"arn:aws:sagemaker:{config.aws_region}:{account_id}:flow-definition/{self.flow_definition_name}"

    @property
    def flow_definition_console_url(self):
        return f"https://console.aws.amazon.com/a2i/home?region={config.aws_region}#/human-review-workflows/{self.flow_definition_name}"

    @property
    def hil_output_uri(self):
        return f"{self.hil_output_loc}/{self.flow_definition_name}"


config = Config()

boto_ses = boto3.session.Session(
    profile_name=config.aws_profile,
    region_name=config.aws_region,
)

sm_client = boto_ses.client("sagemaker")
a2i_client = boto_ses.client("sagemaker-a2i-runtime")
iam_client = boto3.client("iam")
sts_client = boto3.client("sts")

account_id = sts_client.get_caller_identity()["Account"]


class Tag:
    project_name = dict(Key="ProjectName", Value=config.project_name)


def create_a2i_execution_role():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_role
    response = iam_client.create_role(
        RoleName=config.a2i_execution_role_name,
        AssumeRolePolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "sagemaker.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }),
        Tags=[Tag.project_name],
    )

    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_policy
    response = iam_client.put_role_policy(
        RoleName=config.a2i_execution_role_name,
        PolicyName=config.a2i_execution_role_policy_name,
        PolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::*"
                    ]
                }
            ]
        }),
    )

    print(f"Successful created {config.a2i_execution_role_arn}")
    print(f"Preview at {config.a2i_execution_role_console_url}")


def delete_a2i_execution_role():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_policy
    response = iam_client.delete_role_policy(
        RoleName=config.a2i_execution_role_name,
        PolicyName=config.a2i_execution_role_policy_name,
    )

    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role
    response = iam_client.delete_role(
        RoleName=config.a2i_execution_role_name
    )

    print(f"Successful delete {config.a2i_execution_role_arn}")
    print(f"Verify at {config.a2i_execution_role_console_url}")


def create_human_task_ui():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_human_task_ui
    liquid_template = Path(dir_here, "task-backup.liquid").read_text(encoding="utf-8")
    response = sm_client.create_human_task_ui(
        HumanTaskUiName=config.task_ui_name,
        UiTemplate={
            "Content": liquid_template
        },
        Tags=[Tag.project_name, ]
    )

    print(f"Successful created {config.task_ui_arn}")
    print(f"Preview at {config.task_ui_console_url}")


def delete_human_task_ui():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.delete_human_task_ui
    response = sm_client.delete_human_task_ui(
        HumanTaskUiName=config.task_ui_name
    )

    print(f"Successful delete {config.task_ui_arn}")
    print(f"Verify at {config.task_ui_console_url}")


def create_flow_definition():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_flow_definition
    response = sm_client.create_flow_definition(
        FlowDefinitionName=config.flow_definition_name,
        HumanLoopConfig={
            "WorkteamArn": config.worker_team_arn,
            "HumanTaskUiArn": config.task_ui_arn,
            "TaskTitle": config.task_ui_name,
            "TaskDescription": f"{config.task_ui_name} description",
            "TaskCount": 2,
            "TaskTimeLimitInSeconds": 3600,
        },
        OutputConfig={
            "S3OutputPath": config.hil_output_uri,
        },
        RoleArn=config.a2i_execution_role_arn,
        Tags=[Tag.project_name, ],
    )

    print(f"Successful created {config.flow_definition_arn}")
    print(f"Preview at {config.flow_definition_console_url}")


def delete_flow_definition():
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.delete_flow_definition
    response = sm_client.delete_flow_definition(
        FlowDefinitionName=config.flow_definition_name
    )

    print(f"Successful delete {config.flow_definition_arn}")
    print(f"Verify at {config.flow_definition_console_url}")


def start_human_loop():
    input_content = {
        "Pairs": [
            {"row": "Key_0: Value_0", "prediction": 0.1544346809387207},
            {"row": "Key_1: Value_1", "prediction": 0.4938497543334961},
            {"row": "Key_2: Value_2", "prediction": 0.23486430943012238},
            {"row": "Avantor Team 1", "prediction": 0.23486430943012238},
        ]
    }
    response = a2i_client.start_human_loop(
        HumanLoopName=str(uuid.uuid4()),
        FlowDefinitionArn=config.flow_definition_arn,
        HumanLoopInput={
            "InputContent": json.dumps(input_content)
        }
    )


if __name__ == "__main__":
    # create_a2i_execution_role()
    # delete_a2i_execution_role()

    create_human_task_ui()
    delete_human_task_ui()

    # create_flow_definition()
    # delete_flow_definition()

    start_human_loop()
    pass
