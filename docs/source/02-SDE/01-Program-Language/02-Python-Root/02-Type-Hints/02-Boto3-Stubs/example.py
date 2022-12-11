# -*- coding: utf-8 -*-

import typing as T
import boto3

if T.TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client

s3_client: "S3Client" = boto3.client("s3")
res = s3_client.head_object(
    Bucket="aws-data-lab-sanhe-for-everything",
    Key="test.txt",
)
print(res)
