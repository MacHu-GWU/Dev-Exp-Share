MWAA Hands on Practice
==============================================================================


配置 Airflow DAG 的开发环境
------------------------------------------------------------------------------
1. 首先推荐你在 Virtualenv 中进行本地开发.
2. 其次你如果使用的是 AWS MWAA, 那么推荐你使用跟 Airflow 相对应版本的 Python 版本 (你创建 MWAA environment 的时候就会让你选 Airflow 的版本), 具体的对应关系可以参考 `这篇官方文档 <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-faqs.html#python-version>`_

.. code-block:: bash

    # Quick Start
    export AIRFLOW_HOME=~/airflow

    AIRFLOW_VERSION=2.5.1

    # Extract the version of Python you have installed. If you're currently using Python 3.11 you may want to set this manually as noted above, Python 3.11 is not yet supported.
    PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
    # For example this would install 2.5.1 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.8.txt

    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

    virtualenv -p python3.8 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    aws s3 cp dag1.py s3://807388292768-us-east-1-airflow/dags/dag1.py

    # 将所有的 DAG 文件上传到 S3
    aws s3 sync ./dags s3://807388292768-us-east-1-airflow/dags/ --profile awshsh_app_dev_us_east_1


如何定义依赖关系

如何定义复杂的 DAG 编排

如何在 Task 之间传递数据

如何定义 Schedule


1. 简单的单步任务.
2. 简单的两步任务, 串行.
3. 简单的两步任务, 并行.
4. 在 Task 中使用第三方包, 也就是使用 Virtualenv 来运行 Task.
5. 如何在相邻的两个 Task 之间传递数据, 同时定义它们的依赖关系 (接收数据的 Task 依赖于发送数据的 Task).
6. 如何在任意两个 Task 之间传递数据, 而不要求相邻, 使用 XCom 的来传递可序列化的小型数据.
7. 如何在任意两个 Task 之间传递数据, 而不要求相邻, 使用 S3 来传递大型数据.
8. 如何实现 Long Polling 的模式, 也就是启动一个 Task 之后, 等待这个 Task 成功, 失败, 或超时.


Airflow 实战基础篇
------------------------------------------------------------------------------

1. 简单的单步任务
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
直接看例子.

.. literalinclude:: ./dags/dag1.py
   :language: python
   :linenos:


2. 简单的两步任务, 串行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
直接看例子.

.. literalinclude:: ./dags/dag2.py
   :language: python
   :linenos:


3. 简单的两步任务, 并行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
直接看例子.

.. literalinclude:: ./dags/dag3.py
   :language: python
   :linenos:


4. 使用第三方 Python 包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
直接看例子.

.. literalinclude:: ./dags/dag4.py
   :language: python
   :linenos:

5. 在相邻的两个 Task 之间传递数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6. 在任意的两个 Task 之间传递小数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在编排任务中, 在任意两个 Task 之间, 包括不相邻的两个 Task 之间传递数据是很常见的需求. 从 Airflow 1.X 起, 就自带 XComs (Cross Communication) 这一功能, 能在 Tasks 之间传递数据. 它的原理其实是在 Scheduler 上维护一个 Key Value Store, 其中 Key 是 dag_id + task_id 合起来的一个 compound key. 你可以把 value 存在里面, 自然也可以在任何其他的 task 中引用这个 value. 而从 Airflow 2.X 起, 引入了 TaskFlow 这一更加人类友好的 API. 在 TaskFlow API 下, 所有的 PythonOperator Task 的返回值都会默认被包装为一个 XComs, 而你可以直接像写 Python 函数一样在 Tasks 之间传递参数, 而无需显式在其他 Task 引用之前的 Task 的返回值.

但是注意, 能被 XComs 传递的数据必须要是可序列化的对象, 例如 Str, Int, 或是 JSON dict. 而且大小不能超过 48KB. 但这不是什么问题. 对于复杂数据结构, 你只要自己定义一套轻量的 JSON 序列化接口来返回 Task 的输出即可, 你甚至可以用 pickle 或是 JSONPickle 将其 dump 成二进制数据然后 base64 编码. 而对于体积很大的数据, 你可以将数据写入到 AWS S3, 然后返回一个 S3 uri, 传递给后续的 task, 然后后续的 task 再从 S3 读取数据即可.

Reference:

- `XComs (Cross Communication) <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html>`_
- `TaskFlow <https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html>`_


7. 在任意的两个 Task 之间传递大数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有时候一个 Task 返回的数据量非常大, 由于 XComs 又 48KB 的限制, 这时就要另外想办法了. XComs 被设计为用来传递小数据的, 它不允许你用它来储存任意大的数据, 占用服务器资源.

