# -*- coding: utf-8 -*-

import csv
import awswrangler as wr
import pandas as pd
from s3pathlib import S3Path

df = pd.DataFrame([(1, "a"), (2, "b")], columns=["id", "name"])

s3path = S3Path.from_s3_uri("s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-05-18-glue-find-matches/test.csv")

df.to_csv(
    "users.csv",
    index=False,
    header=True,
    quoting=csv.QUOTE_NONNUMERIC,
)
wr.s3.to_csv(
    df,
    path=s3path.uri,
    dataset=True,
    index=False,
    header=True,
    quoting=csv.QUOTE_NONNUMERIC,
)
print(s3path.read_text())
