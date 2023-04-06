# -*- coding: utf-8 -*-

"""

item,price,time
apple,5.34,2019-01-01 16:34:59
"""

import boto3
import numpy as np
import pandas as pd
from rolex.generator import rnd_datetime_list_high_performance
from s3iotools import S3Dataframe

aws_profile = "skymap_sandbox"
bucket_name = "skymap-sandbox-learn-emr"
n_file = 200
n_rows = 1000

s3 = boto3.session.Session(profile_name=aws_profile).resource("s3")
item_list = ["apple", "banana", "cherry"]

for id in range(1, 1 + n_file):
    print(id)
    key = "data/{id}.csv".format(id=id)
    s3df = S3Dataframe(s3_resource=s3, bucket_name=bucket_name, key=key)
    df = pd.DataFrame()
    df["item"] = np.random.choice(item_list, size=n_rows)
    df["price"] = np.random.randn(n_rows, 1) + 5
    df["time"] = rnd_datetime_list_high_performance(size=n_rows, start="2019-01-01", end="2019-01-01 23:59:59")
    s3df.df = df
    s3df.to_csv()
