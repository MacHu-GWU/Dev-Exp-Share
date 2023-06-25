# -*- coding: utf-8 -*-

"""
在 Task 中使用第三方包, 也就是使用 Virtualenv 来运行 Task.
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag4"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag4():
    """ """
    task1_id = "task1"

    # @task.virtualenv 装饰器表示这个 task 需要在一个 Virtualenv 中运行.
    # 它的底层其实是 PythonVirtualenvOperator
    # Ref: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.PythonVirtualenvOperator
    @task.virtualenv(
        task_id=task1_id,
        # 如果不指定这个参数, 则默认使用 Airflow 所用的 Python 版本, 这里我们看了 MWAA 上
        # Airflow 2.5.1 对应的 Python 版本是 3.10
        # 如果你需要使用一个跟 Airflow 不同的 Python 解释器, 那么推荐你不要使用 task.virtualenv
        # 而是使用 @task.external_python. 你需要在 Airflow 服务器上安装你需要的版本的 Python,
        # 并在参数中指定 Python interpreter 的路径. 不过在 MWAA 上你做不到这一点, 因为
        # 服务器是由 AWS 所管理的. 这种情况下我推荐使用 docker package, 用容器来运行
        # Ref: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html
        python_version="3.10",
        # 这里是所有依赖的具体版本, 我建议使用固定版本, 不要使用范围, 这样可以保证每次
        # 运行的环境 100% 一样. 至于如何确定固定版本, 我推荐使用 poetry 来管理并解析依赖
        # 然后输出一个完全固定的版本列表, 并包括 hashes, 以防止注入攻击.
        requirements=[
            "s3pathlib>=2.0.1,<3.0.0",
        ],
        # 表示是否把 system python 中的包也自动添加进来. 这个 system python 也就是
        # Airflow 所在的 Python, Airflow 可包含了一堆杂七杂八哦的包, 说不准哪个就跟你的
        # 项目依赖有冲突, 99.99% 的情况下都选择 False.
        system_site_packages=False,
    )
    def task1():
        import json
        import random
        from datetime import datetime

        import boto3
        from s3pathlib import S3Path, context

        print("Start task1")

        aws_region = "us-east-1"
        boto_ses = boto3.session.Session(region_name=aws_region)
        aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]
        context.attach_boto_session(boto_ses)

        value = random.randint(1, 100)
        print(f"Generated value is {value}")
        data = {
            "value": value,
            "datetime": datetime.now().isoformat(),
        }
        s3path = S3Path(
            f"s3://{aws_account_id}-{aws_region}-data/projects/mwaa-poc/{dag_id}/{task1_id}.output.json"
        )
        s3path.write_text(
            json.dumps(data),
            content_type="application/json",
        )

        print("End task1")
        return "Returned by task 1"

    run_task1 = task1()


run_dag4 = dag4()
