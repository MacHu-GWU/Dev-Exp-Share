# -*- coding: utf-8 -*-

import json
import boto3
import uuid
import random
from pprint import pprint
from datetime import datetime

boto_ses = boto3.session.Session(profile_name="eq_sanhe", region_name="us-east-1")
kinesis_client = boto_ses.client("kinesis")

def kinesis_dump(dct: dict) -> bool:
    return json.dumps(dct).encode("utf-8")

def kinesis_load(data: bool) -> dict:
    return json.loads(data.decode("utf-8"))

stream_name = "sanhe-input"
event_type_list = ["sign-in", "sign-up", "sign-out"]

def put_data():
    n_event = 10
    events = [
        {
            "id": str(uuid.uuid4()),
            "type": random.choice(event_type_list),
            "time": str(datetime.now()),
        }
        for _ in range(n_event)
    ]

    res = kinesis_client.put_records(
        StreamName=stream_name,
        Records=[
            {
                "Data": kinesis_dump(event),
                "PartitionKey": event["id"],
            }
            for event in events
        ]
    )
    print(res)

# put_data()


def get_data():
    res = kinesis_client.get_records(
        StreamName=stream_name,
        Limit=5
    )
    events = [
        kinesis_load(record["Data"])
        for record in res["Records"]
    ]
    print(events)


# get_data()


res = kinesis_client.describe_stream(
    StreamName=stream_name
)
pprint(res)