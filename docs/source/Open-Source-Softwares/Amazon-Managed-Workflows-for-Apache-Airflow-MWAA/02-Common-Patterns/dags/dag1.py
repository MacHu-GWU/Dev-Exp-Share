# -*- coding: utf-8 -*-

"""
简单的单步任务.
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag1"

@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag1():
    """
    这个例子中只有一个 Task.
    """
    task1_id = "task1"

    @task(
        task_id=task1_id,
    )
    def task1():
        """
        该任务随机生成一个 1 - 100 的随机数, 并将这个值和当前的事件一起写入到 S3 中.
        """
        # 注意, 任何跟执行任务相关, 需要 import 的包, 都需要在函数内部 import.
        # 因为 task 函数外部的内容都属于调度器的运行环境, 而 task 函数内则是执行器的运行环境
        # 通常情况下, 调度器只要有 Airflow 服务器自带的包就够了, 而执行器很可能需要在
        # virtualenv 中运行, 可能需要任何包.
        # Ref: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code
        import json
        import random
        from datetime import datetime

        import boto3 # 标准的开源 Airflow 并不预装 boto3, 而 AWS MWAA 预装了 boto3.

        print("Start task1")

        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"

        value = random.randint(1, 100)
        print(f"Generated value is {value}")
        data = {
            "value": value,
            "datetime": datetime.now().isoformat(),
        }
        # 记得确保你的 MWAA 的 IAM Role 里有这个 bucket 的读写权限
        boto3.client("s3").put_object(
            Bucket=f"{aws_account_id}-{aws_region}-data",
            Key=f"projects/mwaa-poc/{dag_id}/{task1_id}.output.json",
            Body=json.dumps(data),
            ContentType="application/json",
        )

        print("End task1")
        # 在 Python Operator (也就是 @task 装饰器装饰的函数) 中, 返回值将会被视为 Task Output
        # 这个返回值一定要是一个可序列化的对象, 因为 Airflow 会自动负责将这个对象序列化后以备
        # 后续的 task 使用 (虽然这个例子中没有).
        return "Returned by task 1"

    run_task1 = task1() # 你只要调用这个 task 函数就相当于告诉 Airflow 我要运行这个 task 了.


run_dag1 = dag1()
