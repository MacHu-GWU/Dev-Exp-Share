# -*- coding: utf-8 -*-

"""
在任意的两个 Task 之间传递小数据.

Airflow Python programming style guide:

1. 定义 dag 的函数名使用 名词, 例如 ``dag_${description}``. 而将其实例化的变量名使用
    ``run_dag_${description} = dag_${description}(...)``. 例如:

.. code-block:: python

    @dag(...)
    def dag_my_description():
        ...

    run_dag = dag_my_description()

2. 定义 task 的函数名使用 名字, 例如 ``task_${description}``. 而运行 task 的实例, 又
    或是 task 的返回值则用 ``run_task_${description}``. 例如:

.. code-block:: python

    @dag(...)
    def dag_my_description():
        @task(...)
        def task1_description():
            pass

        @task(...)
        def task2_description():
            pass

        run_task1 = task1_description()
        run_task2 = task2_description()

        run_task1 >> run_task2

    run_dag = dag_my_description()
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag6"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag6():
    """
    这个例子中我们有三个 Task, 按照 task 1, 2, 3 的顺序执行. 其中 task 1 的返回值是做为
    task 3 的输入参数输入的.
    """
    task1_id = "task1"
    task2_id = "task2"
    task3_id = "task3"

    @task(
        task_id=task1_id,
    )
    def task1():
        import uuid

        print("Start task1")
        value = uuid.uuid4().hex
        print(f"task1 generates value: {value!r}")
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
    def task3(task1_output_value):
        print("Start task3")
        print(f"Received task1_output_value: {task1_output_value!r}")
        print("End task3")
        return "Returned by task 3"

    run_task1 = task1()
    run_task2 = task2()
    run_task1 >> run_task2 >> task3(run_task1)  # task3 的输入参数是 run_task1 的返回值


run_dag6 = dag6()
