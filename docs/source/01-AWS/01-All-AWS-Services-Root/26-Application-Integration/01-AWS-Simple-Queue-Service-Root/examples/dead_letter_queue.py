# -*- coding: utf-8 -*-

"""

- API Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
"""

import json
import boto3
from sfm.fingerprint import fingerprint


def jprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))


aws_profile = "eq_sanhe"
queue_url = "https://sqs.us-east-1.amazonaws.com/110330507156/test-standard-queue"

boto_ses = boto3.Session(profile_name=aws_profile)
sqs_client = boto_ses.client("sqs")


def send_message():
    message_body = "Hello World!"
    res = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
    )
    return res

# res = send_message()
# jprint(res)


def consume_message():
    """
    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
    """
    res = sqs_client.receive_message(
        QueueUrl=queue_url,
    )
    jprint(res)

consume_message()
