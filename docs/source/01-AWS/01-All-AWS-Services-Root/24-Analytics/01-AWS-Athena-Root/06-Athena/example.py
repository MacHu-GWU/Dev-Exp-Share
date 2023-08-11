# -*- coding: utf-8 -*-

import uuid
import time
import textwrap

import boto3
import polars as pl


def run_athena_query(
    athena_client,
    s3_client,
    bucket: str,
    prefix: str,
    database: str,
    sql: str,
):
    """
    Run athena query and get the result as a polars.DataFrame.
    """
    if prefix.endswith("/") is False:
        prefix = prefix + "/"
    # the sql query should not end with ;, it will be embedded in the final query
    sql = sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1]

    # the dataset folder uri will be used in the UNLOAD command
    # the final parquet files will be stored in this folder
    # note that this folder has to be NOT EXISTING before the execution
    s3uri_dataset_folder = f"s3://{bucket}/{prefix}{uuid.uuid4().hex}/"

    # the metadata folder will be used to store the query result metadata file
    # the metadata file will tell you the list of data file uris
    s3uri_metadata_folder = f"s3://{bucket}/{prefix}"

    # ref: https://docs.aws.amazon.com/athena/latest/ug/unload.html
    # use UNLOAD command to write result into data format other than csv
    final_sql = textwrap.dedent(f"""
    UNLOAD ({sql})
    TO '{s3uri_dataset_folder}'
    WITH ( format = 'parquet' )
    """)
    # print(final_sql)

    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_query_execution.html
    res = athena_client.start_query_execution(
        QueryString=final_sql,
        QueryExecutionContext=dict(
            Catalog="AwsDataCatalog",
            Database=database,
        ),
        ResultConfiguration=dict(
            OutputLocation=s3uri_metadata_folder,
        ),
    )
    # the start_query_execution API is async, it returns the execution id
    exec_id = res["QueryExecutionId"]

    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_execution.html
    # wait for the execution to finish
    for _ in range(10):
        time.sleep(1)
        res = athena_client.get_query_execution(
            QueryExecutionId=exec_id,
        )
        status = res["QueryExecution"]["Status"]["State"]
        if status == "SUCCEEDED":
            break
        elif status in ["FAILED", "CANCELLED"]:
            raise RuntimeError(f"status = {status}")
        else:
            pass

    # read the manifest file to get list of parquet file uris
    res = s3_client.get_object(
        Bucket=bucket,
        Key=f"{prefix}{exec_id}-manifest.csv",
    )
    s3uri_list = res["Body"].read().decode("utf-8").splitlines()

    # read all parquet files and concatenate them into a single polars.DataFrame
    df_list = [
        pl.read_parquet(s3uri)
        for s3uri in s3uri_list
    ]
    df = pl.concat(df_list)

    return df


if __name__ == "__main__":
    boto_ses = boto3.session.Session()
    sts_client = boto_ses.client("sts")
    aws_account_id = sts_client.get_caller_identity()["Account"]
    aws_region = boto_ses.region_name

    athena_client = boto_ses.client("athena")
    s3_client = boto_ses.client("s3")

    bucket = f"{aws_account_id}-{aws_region}-data"
    prefix = f"athena/results/"
    database = "mydatabase"
    sql = textwrap.dedent(f"""
    SELECT * FROM "{database}"."mytable" LIMIT 10;
    """)

    df = run_athena_query(
        athena_client=athena_client,
        s3_client=s3_client,
        bucket=bucket,
        prefix=prefix,
        database=database,
        sql=sql,
    )

    print(df)
