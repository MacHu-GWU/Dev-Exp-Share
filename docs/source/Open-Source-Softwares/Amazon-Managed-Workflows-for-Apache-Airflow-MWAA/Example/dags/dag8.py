# -*- coding: utf-8 -*-

"""
如何实现 Long Polling 的模式, 也就是启动一个 Task 之后, 等待这个 Task 成功, 失败, 或超时.
"""

from datetime import datetime
from airflow.decorators import dag, task
from airflow.sensors.base import PokeReturnValue

dag_id = "dag8"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag8():
    """
    在这个例子中我们会在本地电脑上运行一个耗时 20 秒的脚本, 用于模拟 ExternalTask 的异步执行.
    """
    task1_id = "task1"
    task2_id = "task2"

    @task.sensor(
        task_id=task1_id,
        poke_interval=2,
        timeout=30,
        mode="poke",
    )
    def task1_check_status():
        """
        这个任务会隔一段时间检查一次 Task0 (也就是外部任务) 的状态, 超过 30 秒还没有成功或失败
        就算超时. 由于我们的检查频率较高, 所以用 poke 模式.
        """
        import boto3
        from datetime import datetime

        print("Start task1")
        print(f"current time is {datetime.utcnow()}")

        # 从 S3 中读取 task0 的状态
        aws_account_id = boto3.client("sts").get_caller_identity()["Account"]
        aws_region = "us-east-1"

        status = (
            boto3.client("s3")
            .get_object(
                Bucket=f"{aws_account_id}-{aws_region}-data",
                Key=f"projects/mwaa-poc/{dag_id}/task0.status.txt",
            )["Body"]
            .read()
            .decode("utf-8")
        )
        print(f"get status: {status!r}")

        # 如果状态是 succeeded 或 failed, 则结束等待, 并将状态作为返回值返回
        if status in ["succeeded", "failed"]:
            print("End task1 check status")
            return PokeReturnValue(is_done=True, xcom_value=status)
        else:
            return PokeReturnValue(is_done=False)

    @task(
        task_id=task2_id,
    )
    def task2_decide_next_step(status):
        """
        对检测到的 task 0 的状态信息进行处理.
        """
        print("Start task2")
        print(f"received status is {status!r}")
        if status == "succeeded":
            print("external task succeeded")
            print("End task2")
            return "Returned by task 2"
        elif status == "failed":
            print("external task failed")
            raise ValueError("external task failed")
        else:  # pragma: no cover
            raise NotImplementedError

    # 把 task1_check_status 的返回值传递给 task2_decide_next_step
    task2_decide_next_step(task1_check_status())


run_dag8 = dag8()
