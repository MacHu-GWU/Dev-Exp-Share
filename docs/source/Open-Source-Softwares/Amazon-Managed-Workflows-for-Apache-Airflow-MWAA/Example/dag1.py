import boto3
import random
import datetime
from pprint import pprint
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain


@task(
    task_id="print_the_context",
)
def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    boto3.client("s3").put_object(
        Bucket="807388292768-us-east-1-data",
        Key="projects/mwaa-poc/dag1.output.txt",
        Body=str(random.randint(1, 100)),
        ContentType="text/plain",
    )
    return "Whatever you return gets printed in the logs"


@dag(
    dag_id="dag1",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@once",
)
def generate_dag():
    run_this = print_context()
    chain(run_this)


generate_dag()
