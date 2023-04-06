# -*- coding: utf-8 -*-

from rich import print
import boto3

boto_ses = boto3.session.Session()
s3_client = boto_ses.client("s3")

bucket = "aws-data-lab-sanhe-for-everything"
prefix = "poc/2021-10-25-debug-best-practice-poc-dataset/events_parquet/"
res = s3_client.list_objects(
    Bucket=bucket,
    Prefix=prefix,
)

s3_client.delete_objects(
    Bucket=bucket,
    Delete=dict(
        Objects=[
            dict(Key=record["Key"])
            for record in res["Contents"]
        ],
    ),
)
