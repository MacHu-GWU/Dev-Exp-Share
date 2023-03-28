# -*- coding: utf-8 -*-
# content of: sfn_pattern_job_poll_1_run_job.py

import json
import time
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

    s3_client.put_object(
        Bucket=bucket,
        Key=f"{prefix}/{execution_md5}/context.json",
        Body=json.dumps(
            {
                "job_start_timestamp": datetime.utcnow().timestamp(),
            }
        ),
    )
    lbd_client.invoke(
        FunctionName="sfn_pattern_job_poll_0_job_runner",
        InvocationType="Event",
        Payload=json.dumps({
            "execution_md5": execution_md5,
        }),
    )
    time.sleep(1)
    return {}
