# -*- coding: utf-8 -*-

import boto3
import json
import random
import smart_open
from s3pathlib import S3Path, context

boto_ses = boto3.session.Session()
s3_client = boto_ses.client("s3")
bucket = "aws-data-lab-sanhe-for-everything"
prefix = "poc/2022-01-21-smart_open"

p = S3Path(bucket, prefix, "big_compressed_json_file.gz")
with smart_open.open(
    p.uri,
    "w",
    compression=".gz",
    transport_params={"client": s3_client},
) as f:
    print(f"write to {p.console_url}")
    n_row = 1_000
    for i in range(1, 1 + n_row):
        dct = {"id": i, "value": "<div>Hello World!</div>" * 100}
        line = json.dumps(dct) + "\n"
        f.write(line)
