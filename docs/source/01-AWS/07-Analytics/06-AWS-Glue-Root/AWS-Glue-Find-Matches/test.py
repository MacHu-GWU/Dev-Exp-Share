# -*- coding: utf-8 -*-

import string
import random
from typing import List, Dict

import attr
from attrs_mate import AttrsClass
from pathlib_mate import Path
import numpy as np
import pandas as pd
import awswrangler as wr
from faker import Faker
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context
from rich import print as rprint


def add_noise_to_text(text: str, n_noise: int):
    """
    Randomly add noise character to string.

    Example::

        >>> add_noise_to_text("1234567890", n_noise=3)
        123d56e890
    """
    length = len(text)
    if n_noise > length:
        raise ValueError
    chars = list(text)
    for _ in range(n_noise):
        chars[random.randint(1, length) - 1] = random.choice(string.ascii_lowercase)
    return "".join(chars)


def add_noise_to_phone(phone: str, n_noise: int):
    """
    Example::

        >>> add_noise_to_phone("111-222-3333", n_noise=1)
        111-222-3353
    """
    chars = list(phone)
    positions = [0, 1, 2, 4, 5, 6, 8, 9, 10]
    for ind in random.sample(positions, n_noise):
        chars[ind] = random.choice(string.digits)
    return "".join(chars)


def rand_phone_number():
    numbers = [str(random.randint(0, 9)) for _ in range(10)]
    return "".join(
        numbers[:3]
        + [
            "-",
        ]
        + numbers[3:6]
        + [
            "-",
        ]
        + numbers[6:]
    )


fake = Faker(locale="en-US")
bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_2")
context.attach_boto_session(boto_ses=bsm.boto_ses)
dir_here = Path.dir_here(__file__)
path_all_csv = Path(dir_here, "all.csv")
path_records_csv = Path(dir_here, "records.csv")
path_labels_csv = Path(dir_here, "labels.csv")
path_tasks_with_labels_csv = Path(dir_here, "tasks_with_labels.csv")
path_tasks_csv = Path(dir_here, "tasks.csv")


@attr.define
class Person(AttrsClass):
    firstname: str = attr.ib()
    lastname: str = attr.ib()
    phone: str = attr.ib()


@attr.define
class TruePerson(AttrsClass):
    id: int = attr.ib()
    firstname_list: str = attr.ib()
    lastname_list: str = attr.ib()
    phone_list: str = attr.ib()

    @classmethod
    def random(cls, id: int) -> "TruePerson":
        firstname = fake.first_name()
        lastname = fake.last_name()
        phone = rand_phone_number()

        firstname_list = [
            firstname,
        ]
        lastname_list = [
            lastname,
        ]
        phone_list = [
            phone,
        ]
        for _ in range(2):
            firstname_list.append(add_noise_to_text(firstname, random.randint(1, 2)))
            lastname_list.append(add_noise_to_text(lastname, random.randint(1, 2)))
            phone_list.append(add_noise_to_phone(phone, random.randint(0, 1)))

        return cls(
            id=id,
            firstname_list=firstname_list,
            lastname_list=lastname_list,
            phone_list=phone_list,
        )

    def to_person(self) -> "Person":
        return Person(
            firstname=random.choice(self.firstname_list),
            lastname=random.choice(self.lastname_list),
            phone=random.choice(self.phone_list),
        )


