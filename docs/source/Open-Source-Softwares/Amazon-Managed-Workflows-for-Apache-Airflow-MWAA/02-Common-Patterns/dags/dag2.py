# -*- coding: utf-8 -*-

"""
简单的两步任务, 串行.
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag2"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag2():
    """
    这个例子中我们有两个 Task, 先运行 Task 1, 再运行 Task 2. 如果 Task 1 不成功, 则不运行 Task 2.
    我们的两个 Task 的任务都是生成一个随机数, 然后写入到 S3 中. 不过 Task 1 有 50% 的概率会失败.
    你可以看到如果 Task 1 失败了, 则 Task 2 不会被执行.
    """
    task1_id = "task1"
    task2_id = "task2"

    @task(
        task_id=task1_id,
    )
    def task1():
        import json
        import random
        from datetime import datetime

        import boto3

        print("Start task1")

        # 有 50% 的概率失败
        if random.randint(1, 100) <= 50:
            raise Exception("Randomly failed")

        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"

        value = random.randint(1, 100)
        print(f"Generated value is {value}")
        data = {
            "value": value,
            "datetime": datetime.now().isoformat(),
        }
        boto3.client("s3").put_object(
            Bucket=f"{aws_account_id}-{aws_region}-data",
            Key=f"projects/mwaa-poc/{dag_id}/{task1_id}.output.json",
            Body=json.dumps(data),
            ContentType="application/json",
        )

        print("End task1")
        return "Returned by task 1"

    @task(
        task_id=task2_id,
    )
    def task2():
        import json
        import random
        from datetime import datetime

        import boto3

        print("Start task2")

        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"

        value = random.randint(1, 100)
        print(f"Generated value is {value}")
        data = {
            "value": value,
            "datetime": datetime.now().isoformat(),
        }
        boto3.client("s3").put_object(
            Bucket=f"{aws_account_id}-{aws_region}-data",
            Key=f"projects/mwaa-poc/{dag_id}/{task2_id}.output.json",
            Body=json.dumps(data),
            ContentType="application/json",
        )

        print("End task2")
        return "Returned by task 2"

    # 这里调用了两个 task 函数, 就相当于告诉 Airflow 我要运行他们两. 默认情况下 Airflow
    # 认为它们是并行, 没有依赖关系, 但是如果你用 >>, << 这样的符号连接他们, 就表示他们是
    # 有依赖关系的.
    # Ref: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#setting-up-dependencies
    run_task1 = task1()
    run_task2 = task2()

    run_task1 >> run_task2


run_dag2 = dag2()
