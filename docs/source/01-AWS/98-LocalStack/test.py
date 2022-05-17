# -*- coding: utf-8 -*-

from rich import print as rprint
from boto_session_manager import BotoSesManager

endpoint_url = "http://localhost.localstack.cloud:4566"

bsm = BotoSesManager()
s3_client = bsm.boto_ses.client("s3", endpoint_url=endpoint_url)

res = s3_client.list_buckets()
assert len(res["Buckets"]) == 0

s3_client.create_bucket(Bucket="my-bucket")

res = s3_client.list_buckets()
assert len(res["Buckets"]) == 1
