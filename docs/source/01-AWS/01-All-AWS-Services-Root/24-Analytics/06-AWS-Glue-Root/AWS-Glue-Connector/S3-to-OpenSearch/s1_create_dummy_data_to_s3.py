# -*- coding: utf-8 -*-

import random
import typing
import pandas as pd
import awswrangler as wr
from faker import Faker
from s3pathlib import S3Path

mappings = {
    "properties": {
        "customer_id": {"type": "long"},
        "customer_firstname": {"type": "keyword"},
        "customer_lastname": {"type": "keyword"},
        "customer_street": {"type": "text"},
        "customer_city": {"type": "keyword"},
        "customer_state": {"type": "keyword"},
        "customer_postcode": {"type": "keyword"},
        "customer_telephone": {"type": "keyword"},
        "customer_dob": {"type": "keyword"},
        "customer_idnumber": {"type": "keyword"},
    }
}

body = {
    "mappings": mappings,
}

bucket: str = "aws-data-lab-sanhe-for-everything-us-east-2"
prefix: str = "poc/2022-01-21-glue-s3-to-opensearch"

start_customer_id: int = 1_000_000_001
n_doc_per_customer_file: int = 1000
n_customer_file: int = 50

start_order_id: int = 1_000_000_000_000
n_doc_per_order_file: int = 10000
n_order_file: int = 100


def gen_customer(fake: Faker, cid: int):
    dct = {
        "customer_id": cid,
        "customer_firstname": fake.first_name().lower(),
        "customer_lastname": fake.last_name().lower(),
        "customer_street": fake.street_address().lower(),
        "customer_city": fake.city().lower(),
        "customer_state": fake.state().lower(),
        "customer_postcode": fake.postcode().lower(),
        "customer_telephone": fake.phone_number().lower(),
        "customer_dob": str(fake.date_of_birth()).lower(),
        "customer_idnumber": fake.ssn().lower(),
    }
    return dct


def gen_order(fake: Faker, oid: int, cid: int):
    dct = {
        "order_id": oid,
        "customer_id": cid,
        "create_time": fake.date_time(),
    }
    return dct


def generate_customer_data(nth_file: int) -> typing.Iterable[dict]:
    start_id = start_customer_id + (nth_file - 1) * n_doc_per_customer_file
    for cid in range(start_id, start_id + n_doc_per_customer_file):
        yield gen_customer(fake=fake, cid=cid)


def generate_order_data(nth_file: int) -> typing.Iterable[dict]:
    max_customer_id = start_customer_id + n_doc_per_customer_file * n_customer_file - 1
    start_id = start_order_id + (nth_file - 1) * n_doc_per_order_file
    for oid in range(start_id, start_id + n_doc_per_order_file):
        cid = random.randint(start_customer_id, max_customer_id)
        yield gen_order(fake=fake, oid=oid, cid=cid)


def create_customer_s3_files():
    for i in range(1, 1 + n_customer_file):
        p = S3Path(bucket, prefix, "customers", "{}.json".format(str(i).zfill(6)))
        data = list(generate_customer_data(i))
        df = pd.DataFrame(data)
        wr.s3.to_json(df, p.uri, orient="records", lines=True)


def create_order_s3_files():
    for i in range(1, 1 + n_order_file):
        p = S3Path(bucket, prefix, "orders", "{}.json".format(str(i).zfill(6)))
        data = list(generate_order_data(i))
        df = pd.DataFrame(data)
        wr.s3.to_json(df, p.uri, orient="records", lines=True)


if __name__ == "__main__":
    fake = Faker()

    # for doc in generate_customer_data(1):
    #     print(doc)

    # for doc in generate_order_data(1):
    #     print(doc)

    create_customer_s3_files()
    create_order_s3_files()

    p = S3Path(bucket, prefix, "/")
    print(f"preview data: {p.console_url}")
    pass
