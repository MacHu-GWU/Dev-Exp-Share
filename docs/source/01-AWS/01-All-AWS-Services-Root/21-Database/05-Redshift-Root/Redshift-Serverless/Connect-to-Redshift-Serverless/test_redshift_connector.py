# -*- coding: utf-8 -*-

"""
This script introduces how to do CRUD in Python using redshift_connector.

redshift_connector is a low level DB API 2.0 compatible driver for Amazon Redshift.

for more complicate data manipulation, you can use SQLAlchemy + sqlalchemy-redshift,
or awswrangler.
"""

import json
import uuid
import random
import textwrap
import dataclasses
from datetime import datetime
from pathlib import Path

import boto3
import redshift_connector


@dataclasses.dataclass
class DBConn:
    """
    Data model for database connection config file. It should be a json file
    like this::

        {
            "host": "redshift.host.com",
            "port":  5439,
            "database": "database",
            "username": "username",
            "password": "password"
        }
    """

    host: str
    port: int
    database: str
    username: str
    password: str

    @classmethod
    def read_config(cls):
        path_config = Path(__file__).absolute().parent.joinpath("config.json")
        return DBConn(**json.loads(path_config.read_text()))


def create_connect_using_username_password(db_conn: DBConn):
    print("Create connection using username and password")
    conn = redshift_connector.connect(
        host=db_conn.host,
        port=db_conn.port,
        database=db_conn.database,
        user=db_conn.username,
        password=db_conn.password,
    )
    return conn


def create_connect_using_iam(db_conn: DBConn, boto_ses: boto3.session.Session):
    print("Create connection using IAM")
    conn = redshift_connector.connect(
        iam=True,
        database=db_conn.database,
        profile=boto_ses.profile_name,
        is_serverless=True,
        serverless_work_group="sanhe-dev-workgroup",
    )
    # conn = redshift_connector.connect(
    #     iam=True,
    #     host=db_conn.host,
    #     port=db_conn.port,
    #     database=db_conn.database,
    #     db_user="awsuser",
    #     password="",
    #     user="",
    #     access_key_id=credentials.access_key,
    #     secret_access_key=credentials.secret_key,
    #     session_token=credentials.token,
    #     region=boto_ses.region_name,
    # )
    return conn


def test_connection(conn):
    print("Test connection by running a query")
    cursor = conn.cursor()
    sql = f"SELECT {random.randint(1, 100)};"
    row = cursor.execute(sql).fetchone()
    print(row[0])
    print("Success!")


TABLE_NAME = "transactions"


def create_table(conn):
    print(f"Create the {TABLE_NAME!r} table for testing")
    sql = textwrap.dedent(
        f"""
        DROP TABLE IF EXISTS {TABLE_NAME};
        """
    )
    conn.cursor().execute(sql)
    conn.commit()

    sql = textwrap.dedent(
        f"""
        CREATE TABLE {TABLE_NAME}(
            id VARCHAR(36) DISTKEY NOT NULL,
            create_at VARCHAR(26) NOT NULL,
            update_at VARCHAR(26) NOT NULL,
            note VARCHAR
        )
        DISTSTYLE key
        COMPOUND SORTKEY(create_at);
        """
    )
    conn.cursor().execute(sql)
    conn.commit()


def insert_data(conn):
    print(f"Insert some data into {TABLE_NAME!r} table")
    sql = textwrap.dedent(
        f"""
        INSERT INTO {TABLE_NAME} (id, create_at, update_at, note) VALUES (%s, %s, %s, %s)
        """
    )
    rows = list()
    for i in range(1, 1 + 3):
        now = datetime.now().isoformat()
        rows.append((str(uuid.uuid4()), now, now, f"note {i}"))
    conn.cursor().executemany(sql, rows)
    conn.commit()


def select_data(conn):
    print(f"Select data from {TABLE_NAME!r} table")
    sql = textwrap.dedent(
        f"""
        SELECT * FROM {TABLE_NAME} LIMIT 10;
        """
    )
    for row in conn.cursor().execute(sql):
        print(row)


if __name__ == "__main__":
    db_conn = DBConn.read_config()
    aws_profile = "awshsh_app_dev_us_east_1"
    boto_ses = boto3.session.Session()
    credentials = boto_ses.get_credentials()

    # conn = create_connect_using_username_password(db_conn)
    conn = create_connect_using_iam(db_conn, boto_ses)

    test_connection(conn)
    # create_table(conn)
    # insert_data(conn)
    # select_data(conn)