一个比较直观的解决方案是利用全局可用的 context 对象. 它是一个字典的数据结构, 在整个 DAG 执行的生命周期内都存在. 记录了一些全局变量之类的信息. 其中就有一个 ``run_id`` 的字段, 它的值是一个包含时间戳的唯一的值, 看起来像这样 ``manual__2023-01-01T01:23:45.123456+00:00`` 或 ``scheduled__2021-01-01T00:00:00+00:00``. 精确到微秒. 其中 manual 代表你手动运行的, 而 scheduled 代表按照 scheduler 的调度规则执行的. 你可以用它和 DAG ID 合起来作为一个唯一的 Key, 然后用任何 Key Value Store 的 backend 来储存这个数据. 例如 AWS S3 或 DynamoDB 都可以. 如果你的需要访问这个数据的并发性高 (例如你用到了 Map 并行, 所有并行 Task 都需要读写同一个数据) 且数据量不大 (48KB - 400KB) 之间, 那么用 DynamoDB 就比较合适, 能确保读写的原子性. 而如果你仅仅是进行数据传递但数据量很大, 那么用 S3 就比较合适.

我们稍微的扩展一下, 其实我们可以不限定只使用一个 Key, 而是基于 DAG ID 和 ``run_id`` 可以创造出多个 Key, 然后将 Key 作为参数用 XComs 返回即可. 基于这种策略你可以几乎做到任何事.

Reference:

- `Accessing current context <https://airflow.apache.org/docs/apache-airflow/2.0.0/concepts.html#accessing-current-context>`_


8. Poll for Job Status 模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Poll for Job 模式常用于你有一个异步执行, 耗时较长的 Task 的情况. 举例来说, 你要用 AWS Glue 来运行一个耗时在 1 - 5 分钟的 ETL Job. 如果 Glue Job 成功, 则继续后面的步骤. 如果 Glue Job 失败, 则停止整个 DAG. 如果 Glue Job 超时, 则视为失败, 也停止 DAG. 这个模式就叫做 Poll for Job.

这个模式的一个通用解决方案是, 在异步执行这个 Task 后 (我们继续拿 AWS Glue Job 举例) 隔一段时间就去查询一下运行状态, 如果是 in progress 就等下一次, 如果是 succeeded 就继续后面的步骤, 如果是 failed 或 timeout 就停止 DAG.

而根据直觉, 这个 "隔一段时间" 一般我们会用 ``import time``, ``time.sleep(60)`` 来实现. 等于这个进程被挂在那里 60 秒, 占用了服务器资源. 这也叫 **同步轮询**. 想象一下, 很可能你 check status 只需要 1 秒, 但 60 秒都在占用服务器资源, 如果你有 60 个这样的程序, 相当于你有 60 个 Python 程序一直在吃内存.

一个成熟的调度系统一般会把这个等待的事情交给一个调度系统来做, 例如一个每 1 毫秒心跳一次的 event loop. 当它等待 60 秒后, 就异步的来执行这个 check status 的操作, 所以这也叫 **异步轮询**. 这样 60 个这样的程序本质上相当于每个只占在运行的那 1 秒内占用了系统资源, 60 个程序占用的资源和 1 个旧版程序一样多, 大大提高了资源利用率.

- `Core Concepts - Sensors <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html>`_
- `Using the TaskFlow API with Sensor operators <https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html#using-the-taskflow-api-with-sensor-operators>`_

我们来看一下官方文档中的一个例子, 理解一下在 Airflow 中应该如何实现这个模式. 为了帮助理解, 我在官方的文档的基础上增加了很多保姆级注释.

