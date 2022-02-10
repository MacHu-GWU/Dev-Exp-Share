# -*- coding: utf-8 -*-

"""
This is a simple example shows how to connect Redshift from Python

If your Redshift cluster is on Private Subnet, you can create a Cloud 9 Dev
environment, put it in the same subnet, configure both Cloud 9 Dev EC2 and
Redshift cluster the same ``default`` security gorup,
and run this script from there.

Python dependencies::

    pip install redshift_connector
    pip install psycopg2-binary
    pip install sqlalchemy
    pip install sqlalchemy-redshift

Create a ``config.json`` file like this::

    {
        "cluster_identifier": "my-redshift-cluster-identifier",
        "host": "my-redshift-cluster-identifier.fjyasecmdika.us-east-1.redshift.amazonaws.com",
        "db_user": "awsuser",
        "db_password": "myfakepassword",
        "database": "dev",
        "aws_profile": "my_aws_profile",
        "aws_region": "my_aws_region"
    }
"""

import json
import redshift_connector
import sqlalchemy as sa
from pathlib import Path

path = Path(Path(__file__).parent, "config.json")

with open(path, "r") as f:
    config = json.load(f)

cluster_identifier = config.get("cluster_identifier")
host = config.get("host")
db_user = config.get("db_user")
db_password = config.get("db_password")
database = config.get("database")
aws_profile = config.get("aws_profile")
aws_region = config.get("aws_region")


def method1():
    conn = redshift_connector.connect(
        iam=True,
        database=database,
        db_user=db_user,
        cluster_identifier=cluster_identifier,
        profile=aws_profile,
        region=aws_region,
        user="",
        password="",
        timeout=6,
    )
    cur = conn.cursor()
    for row in cur.execute("SELECT 1;"):
        print(row)


def method2():
    conn = redshift_connector.connect(
        host=host,
        port=5439,
        database=database,
        user=db_user,
        password=db_password,
        timeout=6,
    )

    cur = conn.cursor()
    for row in cur.execute("SELECT 1;"):
        print(row)


def method3():
    conn_str = f"redshift+psycopg2://{db_user}:{db_password}@{host}:5439/{database}"
    engine = sa.create_engine(conn_str)
    with engine.connect() as conn:
        for row in conn.execute("SELECT 1;"):
            print(row)


if __name__ == "__main__":
    method1()
    method2()
    method3()
    pass
