# -*- coding: utf-8 -*-

import boto3
import random
import time
import itertools
import uuid


aws_profile = "eq_sanhe"

ses = boto3.session.Session(profile_name=aws_profile)

# sqs = ses.client("sqs")
sqs = boto3.resource('sqs')

q_url = "https://sqs.us-east-1.amazonaws.com/110330507156/sql-q.fifo"
q = sqs.Queue(q_url)

# attempt_id = str(uuid.uuid4())
attempt_id = "666193e094efa8ee5ea24fcc6ef99ed1"

# try:
#     res = q.receive_messages(
#         MaxNumberOfMessages=1,
#         AttributeNames=["All",],
#         ReceiveRequestAttemptId=attempt_id,
#     )
#     print("--- first time ---")
#     for msg in res:
#         print(msg.message_id)
#         print(msg.body)
#         print(msg.md5_of_body)
#         print(msg.receipt_handle)
#         print(msg.attributes)
#     raise Exception
# except:
#     res = q.receive_messages(
#         MaxNumberOfMessages=1,
#         AttributeNames=["All",],
#         ReceiveRequestAttemptId=attempt_id,
#     )
#     print("--- second time ---")
#     for msg in res:
#         print(msg.message_id)
#         print(msg.body)
#         print(msg.md5_of_body)
#         print(msg.receipt_handle)
#         print(msg.attributes)
#

res = q.receive_messages(
    MaxNumberOfMessages=1,
    AttributeNames=["All", ],
    # ReceiveRequestAttemptId=attempt_id,
)
print("--- first time ---")
for msg in res:
    print(msg.message_id)
    print(msg.body)
    print(msg.md5_of_body)
    print(msg.receipt_handle)
    print(msg.attributes)