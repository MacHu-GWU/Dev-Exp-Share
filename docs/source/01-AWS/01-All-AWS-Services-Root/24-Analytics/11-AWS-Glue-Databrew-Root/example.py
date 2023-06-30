# -*- coding: utf-8 -*-

import typing as T
import random
import uuid
from datetime import datetime, timezone

from faker import Faker
import pandas as pd
import awswrangler as wr
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)
fake = Faker()

s3dir_root = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-data/projects/learn_aws_glue_databrew/dev/databases/databrew_example/"
).to_dir()

db_databrew_example = "databrew_example"
t_orders = "orders"
t_customers = "customers"
wr.catalog.create_database(db_databrew_example, exist_ok=True)


def create_data():
    # --------------------------------------------------------------------------
    # Customer
    # --------------------------------------------------------------------------
    s3dir_customers = s3dir_root.joinpath("customers").to_dir()
    s3dir_customers.delete()
    print(f"s3dir_customers: {s3dir_customers.console_url}")
    n_files = 3
    n_records = 100
    df_data_customers = []
    for i in range(1, 1 + n_files):
        df_data = [
            {
                "id": str(uuid.uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "signup_date": fake.date(),
            }
            for _ in range(n_records)
        ]
        df_data_customers.extend(df_data)
        df = pd.DataFrame(df_data)
        s3path = s3dir_customers.joinpath(f"{i}.tsv")
        wr.s3.to_csv(
            df,
            s3path.uri,
            index=False,
            header=True,
            sep=",",
            s3_additional_kwargs=dict(ContentType="text/plain"),
        )

    columns_types, partitions_types = wr.catalog.extract_athena_types(
        df=df,
        file_format="csv",
        index=False,
    )
    wr.catalog.create_csv_table(
        table=t_customers,
        database=db_databrew_example,
        path=s3dir_customers.uri,
        partitions_types=partitions_types,
        columns_types=columns_types,
        skip_header_line_count=1,
        sep=",",
    )


    # --------------------------------------------------------------------------
    # Order
    # --------------------------------------------------------------------------
    categories = [
        "Groceries",
        "Pharmacy",
        "Household",
    ]

    s3dir_orders = s3dir_root.joinpath("orders").to_dir()
    s3dir_orders.delete()
    print(f"s3dir_orders: {s3dir_orders.console_url}")
    n_files = 3
    n_records = 1000
    for i in range(1, 1 + n_files):
        df_data = [
            {
                "order_id": str(uuid.uuid4()),
                "time": None,
                "total": random.randint(1, 100),
                "category": random.choice(categories),
                "customer_id": random.choice(df_data_customers)["id"],
            }
            for _ in range(n_records)
        ]
        df = pd.DataFrame(df_data)
        df["time"] = pd.date_range(
            start="2023-01-01", end="2023-01-31", periods=n_records, unit="s"
        )
        s3path = s3dir_orders.joinpath(f"{i}.tsv")
        wr.s3.to_csv(
            df,
            s3path.uri,
            index=False,
            header=True,
            sep=",",
            s3_additional_kwargs=dict(ContentType="text/plain"),
        )

    columns_types, partitions_types = wr.catalog.extract_athena_types(
        df=df,
        file_format="csv",
        index=False,
    )
    wr.catalog.create_csv_table(
        table=t_orders,
        database=db_databrew_example,
        path=s3dir_orders.uri,
        partitions_types=partitions_types,
        columns_types=columns_types,
        skip_header_line_count=1,
        sep=",",
    )


create_data()
