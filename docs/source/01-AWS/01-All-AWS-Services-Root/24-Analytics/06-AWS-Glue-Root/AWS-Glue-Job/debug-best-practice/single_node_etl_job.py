# -*- coding: utf-8 -*-

"""
This script perform the ETL process exactly the same as Glue ETL job.
"""

from datetime import datetime
from pathlib_mate import Path
import pandas as pd
from dateutil.parser import parse as parse_datetime
here = Path(__file__).parent
dir_events = Path(here, "datalake", "events")
dir_events_parquet = Path(here, "datalake", "events_parquet")

def process_one_file(path_in, path_out):
    df = pd.read_json(path_in, orient="records", lines=True)
    df["time"] = df["time"].apply(parse_datetime)
    df["value"] = pd.to_numeric(df["value"], errors="coerce", downcast="integer")
    df = df[df["value"].notna()]
    df["value"] = pd.to_numeric(df["value"], downcast="integer")
    df.to_parquet(path_out)

st = datetime.utcnow()
for p_in in dir_events.select_file():
    print(f"processing {p_in} ...")
    p_out = Path(dir_events_parquet, p_in.fname + ".parquet").abspath
    process_one_file(p_in, p_out)

elapse = (datetime.utcnow() - st).total_seconds()
print(f"elapse {elapse} seconds")