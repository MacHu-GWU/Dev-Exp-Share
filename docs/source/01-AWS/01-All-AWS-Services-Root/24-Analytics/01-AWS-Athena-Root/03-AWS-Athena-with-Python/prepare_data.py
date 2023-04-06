# -*- coding: utf-8 -*-

"""

"""

import numpy as np
import pandas as pd
from s3pathlib import S3Path

# define s3 object path
class Config:
    bucket = "aws-data-lab-sanhe-for-everything-us-east-2"
    prefix = "poc/2022-02-04-aws-athena-with-python"

s3path = S3Path(
    Config.bucket,
    Config.prefix,
    "events",
    "data.csv",
)
print(f"preview data at {s3path.console_url}")

# generate dummy data
n_rows = 1000
df = pd.DataFrame()
df["id"] = range(1, n_rows+1)
df["time"] = pd.date_range(start="2000-01-01", end="2000-03-31", periods=n_rows)
df["category"] = np.random.randint(1, 1+3, size=n_rows)
df["value"] = np.random.randint(1, 1+100, size=n_rows)

# write csv to s3
with s3path.open("w") as f:
    df.to_csv(f, index=False)
