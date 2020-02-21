# -*- coding: utf-8 -*-

import json
import random
import time
import uuid
from datetime import datetime

import boto3

aws_profile = "eq_sanhe"
stream_name = "kinesis-practice-web-event"
n_records_per_second = 10
n_records_per_send = 10

boto_ses = boto3.session.Session(profile_name=aws_profile)
kn_client = boto_ses.client("kinesis")

event_name_pool = ["sign_in", ] * 9 + ["sign_up", ] * 1

while True:
    record_data_list = list()
    for _ in range(n_records_per_send):
        sleep_time_base = 1.0 / n_records_per_second
        sleep_time = sleep_time_base * (random.randint(90, 110) / 100.0)
        time.sleep(sleep_time)
        record_data = {
            "event_id": str(uuid.uuid4()),
            "event_name": random.choice(event_name_pool),
            "event_time": str(datetime.utcnow())
        }
        record_data_list.append(record_data)

    records = [
        {
            "Data": (json.dumps(record_data) + "\n").encode("utf-8"),
            "PartitionKey": record_data["event_id"]
        }
        for record_data in record_data_list
    ]
    res = kn_client.put_records(
        Records=records,
        StreamName=stream_name,
    )
    print(records)

    # break
