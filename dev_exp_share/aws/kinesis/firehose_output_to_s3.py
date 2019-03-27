# -*- coding: utf-8 -*-

"""
reference:

- boto3 Kinesis: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html
"""

import boto3
import json
from dev_exp_share.aws.config import Config

ses = boto3.Session(profile_name=Config.aws_profile)
kinesis = ses.client("kinesis")

stream_name = "learn_aws_kinesis-output-to"

kinesis.create_stream(
    StreamName=,
    ShardCount=,
)

response = client.delete_stream(
    StreamName='string',
    EnforceConsumerDeletion=True|False
)
# import boto3
# import json
#
# ses = boto3.Session(profile_name="identitysandbox.gov")
# kin = ses.client("kinesis")
# stream_name = "sanh-test"
# kin.put_records(
#     Records=[
#         {
#             "Data": json.dumps({"id": 1, "name": "Alice"}).encode("utf-8"),
#             "PartitionKey": "id",
#         },
#     ] * 100,
#     StreamName=stream_name,
# )