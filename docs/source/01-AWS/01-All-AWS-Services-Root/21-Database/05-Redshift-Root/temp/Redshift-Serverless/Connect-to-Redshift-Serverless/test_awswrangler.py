# -*- coding: utf-8 -*-

"""
This script introduces how to do CRUD in Python using redshift_connector.

redshift_connector is a low level DB API 2.0 compatible driver for Amazon Redshift.

for more complicate data manipulation, you can use SQLAlchemy + sqlalchemy-redshift,
or awswrangler.
"""

import json
import uuid
import textwrap
import random
import dataclasses
from pathlib import Path
from datetime import datetime

import boto3
import pandas as pd
import redshift_connector
import sqlalchemy as sa
import sqlalchemy.orm as orm
import awswrangler as wr


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

    @property
    def workgroup(self) -> str:
        return self.host.split(".")[0]


def create_connect_using_iam(db_conn: DBConn, boto_ses: boto3.session.Session):
    print("Create connection using IAM")
    credentials = boto_ses.get_credentials()
    conn = redshift_connector.connect(
        iam=True,
        host=db_conn.host,
        port=db_conn.port,
        database=db_conn.database,
        db_user="awsuser",
        password="",
        user="",
        access_key_id=credentials.access_key,
        secret_access_key=credentials.secret_key,
        session_token=credentials.token,
        region=boto_ses.region_name,
    )
    return conn


# Base = orm.declarative_base()
#
#
# class Transaction(Base):
#     __tablename__ = "transactions"
#
#     id: str = sa.Column(sa.String, primary_key=True)
#     create_at: str = sa.Column(sa.String)
#     update_at: str = sa.Column(sa.String)
#     note: str = sa.Column(sa.String, nullable=True)
#
#     @classmethod
#     def new(cls, note: str = None):
#         return cls(
#             id=str(uuid.uuid4()),
#             create_at=datetime.utcnow().isoformat(),
#             update_at=datetime.utcnow().isoformat(),
#             note=note,
#         )
#
#
# def create_engine_using_username_password(db_conn: DBConn):
#     conn_str = (
#         f"redshift+psycopg2://{db_conn.username}:{db_conn.password}"
#         f"@{db_conn.host}:{db_conn.port}/{db_conn.database}"
#     )
#     return sa.create_engine(conn_str)
#
#
# def create_engine_using_iam(db_conn: DBConn, boto_ses: boto3.session.Session):
#     redshift_serverless_client = boto_ses.client("redshift-serverless")
#     res = redshift_serverless_client.get_credentials(
#         dbName="dev",
#         workgroupName="sanhe-dev-workgroup",
#         durationSeconds=900,
#     )
#     username = res["dbUser"]
#     password = res["dbPassword"]
#     username = username.replace(":", "%3A")  # url encode the : character
#     conn_str = (
#         f"redshift+psycopg2://{username}:{password}"
#         f"@{db_conn.host}:{db_conn.port}/{db_conn.database}"
#     )
#     return sa.create_engine(conn_str)
#
#
# def test_connection(conn):
#     print("Test connection by running a query")
#     cursor = conn.cursor()
#     sql = f"SELECT {random.randint(1, 100)};"
#     row = cursor.execute(sql).fetchone()
#     print(row[0])
#     print("Success!")
#
#
TABLE_NAME = "transactions"
#
#
# def create_table(engine):
#     with engine.connect() as conn:
#         sql = textwrap.dedent(
#             f"""
#             DROP TABLE IF EXISTS {TABLE_NAME};
#             """
#         )
#         conn.execute(sql)
#
#     with engine.connect() as conn:
#         sql = textwrap.dedent(
#             """
#             CREATE TABLE transactions(
#                 id VARCHAR(36) DISTKEY NOT NULL,
#                 create_at VARCHAR(26) NOT NULL,
#                 update_at VARCHAR(26) NOT NULL,
#                 note VARCHAR
#             )
#             DISTSTYLE key
#             COMPOUND SORTKEY(create_at);
#             """
#         )
#         conn.execute(sql)
#
#
# def insert_data(engine):
#     print(f"Insert some data into {TABLE_NAME!r} table")
#     with orm.Session(engine) as ses:
#         transaction = Transaction.new(note=f"note {random.randint(1, 1000000)}")
#         ses.add(transaction)
#         ses.commit()
#
#
# def select_data(engine):
#     print(f"Select data from {TABLE_NAME!r} table")
#
#     # return object
#     with orm.Session(engine) as ses:
#         for transaction in ses.query(Transaction):
#             print(
#                 [
#                     transaction.id,
#                     transaction.create_at,
#                     transaction.update_at,
#                     transaction.note,
#                 ]
#             )
#
#     # return python dict
#     # with engine.connect() as conn:
#     #     for transaction in conn.execute(sa.select(Transaction)).mappings():
#     #         print(transaction)
#
#


