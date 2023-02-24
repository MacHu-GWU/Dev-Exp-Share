# -*- coding: utf-8 -*-
# content of: sfn_pattern_job_poll_2_check_status.py

import json
import hashlib

import boto3
from datetime import datetime

s3_client = boto3.client("s3")
lbd_client = boto3.client("lambda")

bucket = "669508176277-us-east-1-data"
prefix = "projects/aws-stepfunction/patterns/job-poll"


def lambda_handler(event, context):
    print("------ received event ------")
    print(json.dumps(event, indent=4))

    execution_id = event["Execution"]["Id"]
    m = hashlib.md5()
    m.update(execution_id.encode("utf-8"))
    execution_md5 = m.hexdigest()

    response = s3_client.get_object(
        Bucket=bucket,
        Key=f"{prefix}/{execution_md5}/context.json",
    )
    job_start_timestamp = json.loads(response["Body"].read().decode("utf-8"))["job_start_timestamp"]
    if (datetime.utcnow().timestamp() - job_start_timestamp) >= 30:
        raise TimeoutError("job run timed out in 30 seconds!")

    response = s3_client.get_object(
        Bucket=bucket,
        Key=f"{prefix}/{execution_md5}/status.txt",
    )
    status = response["Body"].read().decode("utf-8").strip()
    return {
        "status": status
    }
