# -*- coding: utf-8 -*-

import subprocess
import json
from datetime import datetime, timezone, timedelta

from s3pathlib import S3Path, context
from pathlib_mate import Path
from boto_session_manager import BotoSesManager
from aws_console_url import AWSConsole
from rich import print as rprint

# ------------------------------------------------------------------------------
# Put your config here
profile_name = "bmt_app_dev_us_east_1"
bsm = BotoSesManager(profile_name=profile_name)
codecommit_repo = "learn_event_bridge-project"
lambda_function_name = "learn_event_bridge"
lambda_function_role = f"arn:aws:iam::{bsm.aws_account_id}:role/lambda-power-user-role"
# ------------------------------------------------------------------------------


bsm = BotoSesManager(profile_name=profile_name)
context.attach_boto_session(bsm.boto_ses)
aws_console = AWSConsole(
    aws_account_id=bsm.aws_account_id, aws_region=bsm.aws_region, bsm=bsm
)

bucket = f"{bsm.aws_account_id}-{bsm.aws_region}-artifacts"
s3dir_root = S3Path(bucket, "projects", "learn_event_bridge").to_dir()
s3path_source_zip = s3dir_root.joinpath("lambda", "source.zip")

dir_here = Path.dir_here(__file__)
path_source_zip = dir_here.joinpath("source.zip")

log_group_name = f"/aws/lambda/{lambda_function_name}"  # cloudwatch log group name


def build_source():
    path_source_zip.remove_if_exists()
    with path_source_zip.parent.temp_cwd():
        args = [
            "zip",
            f"{path_source_zip}",
            f"lambda_function.py",
            "-q",
        ]
        subprocess.run(args, check=True)
    s3path_source_zip.upload_file(path_source_zip, overwrite=True)


def deploy_lambda_function():
    console_url = aws_console.awslambda.get_function(lambda_function_name)
    print(f"preview lambda function: {console_url}")
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/get_function.html
    try:
        bsm.lambda_client.get_function(FunctionName=lambda_function_name)
        exists = True
    except Exception as e:
        if "Function not found" in str(e):
            exists = False
        else:
            raise e

    if exists is False:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html
        bsm.lambda_client.create_function(
            FunctionName=lambda_function_name,
            Description="for aws event bridge testing",
            Runtime="python3.8",
            Code=dict(
                S3Bucket=s3path_source_zip.bucket,
                S3Key=s3path_source_zip.key,
            ),
            Handler="lambda_function.lambda_handler",
            MemorySize=128,
            Timeout=3,
            Role=lambda_function_role,
        )
    else:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/update_function_code.html
        bsm.lambda_client.update_function_code(
            FunctionName=lambda_function_name,
            S3Bucket=s3path_source_zip.bucket,
            S3Key=s3path_source_zip.key,
        )


def deploy_event_rule():
    event_pattern = {
        "source": ["aws.codecommit"],
        "resources": [f"arn:aws:codecommit:us-east-1:{bsm.aws_account_id}:{codecommit_repo}"]
    }
    bsm.eventbridge_client.put_rule(
        Name="string",
        ScheduleExpression="string",
        EventPattern=json.dumps(event_pattern),
        State="ENABLED",
        Tags=[
            {"Key": "string", "Value": "string"},
        ],
    )


def print_lambda_log():
    response = bsm.cloudwatchlogs_client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy="LastEventTime",
        descending=True,
        limit=3,
    )
    logStreams = response.get("logStreams", [])
    if len(logStreams) == 0:
        print("no log stream found")
        return
    log_stream_name = logStreams[0]["logStreamName"]
    print(f"log stream name: {log_stream_name}")

    utcnow = datetime.utcnow().replace(tzinfo=timezone.utc)
    fifteen_minutes_ago = utcnow - timedelta(minutes=15)

    response = bsm.cloudwatchlogs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startTime=int(1000 * fifteen_minutes_ago.timestamp()),
        limit=100,
        startFromHead=True,
    )
    events = response.get("events", [])
    text = "".join([event["message"] for event in events])
    print(text)


# build_source()
# deploy_lambda_function()
# print_lambda_log()