def s1_generate_dataset():
    # generate ground truth dataset in memory
    n_true_person = 2000
    true_person_list: List[TruePerson] = list()
    for id in range(1, 1 + n_true_person):
        tp = TruePerson.random(id=id)
        true_person_list.append(tp)

    rows: List[dict] = list()
    for tc in true_person_list:
        n_occurrence = random.randint(2, 10)
        for _ in range(n_occurrence):
            row = tc.to_person().to_dict()
            row["tid"] = f"tid-{tc.id}"
            row["n_occur"] = n_occurrence
            rows.append(row)

    df_all = pd.DataFrame(rows)
    df_all["id"] = [f"id-{ind + 1}" for ind in df_all.index]
    df_all = df_all["id,tid,firstname,lastname,phone".split(",")]
    df_all.to_csv(path_all_csv, sep=",", index=False)

    n_person = df_all.shape[0]
    print(f"total rows = {n_person}")

    # df_all = df_all.loc[shuffled_indices, :]

    # Create records.csv
    df_records = df_all.loc[df_all.index, :]
    del df_records["tid"]
    df_records.to_csv(path_records_csv, sep=",", index=False)

    # Create labels.csv
    df_labels = df_all.loc[df_all.index, :]
    counters = dict()
    col_label = list()
    for tid in df_labels["tid"]:
        if tid in counters:
            counters[tid] += 1
            col_label.append(f"lb-{str(counters[tid])}")
        else:
            col_label.append("lb-1")
            counters[tid] = 0

    df_labels["label"] = col_label
    df_labels = df_labels.rename(columns={"tid": "labeling_set_id"})
    df_labels = df_labels["labeling_set_id,label,id,firstname,lastname,phone".split(",")]
    df_labels.to_csv(path_labels_csv, sep=",", index=False)

    # Create tasks.csv
    rows = list()
    for tc in true_person_list:
        if random.randint(1, 100) <= 70:
            row = tc.to_person().to_dict()
            row["tid"] = f"tid-{tc.id}"
            row["n_occur"] = 1

    for tid, _ in enumerate(
        range(n_person, n_person + int(n_true_person * 0.3)),
        start=n_true_person + 1
    ):
        tc = TruePerson.random(id=tid)
        row = tc.to_person().to_dict()
        row["tid"] = f"tid-{tc.id}"
        row["n_occur"] = 1
        rows.append(row)

    df_tasks_with_labels = pd.DataFrame(rows)
    df_tasks_with_labels["id"] = [f"id-{id}" for id in range(n_person + 1, n_person + 1 + len(rows))]
    df_tasks_with_labels = df_tasks_with_labels["id,tid,firstname,lastname,phone,n_occur".split(",")]
    df_tasks_with_labels.to_csv(path_tasks_with_labels_csv, sep=",", index=False)

    df_tasks = df_tasks_with_labels["id,firstname,lastname,phone".split(",")]
    df_tasks.to_csv(path_tasks_csv, sep=",", index=False)

    # Create glue catalog database / tables
    db_name = "learn_glue_find_matches"
    tb_name_records = "records"
    tb_name_labels = "labels"
    tb_name_tasks = "tasks"

    databases = wr.catalog.databases(boto3_session=bsm.boto_ses)
    if db_name not in databases["Database"].to_list():
        print(f"create database {db_name}")
        wr.catalog.create_database(db_name)

    s3path_prefix = S3Path.from_s3_uri(
        "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-05-18-glue-find-matches/find-matches/"
    )
    s3path_records = S3Path(s3path_prefix, "records")
    s3path_labels = S3Path(s3path_prefix, "labels")
    s3path_tasks = S3Path(s3path_prefix, "tasks")

    s3path_prefix.delete_if_exists()
    tables = wr.catalog.tables(database=db_name, boto3_session=bsm.boto_ses)

    # if tb_name_records not in tables["Table"].to_list():
    wr.s3.to_csv(
        df=df_records,
        path=s3path_records.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_records,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )

    # if tb_name_labels not in tables["Table"].to_list():
    wr.s3.to_csv(
        df=df_labels,
        path=s3path_labels.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_labels,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )

    wr.s3.to_csv(
        df=df_tasks,
        path=s3path_tasks.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_tasks,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )


def s0_download_sample_data_from_aws_doc():
    """
    Ref:

    - Tutorial: Creating a Machine Learning Transform with AWS Glue: https://docs.aws.amazon.com/glue/latest/dg/machine-learning-transform-tutorial.html
    """
    s3path_data = S3Path.from_s3_uri(
        "s3://ml-transforms-public-datasets-us-east-1/dblp-acm/records/dblp_acm_records.csv"
    )
    s3path_label = S3Path.from_s3_uri(
        "s3://ml-transforms-public-datasets-us-east-1/dblp-acm/labels/dblp_acm_labels.csv"
    )

    Path(dir_here, "dblp_acm_records.csv").write_text(s3path_data.read_text())
    Path(dir_here, "dblp_acm_labels.csv").write_text(s3path_label.read_text())


