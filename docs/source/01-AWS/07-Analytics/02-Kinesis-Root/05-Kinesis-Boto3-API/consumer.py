# -*- coding: utf-8 -*-

"""
Ref:

- ``describe_stream``: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.describe_stream
- ``get_shard_iterator``: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.get_shard_iterator
- ``get_records``: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.get_records
"""
import boto3

boto_ses = boto3.session.Session()
k_client = boto_ses.client("kinesis")

stream_name = "sanhe-dev"

response = k_client.describe_stream(
    StreamName=stream_name,
    Limit=100,
)

response = k_client.get_shard_iterator(
    StreamName=stream_name,
)

# response = k_client.get_records(
#     ShardIterator
# )