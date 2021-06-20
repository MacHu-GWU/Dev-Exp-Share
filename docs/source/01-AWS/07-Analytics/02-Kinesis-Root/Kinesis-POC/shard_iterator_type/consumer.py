# -*- coding: utf-8 -*-

import json
import typing
import time
import boto3
from pathlib_mate import PathCls as Path
from sqlitedict import SqliteDict


class IteratorType:
    AT_SEQUENCE_NUMBER = "AT_SEQUENCE_NUMBER"
    AFTER_SEQUENCE_NUMBER = "AFTER_SEQUENCE_NUMBER"
    AT_TIMESTAMP = "AT_TIMESTAMP"
    TRIM_HORIZON = "TRIM_HORIZON"
    LATEST = "LATEST"

class Config:
    aws_profile = "eq_sanhe"
    aws_region = "us-east-1"
    stream_name = "test-shard-iterator-type"
    iterator_type = ""


boto_ses = boto3.session.Session(profile_name=Config.aws_profile, region_name=Config.aws_region)
kinesis_client = boto_ses.client("kinesis")
cache = SqliteDict(
    Path(__file__).change(new_basename="cache.sqlite").abspath, autocommit=True)


def kinesis_dump(dct: dict) -> bool:
    return json.dumps(dct).encode("utf-8")


def kinesis_load(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


event_type_list = ["sign-in", "sign-up", "sign-out"]


def get_shard_id_list() -> typing.List[str]:
    res = kinesis_client.describe_stream(
        StreamName=Config.stream_name
    )
    shard_id_list = [
        dct["ShardId"]
        for dct in res["StreamDescription"]["Shards"]
    ]
    return shard_id_list


shard_id_list = get_shard_id_list()


def process_record_data(file, record):
    file.write("{}\n".format(record["id"]))

def consume_data_long_living():
    shard_id = shard_id_list[0]

    res = kinesis_client.get_shard_iterator(
        StreamName=Config.stream_name,
        ShardId=shard_id,
        ShardIteratorType=IteratorType.TRIM_HORIZON,
    )
    shard_iterator = res["ShardIterator"]

    counter = 0
    with open(Path(__file__).change(new_basename="data.txt").abspath, "a") as f:
        while 1:
            counter += 1
            print(f"--- {counter} th get_records call ---")
            res = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=1000,
            )

            for record in res["Records"]:
                record_data = kinesis_load(record["Data"])
                process_record_data(f, record_data)

            if len(res["Records"]):
                print("from {}".format(kinesis_load(res["Records"][0]["Data"])))
                print("to {}".format(kinesis_load(res["Records"][-1]["Data"])))
            else:
                print("no data")

            shard_iterator = res["NextShardIterator"]

            time.sleep(0.5)


if __name__ == "__main__":
    print("Start Consumer")

    consume_data_long_living()
