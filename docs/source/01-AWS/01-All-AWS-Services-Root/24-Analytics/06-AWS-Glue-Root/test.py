# -*- coding: utf-8 -*-

"""

"""

import boto3
import awswrangler as wr
import pandas as pd

aws_profile = "eq_sanhe"
aws_region = "us-east-1"
bucket_name = "eq-sanhe-for-everything"

boto3.setup_default_session(profile_name="eq_sanhe", region_name="us-east-1")

# df = pd.DataFrame(
#     [
#         dict(id=1, name="Alice"),
#         dict(id=2, name="Bob"),
#         dict(id=3, name="Cathy"),
#     ],
#     columns="id,name".split(",")
# )


df = pd.DataFrame(
    [
        dict(id=4, name="David2"),
        dict(id=5, name="Edward2"),
        dict(id=6, name="Frank2"),
    ],
    columns="id,name".split(",")
)

wr.s3.to_csv(df=df, path=f"s3://{bucket_name}/data/aws-glue-test/before/test2.csv", index=False)

# df = wr.s3.read_csv(path=f"s3://{bucket_name}/data/aws-glue-test/before/test.csv")
# print(df)