def read_dataframe(conn: redshift_connector.Connection):
    print("Read data from Redshift into pandas dataframe")
    sql = f"SELECT * FROM {TABLE_NAME} LIMIT 10;"
    df = wr.redshift.read_sql_query(sql, con=conn)
    print(df)

def insert_dataframe(conn: redshift_connector.Connection):

    df = pd.DataFrame(
        [
            (
                "d87e0557-447c-4743-a527-cd26b59720b9",
                "2023-08-09T14:04:58.919920",
                "2023-08-09T14:04:58.919920",
                "note 1",
            )
        ]
    )


if __name__ == "__main__":
    db_conn = DBConn.read_config()
    aws_profile = "awshsh_app_dev_us_east_1"
    boto_ses = boto3.session.Session()
    aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]
    aws_region = boto_ses.region_name

    conn = create_connect_using_iam(db_conn, boto_ses)
    # read_dataframe(conn)

    # df = pd.DataFrame(
    #     [
    #         (
    #             "d87e0557-447c-4743-a527-cd26b59720b9",
    #             "2023-08-09T14:04:58.919920",
    #             "2023-08-09T14:04:58.919920",
    #             "note 1",
    #         )
    #     ],
    #     columns=["id", "create_at", "update_at", "note"],
    # )

    bucket = f"{aws_account_id}-{aws_region}-data"
    path = f"s3://{bucket}/project/redshift-serverless-poc/"

    # wr.redshift.copy(
    #     df=df,
    #     path=path,
    #     con=conn,
    #     schema="public",
    #     table=TABLE_NAME,
    #     mode="append",
    #     boto3_session=boto_ses,
    #     primary_keys=["id"],
    # )

    # df = wr.redshift.read_sql_table(table=TABLE_NAME, schema="public", con=conn)
    # print(df)

    df = pd.DataFrame(
        [
            (
                "d87e0557-447c-4743-a527-cd26b59720b9",
                "2023-08-09T14:04:58.919920",
                "2023-08-09T14:04:58.919920",
                "note 111",
            ),
            (
                "959a2aec-b560-4b1e-9b59-cdca5546f091",
                "2023-08-09T14:04:58.919920",
                "2023-08-09T14:04:58.919920",
                "note 2",
            ),
        ],
        columns=["id", "create_at", "update_at", "note"],
    )
    wr.redshift.copy(
        df=df,
        path=path,
        con=conn,
        schema="public",
        table=TABLE_NAME,
        mode="upsert",
        boto3_session=boto_ses,
        primary_keys=["id"],
    )

    # con = wr.redshift.connect("MY_GLUE_CONNECTION")
    # with con.cursor() as cursor:
    #     cursor.execute("SELECT 1")
    #     print(cursor.fetchall())
    # con.close()

#
#     # engine = create_engine_using_username_password(db_conn)
#     engine = create_engine_using_iam(db_conn, boto_ses)
#     # create_table(engine)
#     # insert_data(engine)
#     # select_data(engine)
