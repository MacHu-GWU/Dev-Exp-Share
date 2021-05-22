# -*- coding: utf-8 -*-

"""
测试 DeduplicationId 在 FIFO 中作用的原理.

DeduplicationId 只支持 FIFO Queue. 如果一条带有 ``DeduplicationId`` 的消息被成功接收, 那么在 5 分钟内的 deduplication interval  以后收到任何同样 ``DeduplicationId`` 的消息, 都会被成功接收, 但是被直接丢弃. Consumer 不会见到重复的 Message

如果你打开了 Content Based DeduplicationId, 那么 Dedpulication 则会根据 Message Body 自动生成.

- DeduplicationId Reference: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html
- API Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
"""

import boto3
from sfm.fingerprint import fingerprint

aws_profile = "eq_sanhe"
queue_url = "	https://sqs.us-east-1.amazonaws.com/110330507156/test-fifo-queue.fifo"

boto_ses = boto3.Session(profile_name=aws_profile)
sqs_client = boto_ses.client("sqs")


def send_message():
    message_body = "Hello World!"
    res = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
        MessageDeduplicationId=fingerprint.of_text(message_body),
        MessageGroupId="greeting",
    )
    return res


send_message() # will received different sequence number
