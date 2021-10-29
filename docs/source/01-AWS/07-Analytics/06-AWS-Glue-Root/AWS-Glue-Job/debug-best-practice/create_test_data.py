# -*- coding: utf-8 -*-

from pathlib_mate import Path
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

here = Path(__file__).parent
dir_events = Path(here, "datalake", "events")

n_file = 10
n_row_per_file = 1000 * 1000

bad_file_index = [2, 6]
bad_row_index = [3, 7]

for ith_file in range(1, 1+n_file):
    print(f"working on {ith_file}.json ...")
    p_json = Path(dir_events, f"{str(ith_file).zfill(3)}.json")
    df = pd.DataFrame(columns=["id", "time", "value"])
    df["id"] = range(1 + (ith_file - 1) * n_row_per_file, 1 + n_row_per_file + (ith_file - 1) * n_row_per_file)
    df["time"] = pd.date_range(
        datetime(2000, 1, 1) + timedelta(days=ith_file - 1),
        datetime(2000, 1, 1) + timedelta(days=1) - timedelta(seconds=1) + timedelta(days=ith_file - 1),
        periods=n_row_per_file,
    )
    df["value"] = np.random.randint(1, 1000000, size=n_row_per_file)
    if ith_file in bad_file_index:
        for row_index in bad_row_index:
            df.loc[row_index-1, "value"] = "invalid"
    df.to_json(p_json.abspath, orient="records", lines=True, date_format="iso")
