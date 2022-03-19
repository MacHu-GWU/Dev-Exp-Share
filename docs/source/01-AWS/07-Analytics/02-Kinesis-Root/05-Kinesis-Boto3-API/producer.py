# -*- coding: utf-8 -*-

import boto3
import json
import random
from rich import print as rprint

boto_ses = boto3.session.Session()
k_client = boto_ses.client("kinesis")

stream_name = "sanhe-dev"

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.put_records
raw_records = [
    {"id": str(i), "value": random.randint(1, 100)}
    for i in range(21, 21+10)
]

kin_records = [
    dict(
        Data=json.dumps(raw_record).encode("utf-8"),
        PartitionKey=raw_record["id"],
    )
    for raw_record in raw_records
]

response = k_client.put_records(
    Records=kin_records,
    StreamName=stream_name,
)

rprint(response)