def s2_generate_dataset():
    n_label_set_id = 1000
    n_label_per_set = 20
    n_sample_list = [10, 6, 3, 1]
    assert n_label_per_set == sum(n_sample_list)

    id = 0
    tid = 0
    rows = list()
    for label_set_id in range(1, 1 + n_label_set_id):
        for label, n_sample in enumerate(n_sample_list, start=1):
            tid += 0
            true_person = TruePerson.random(tid)
            for _ in range(n_sample):
                id += 1
                person = true_person.to_person()
                row = dict(
                    labeling_set_id=f"labeling_set_id_{label_set_id}",
                    label=f"label_{label}",
                    id=f"id_{id}",
                    tid=f"tid_{tid}",
                    firstname=person.firstname,
                    lastname=person.lastname,
                    phone=person.phone,
                )
                rows.append(row)

    columns_all = "labeling_set_id,label,id,tid,firstname,lastname,phone".split(",")
    columns_records = "id,firstname,lastname,phone".split(",")
    columns_labels = "labeling_set_id,label,id,firstname,lastname,phone".split(",")
    columns_tasks_with_labels = "labeling_set_id,label,id,tid,firstname,lastname,phone".split(",")
    columns_tasks = "id,firstname,lastname,phone".split(",")

    df = pd.DataFrame(rows, columns=columns_all)

    indices = list(df.index)
    indices_records = random.sample(indices, int(df.shape[0] * 0.7))
    indices_records.sort()
    indices_tasks = list(set(indices).difference(indices_records))
    indices_tasks.sort()

    df_records = df.loc[indices_records, columns_records]
    df_labels = df.loc[indices_records, columns_labels]
    df_tasks_with_labels = df.loc[indices_tasks, columns_tasks_with_labels]
    df_tasks = df.loc[indices_tasks, columns_tasks]

    print(f"df_records has {df_records.shape[0]} rows")
    print(f"df_labels has {df_labels.shape[0]} rows")
    print(f"df_tasks_with_labels has {df_tasks_with_labels.shape[0]} rows")
    print(f"df_tasks has {df_tasks.shape[0]} rows")

    # Dump to local
    df_records.to_csv(path_records_csv, sep=",", index=False)
    df_labels.to_csv(path_labels_csv, sep=",", index=False)
    df_tasks_with_labels.to_csv(path_tasks_with_labels_csv, sep=",", index=False)
    df_tasks.to_csv(path_tasks_csv, sep=",", index=False)

    # Create glue catalog database / tables
    db_name = "learn_glue_find_matches"
    tb_name_records = "records"
    tb_name_labels = "labels"
    tb_name_tasks = "tasks"

    databases = wr.catalog.databases(boto3_session=bsm.boto_ses)
    if db_name not in databases["Database"].to_list():
        print(f"create database {db_name}")
        wr.catalog.create_database(db_name)

    s3path_prefix = S3Path.from_s3_uri(
        "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-05-18-glue-find-matches/find-matches/"
    )
    s3path_records = S3Path(s3path_prefix, "records")
    s3path_labels = S3Path(s3path_prefix, "labels")
    s3path_tasks = S3Path(s3path_prefix, "tasks")

    s3path_prefix.delete_if_exists()
    tables = wr.catalog.tables(database=db_name, boto3_session=bsm.boto_ses)

    # Dump to S3
    print(f"create table {db_name}.{tb_name_records}")
    wr.s3.to_csv(
        df=df_records,
        path=s3path_records.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_records,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )
    s3path = s3path_records.iter_objects().one()
    print(f"preview at {s3path.uri} or {s3path.console_url}")

    print(f"create table {db_name}.{tb_name_labels}")
    wr.s3.to_csv(
        df=df_labels,
        path=s3path_labels.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_labels,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )
    s3path = s3path_labels.iter_objects().one()
    print(f"preview at {s3path.uri} or {s3path.console_url}")

    print(f"create table {db_name}.{tb_name_tasks}")
    wr.s3.to_csv(
        df=df_tasks,
        path=s3path_tasks.uri,
        dataset=True,
        sep=",",
        index=False,
        header=True,
        database=db_name,
        table=tb_name_tasks,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )
    s3path = s3path_tasks.iter_objects().one()
    print(f"preview at {s3path.uri} or {s3path.console_url}")


if __name__ == "__main__":
    # s0_download_sample_data_from_aws_doc()
    # s1_generate_dataset()
    s2_generate_dataset()
    pass
