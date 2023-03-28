# -*- coding: utf-8 -*-

"""
This script is a data producer, continuously put data to kinesis data stream.
"""

import json
import random
import time
from datetime import datetime

import boto3
from pathlib_mate import PathCls as Path
from sqlitedict import SqliteDict


class Config:
    aws_profile = "eq_sanhe"
    aws_region = "us-east-1"
    stream_name = "test-shard-iterator-type"


boto_ses = boto3.session.Session(profile_name=Config.aws_profile, region_name=Config.aws_region)
kinesis_client = boto_ses.client("kinesis")
cache = SqliteDict(
    Path(__file__).change(new_basename="cache.sqlite").abspath, autocommit=True)


def kinesis_dump(dct: dict) -> bool:
    return json.dumps(dct).encode("utf-8")


def produce_data():
    n_event_per_put = 100
    n_put_event = 1000000
    event_type_list = ["sign-in", "sign-up", "sign-out"]

    for put_id in range(1, n_put_event + 1):
        start_id = 1 + (put_id - 1) * n_event_per_put
        end_id = put_id * n_event_per_put
        print(f"put {start_id} to {end_id} th record, put_id = {put_id} ...")
        events = list()
        for _id in range(start_id, end_id + 1):
            event = {
                "id": str(_id),
                "type": random.choice(event_type_list),
                "time": str(datetime.now()),
            }
            events.append(event)
        res = kinesis_client.put_records(
            StreamName=Config.stream_name,
            Records=[
                {
                    "Data": kinesis_dump(event),
                    "PartitionKey": event["id"],
                }
                for event in events
            ]
        )
        time.sleep(1)
        # break


if __name__ == "__main__":
    print("Start!")
    produce_data()
