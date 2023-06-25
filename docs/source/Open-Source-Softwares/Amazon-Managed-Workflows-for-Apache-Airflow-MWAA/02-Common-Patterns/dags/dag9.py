# -*- coding: utf-8 -*-

"""
Fan out and Fan in 模式. 以及在 Fan in 模式下的复杂异常处理.
"""

from datetime import datetime
from airflow.decorators import dag, task

dag_id = "dag9"


@dag(
    dag_id=dag_id,
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False,
)
def dag9():
    """
    在这个例子中 task1 fan out 成了 task2 和 task3, task2 和 task4 fan in 成了 task5.
    其中 task2, 4 都有 30% 的几率出错 (大约 50% 的几率两个都成功). 为了能让 task5 能对
    task2, task4 可能出现的各种复杂的成功失败情况进行处理, 我们让 task2 和 task4 在成功的
    时候返回一个值. 而失败的时候抛出异常. 而 task5 则将 task2 和 task4 的返回值作为参数.
    那么一旦收到返回值则说明成功了, 而收到 None 则意味着失败了. 这样我们就可以用 if, else
    写出任意复杂的逻辑了. 这里注意 task5 的 trigger rule 是 all_done. 也就是说 task2, 4
    都成功或失败, 总之是结束了之后再运行.
    """
    task1_id = "task1"
    task2_id = "task2"
    task3_id = "task3"
    task4_id = "task4"
    task5_id = "task5"
    task6_id = "task6"

    @task(task_id=task1_id)
    def task1():
        print("Start task1")
        print("End task1")
        return "Returned by task 1"

    @task(task_id=task2_id)
    def task2():
        import random
        print("Start task2")
        if random.randint(1, 100) <= 30:
            raise Exception("task2 failed")
        print("End task2")
        return "Returned by task 2"

    @task(task_id=task3_id)
    def task3():
        import time
        print("Start task3")
        time.sleep(5)
        print("End task3")
        return "Returned by task 3"

    @task(task_id=task4_id)
    def task4():
        import time
        import random
        print("Start task4")
        time.sleep(5)
        if random.randint(1, 100) <= 30:
            raise Exception("task2 failed")
        print("End task4")
        return "Returned by task 4"

    @task(task_id=task5_id, trigger_rule="all_done") # 这里的 trigger rule 是 all_done
    def task5(task2_return_value: str, task4_return_value: str):
        print("Start task5")
        print(
            f"received task2 return value: {task2_return_value!r}, task4 return value: {task4_return_value!r}"
        )
        print("End task5")

    @task(task_id=task6_id)
    def task6():
        print("Start task6")
        print("End task6")
        return "Returned by task 6"

    run_task1 = task1()
    run_task2 = task2()
    run_task3 = task3()
    run_task4 = task4()
    # task 5 把 2 和 4 的两个前置的返回值作为参数传入, 如果失败了则传入的是 None
    run_task5 = task5(run_task2, run_task4)
    run_task6 = task6()

    # Fan out
    run_task1 >> [run_task2, run_task3]
    run_task2 >> run_task5
    run_task3 >> run_task4 >> run_task5
    run_task5 >> run_task6

run_dag9 = dag9()
