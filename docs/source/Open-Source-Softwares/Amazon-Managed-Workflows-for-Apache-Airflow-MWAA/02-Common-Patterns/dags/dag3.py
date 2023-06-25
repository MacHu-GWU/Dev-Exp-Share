# -*- coding: utf-8 -*-

"""
简单的两步任务, 并行.
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag3"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag3():
    """
    这个例子中我们有两个 Task, 两个 Task 并行.
    我们的两个 Task 的任务都是生成一个随机数, 然后写入到 S3 中. 不过 Task 1 有 50% 的概率会失败.
    对于并行的任务, 如果其中一个失败了, 则整个 DAG 会失败, 但是并不会阻止其他任务失败.
    根据实验结果, 可以看出不管 Task 1 失败与否, Task 2 都成功了.

    而 Airflow 允许你手动的对具体的 Task 进行重试, 如果你在 Airflow UI 里可以看到 Task 1
    红了 (失败了), 你点进去在 Task Action 里 Run 即可对 Task 1 重运行. 不过默认是不允许
    已经失败的任务进行重试的. 除非你手动选择了 Ignore All Deps 选项 (它的意思是忽略所有依赖
    条件, 这里的依赖就包括了不允许冲运行已经失败的任务).
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
    # 认为它们是并行, 没有依赖关系.
    # Ref: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#setting-up-dependencies
    run_task1 = task1()
    run_task2 = task2()


run_dag3 = dag3()
