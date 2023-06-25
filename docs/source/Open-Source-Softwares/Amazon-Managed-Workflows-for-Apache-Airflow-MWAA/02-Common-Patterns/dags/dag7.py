# -*- coding: utf-8 -*-

"""
在任意的两个 Task 之间传递大数据.
"""

from datetime import datetime
from airflow.decorators import dag, task

# 导入 get_current_context
from airflow.operators.python import get_current_context


dag_id = "dag7"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag7():
    """
    这个例子中我们有三个 Task, 按照 task 1, 2, 3 的顺序执行. 其中 task 1 的返回值是做为
    task 3 的输入参数输入的. 但是我们假设 task 1 的返回值非常大, 不适合用 XCome 直接返回.
    """
    task1_id = "task1"
    task2_id = "task2"
    task3_id = "task3"

    @task(
        task_id=task1_id,
    )
    def task1():
        """
        这里我们从 context 中获得 run_id 后, 和 dag id 一起计算出一个 S3 location,
        并将输出结果储存在里面.
        """
        import boto3
        import uuid
        from pprint import pprint

        print("Start task1")

        context = get_current_context()
        print("context:")
        pprint(context)
        run_id = context["run_id"]

        value = uuid.uuid4().hex
        print(f"task1 generates value: {value!r}")

        print("write task 1 output to S3")
        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"
        boto3.client("s3").put_object(
            Bucket=f"{aws_account_id}-{aws_region}-data",
            Key=f"projects/mwaa-poc/{dag_id}/{run_id}/{task1_id}.output.txt",
            Body=value,
            ContentType="text/plain",
        )

        print("End task1")
        return value  # 返回值

    @task(
        task_id=task2_id,
    )
    def task2():
        print("Start task2")
        print("End task2")
        return "Returned by task 2"

    @task(
        task_id=task3_id,
    )
    def task3():
        """
        这里我们从计算出的 S3 location 处读取数据.
        """
        import boto3

        print("Start task3")

        context = get_current_context()
        run_id = context["run_id"]

        print("read task 1 output from S3")
        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"
        value = (
            boto3.client("s3")
            .get_object(
                Bucket=f"{aws_account_id}-{aws_region}-data",
                Key=f"projects/mwaa-poc/{dag_id}/{run_id}/{task1_id}.output.txt",
            )["Body"]
            .read()
            .decode("utf-8")
        )
        print(f"task 1 output: {value!r}")

        print("End task3")
        return "Returned by task 3"

    run_task1 = task1()
    run_task2 = task2()
    run_task3 = task3()

    run_task1 >> run_task2 >> run_task3


run_dag7 = dag7()
