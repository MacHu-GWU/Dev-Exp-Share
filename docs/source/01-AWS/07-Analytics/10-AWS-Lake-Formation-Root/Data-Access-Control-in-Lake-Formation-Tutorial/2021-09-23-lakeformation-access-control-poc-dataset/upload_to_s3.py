# -*- coding: utf-8 -*-

import os
import boto3

aws_profile = "aws_data_lab_sanhe"
region_name = "us-east-1"
s3_client = boto3.session.Session(profile_name=aws_profile, region_name=region_name).client("s3")
here = os.path.dirname(os.path.abspath(__file__))


def upload_to_s3():
    for table_name in ["users", "items", "orders"]:
        s3_client.upload_file(
            Filename=os.path.join(here, table_name, "1.json"),
            Bucket="aws-data-lab-sanhe-for-everything",
            Key=f"poc/2021-09-25-lakeformation-access-control-poc-dataset/{table_name}/1.json",
        )


upload_to_s3()
