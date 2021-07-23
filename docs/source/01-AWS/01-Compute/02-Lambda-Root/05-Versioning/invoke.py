# -*- coding: utf-8 -*-

import time
import boto3

boto_ses = boto3.session.Session(profile_name="sanhe")
lbd_client = boto_ses.client("lambda")


def invoke():
    response = lbd_client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:663351365541:function:lbd-versioning-poc:latest",
        InvocationType="RequestResponse",
    )


for i in range(100):
    time.sleep(1)
    invoke()