.. code-block:: python

    from airflow.decorators import dag, task
    from airflow.sensors.base import PokeReturnValue

    # @task.sensor 的全部参数请参考下面两个文档, 其中 BaseSensorOperator 是基类,
    # ExternalTaskSensor 是子类, 全部参数是两者之和
    # - BaseSensorOperator: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/base/index.html#airflow.sensors.base.BaseSensorOperator
    # - ExternalTaskSensor: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/external_task/index.html#airflow.sensors.external_task.ExternalTaskSensor
    @task.sensor(
        # 每多少秒检查一次状态
        poke_interval=60,
        # 以供多少秒后超时
        timeout=300,
        # Airflow 同时支持 同步轮询 和 异步轮询 两种模式
        # poke 就是同步模式, 等待期间也占用一个 worker 字眼
        # reschedule 就是异步模式,
        # 简单来说, 你查询的频率越高, 那么异步执行反复释放和重新 import 到内存的开销就越不值当
        # 就应该用 poke 模式索性一直占用一个 worker
        # 而如果你查询的频率不高, 那么就应该在等待期间释放资源, 等下一次再 load 也没关系
        # 就应该用 reschedule 模式
        # mode="poke",
        mode="reschedule",
    )
    def wait_for_upstream() -> PokeReturnValue:
        """
        用 @task.sensor 包装起来的函数最好返回一个 PokeReturnValue 对象, 它只有两个参数:

        - is_done: bool, 表示是否已经完成, 这里的完成指的是是否可以停止轮询, 无论是成功还是
            失败都可以视为 "完成". 逻辑上你查询到的外部任务的状态如果你认为没有必要再查询了,
            例如成功, 失败, 或者是失败进行中, 失败后回滚中, 你都能预料到最终结局了, 这时就
            该返回 is_done = True.
        - xcom_value: 这是 Airflow 在两个 task 之间传递 data 的机制, 必须要是个可序列化对象,
            而且不能超过 48KB. 一般你用来将外部任务的状态信息传递给下一个 task, 例如成功, 失败,
            以及任何额外的信息, 例如失败原因, debug 信息等.

        这里有一个点. 很多人会想说如果失败了, 那么就直接在这个 Sensor task 里 raise 一个异常.
        如果成功了, 就直接在这个 task 里继续运行下一个 task 的逻辑, 这样就可以少写一个 task,
        降低系统复杂度了. 其实不然. 这样做等于是将调度逻辑和业务逻辑放在了一起, 失去了使用调度
        系统的意义. 并且你的代码违背了一段代码只做一件事的原则, 如果你的业务代码不小心有 bug,
        那么就会拖累这个调度逻辑, 使得调度逻辑也失败了. 这样做弊大于利.
        """
        # your get status logic here
        # the status is a string: "doing", "succeeded", "failed"
        status: str = get_status(...)
        if status == "doing":
            return PokeReturnValue(is_done=False)
        elif status in ["succeeded", "failed"]:
            return PokeReturnValue(is_done=True, xcom_value=status)
        else:
            raise NotImplementedError(f"unknown status: {status!r}"))

好了我们了解了原理之后, 就来看一个非常具体的例子. 下面这个脚本模拟了一个耗时 20 秒的外部任务. 请仔细阅读里面的注释, 里面介绍了这个任务的逻辑.

.. literalinclude:: ./dag8_external_task.py
   :language: python
   :linenos:

然后我们来看一下这个 DAG 定义. 同样的, 请自诩阅读里面的注释.

.. literalinclude:: ./dags/dag8.py
   :language: python
   :linenos:

好了现在我们对如何用 Airflow 实现 Poll Job 模式有一个比较清晰的认识了. 我们不妨再展开一点点,

如果这个耗时较长的业务逻辑是写在 Task 里的, 注意这里说的不是你调用一个外面的 API 让真正的运算资源远程执行, 而是说你的业务逻辑例如数据处理就卸载了 Task 函数里面. 这种情况你没有必要用 Sensor. 你直接就在这个 Task 里用 ``try ... except ...`` 判断是否成功, 如果出现了 ``try ... except ...`` 每预料到的错误, 那么就让他 fail 即可.

而如果这个耗时较长的业务只是一个外部的 API 调用, 例如你要跑一个 AWS Glue Job. 那么你在这个 Task 里就写异步调用的逻辑即可, 然后将 job id 传递给后面的 Sensor task 来轮询状态即可. 例如:

.. code-block:: python

    @task(...)
    def run_aws_glue_job() -> str:
        res = boto3.client("glue").glue.start_job_run(...)
        return res["JobRunId"]


9. Fan out and Fan in 模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fan out 指的是一个任务之后, 并行的执行多个任务.

而 Fan in 指的是只有多个任务都完成之后, 才能继续执行下一个任务. 这里有一些变化, 例如你想要 3 个任务里的至少 2 个完成才执行下一个. 又或者你想要 1 号任务必须完成, 而 2 和 3 之中至少有一个完成. 这种复杂的情况该怎么做呢? 简单来说, `BaseOperator <https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html#airflow.models.baseoperator.BaseOperator>`_ 有一个参数 ``trigger_rule`` 可以是 ``{ all_success | all_failed | all_done | all_skipped | one_success | one_done | one_failed | none_failed | none_failed_min_one_success | none_skipped | always }`` 中的一个, 可以决定某个人物是否执行的条件是前置的多个任务全部成功,  全部失败, 有一个失败, 等等. 可以应对大部分的业务情况. 而对于超级复杂的情况, 你可以简单的把所有的前置 task 都用 try except 包裹起来自己做异常处理, 然后返回一个 status. 然后后续任务使用 all_done, 然后把所有前置 task 的返回值作为参数传入, 然后自己用 if else 判断分析即可实现任何复杂逻辑.

请看下面这个 DAG 的例子.

.. literalinclude:: ./dags/dag9.py
   :language: python
   :linenos:
