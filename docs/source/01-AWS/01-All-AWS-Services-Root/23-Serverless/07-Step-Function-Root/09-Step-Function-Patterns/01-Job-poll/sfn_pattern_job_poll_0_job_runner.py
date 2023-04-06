# -*- coding: utf-8 -*-
# content of sfn_pattern_job_poll_0_job_runner.py

import time
import json
import boto3

s3_client = boto3.client("s3")
bucket = "669508176277-us-east-1-data"
prefix = "projects/aws-stepfunction/patterns/job-poll"


class Status:
    running = "running"
    failed = "failed"
    succeeded = "succeeded"


def lambda_handler(event, context):
    print("------ received event ------")
    print(json.dumps(event, indent=4))

    execution_md5 = event["execution_md5"]

    s3_client.put_object(
        Bucket=bucket,
        Key=f"{prefix}/{execution_md5}/status.txt",
        Body=Status.running,
    )
    time.sleep(15)
    succeeded_flag = True
    if succeeded_flag:
        s3_client.put_object(
            Bucket=bucket,
            Key=f"{prefix}/{execution_md5}/status.txt",
            Body=Status.succeeded,
        )
        return {}
    else:
        s3_client.put_object(
            Bucket=bucket,
            Key=f"{prefix}/{execution_md5}/status.txt",
            Body=Status.failed,
        )
        raise ValueError("job failed!")

