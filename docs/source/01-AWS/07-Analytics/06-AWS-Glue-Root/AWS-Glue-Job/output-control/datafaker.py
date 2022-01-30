# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime, timezone
from s3pathlib import S3Path


class Config:
    bucket = "aws-data-lab-sanhe-for-everything-us-east-2"
    prefix = "poc/2022-01-25-output-control"
    n_file = 100
    n_record_per_file = 100000


p_root = S3Path(Config.bucket, Config.prefix)
print(p_root.console_url)

start_timestamp = int(datetime(2020, 1, 1, tzinfo=timezone.utc).timestamp())
end_timestamp = int(datetime(2020, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp())


def create_one_file(nth: int):
    p = S3Path(p_root, "events", "{}.json".format(str(nth).zfill(6)))
    print("working on {}".format(p.console_url))
    start_id = 1 + (nth - 1) * Config.n_record_per_file
    end_id = start_id + Config.n_record_per_file
    with p.open("w") as f:
        for id in range(start_id, end_id):
            time = datetime.utcfromtimestamp(
                random.randint(start_timestamp, end_timestamp)
            )
            record = {
                "id": id,
                "time": str(time),
                "date": str(time.date()),
            }
            f.write(json.dumps(record) + "\n")


for nth_file in range(1, Config.n_file + 1):
    create_one_file(nth_file)
    # break
