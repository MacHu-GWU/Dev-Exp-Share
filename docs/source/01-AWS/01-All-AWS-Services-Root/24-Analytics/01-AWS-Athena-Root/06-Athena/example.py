# -*- coding: utf-8 -*-

"""
This script demonstrate the best practice using parquet file to store Athena query result.
It loads the parquet dataset (many parquet files) from S3.
"""

import typing as T
import uuid
import time

import s3fs
import polars as pl
import pyarrow.dataset

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager
    from s3pathlib import S3Path


def wait_athena_query_to_succeed(
    bsm: "BotoSesManager",
    exec_id: str,
    delta: int = 1,
    timeout: int = 30,
):
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_execution.html
    # wait for the execution to finish
    for _ in range(timeout):
        res = bsm.athena_client.get_query_execution(
            QueryExecutionId=exec_id,
        )
        status = res["QueryExecution"]["Status"]["State"]
        if status == "SUCCEEDED":
            return
        elif status in ["FAILED", "CANCELLED"]:
            raise RuntimeError(f"status = {status}")
        else:
            time.sleep(delta)
    raise TimeoutError(f"athena query timeout in {timeout} seconds!")


def run_athena_query(
    bsm: "BotoSesManager",
    s3dir_result: "S3Path",
    database: str,
    sql: str,
    delta: int = 1,
    timeout: int = 30,
    verbose: bool = True,
) -> pl.LazyFrame:
    """
    Run athena query and get the result as a polars.LazyFrame.
    With LazyFrame, you can do further select, filter actions before actually
    reading the data, and leverage the parquet predicate pushdown feature to
    reduce the amount of data to be read. If you just need to return the
    regular DataFrame, you can do ``df = run_athena_query(...).collect()``.

    Example::

        >>> from boto_session_manager import BotoSesManager
        >>> from s3pathlib import S3Path
        >>>
        >>> bsm = BotoSesManager(profile_name="your_aws_profile")
        >>> bucket = f"{bsm.aws_account_id}-{bsm.aws_region}-data"
        >>> prefix = f"athena/results/"
        >>> s3dir_result = S3Path(f"s3://{bucket}/{prefix}").to_dir()

        >>> database = "your_database"
        >>> sql = f"SELECT * FROM {database}.your_table LIMIT 10;"
        >>> df = run_athena_query(
        ...     bsm=bsm,
        ...     s3dir_result=s3dir_result,
        ...     database=database,
        ...     sql=sql,
        ... ).collect()
        >>> df
        ...

    :param bsm: boto_session_manager.BotoSesManager object.
    :param s3dir_result: an S3Path object that represent a s3 directory to store
        the athena query result.
    :param database: database name.
    :param sql: sql query string.
    :param delta: sleep time in seconds between each query status check.
    :param timeout: timeout in seconds.
    :param verbose: do you want to print the log?
    """
    # the sql query should not end with ;, it will be embedded in the final query
    sql = sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1]

    # the dataset folder uri will be used in the UNLOAD command
    # the final parquet files will be stored in this folder
    # note that this folder has to be NOT EXISTING before the execution
    s3dir_dataset = s3dir_result.joinpath("dataset", uuid.uuid4().hex).to_dir()

    # the metadata folder will be used to store the query result metadata file
    # the metadata file will tell you the list of data file uris
    s3dir_metadata = s3dir_result.joinpath("metadata").to_dir()

    # ref: https://docs.aws.amazon.com/athena/latest/ug/unload.html
    # use UNLOAD command to write result into data format other than csv
    final_sql = textwrap.dedent(
        f"""
        UNLOAD ({sql})
        TO '{s3dir_dataset.uri}'
        WITH ( format = 'parquet' )
        """
    )

    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_query_execution.html
    # you may need to customize this for more advanced query,
    # like cross database query, federated query
    res = bsm.athena_client.start_query_execution(
        QueryString=final_sql,
        QueryExecutionContext=dict(
            Catalog="AwsDataCatalog",
            Database=database,
        ),
        ResultConfiguration=dict(
            OutputLocation=s3dir_metadata.uri,
        ),
    )
    # the start_query_execution API is async, it returns the execution id
    exec_id = res["QueryExecutionId"]

    # wait for the execution to finish
    wait_athena_query_to_succeed(bsm=bsm, exec_id=exec_id, delta=delta, timeout=timeout)

    # read the manifest file to get list of parquet file uris
    s3path_manifest = s3dir_metadata.joinpath(f"{exec_id}-manifest.csv")
    s3uri_list = s3path_manifest.read_text(bsm=bsm).splitlines()

    if verbose:
        print(f"query result manifest: {s3path_manifest.console_url}")
        print(f"query result data: {s3dir_dataset.console_url}")
        print(f"number of files in result: {len(s3uri_list)}")

    if isinstance(bsm.profile_name, str):
        profile = bsm.profile_name
    else:
        profile = None

    fs = s3fs.S3FileSystem(profile=profile)
    dataset = pyarrow.dataset.dataset(s3uri_list, filesystem=fs)
    lazy_df = pl.scan_ds(dataset)
    df = lazy_df.select(pl.col("*"))
    return df


if __name__ == "__main__":
    import random
    import textwrap

    from boto_session_manager import BotoSesManager
    from s3pathlib import S3Path

    bsm = BotoSesManager()

    bucket = f"{bsm.aws_account_id}-{bsm.aws_region}-data"
    prefix = f"athena/results/"
    s3dir_result = S3Path(f"s3://{bucket}/{prefix}").to_dir()

    database = "dynamodb_to_datalake"
    table = "transactions"

    n = random.randint(100, 500)
    sql = textwrap.dedent(
        f"""
        SELECT * 
        FROM "{database}"."{table}"
        LIMIT {n};
    """
    )

    df = run_athena_query(
        bsm=bsm,
        s3dir_result=s3dir_result,
        database=database,
        sql=sql,
    ).collect()

    print(df.shape)
    print(df)
    assert df.shape[0] == n
