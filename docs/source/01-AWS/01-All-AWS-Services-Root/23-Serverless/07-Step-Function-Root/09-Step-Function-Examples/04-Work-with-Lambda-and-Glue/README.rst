Work with Lambda and Glue
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, Lambda, Glue

StepFunction 本身作为一款 Serverless 的编排工具, 用来管理同样是 Serverless 的 Lambda Function 和 Glue Job 是再合适不过的了. 本文将用一种比较简单的应用场景为例, 介绍如何使用 StepFunction 来编排 Lambda 和 Glue Job. 在这个简单的例子中, 所有的数据传递都是静态的, 不存在说进行中间态的数据处理的情况. 显然这个例子不适用于所有的情况, 但是静态的场景比动态场景要简单, 掌握了静态场景的情况有助于你学习如何处理动态场景.


理解我们的需求
------------------------------------------------------------------------------
在我们的工作流中, 我们有多个 Lambda 和 Glue Job. 它们之间互相都是独立的, 并不需要互相之间传递数据. 但是可能会有先后顺序的依赖关系. 换言之, 我们只有先运行一个, 再运行一个的需求, 而没有说后面的那个需要前面的结果作为参数的情况.


Task 1 - Glue Job
------------------------------------------------------------------------------
我们假设 task1 是一个 Glue Job, 它的 argument 是一个 key value pairs 的字典, 例如:

.. code-block:: python

    {
        "parameter1": "value1",
        "parameter2": "value2"
    }

在写 Glue Job Script 的时候, 最重要的的是下面这段代码, 它能从 ``spark-submit`` 命令中读你的参数. 注意你的参数名最好都用下划线, 虽然 hyphen 也可以, 但是不推荐.

.. code-block:: python

    from awsglue.utils import getResolvedOptions

    args = getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "parameter1",
            "parameter2",
        ],
    )

完整的 Glue Job 代码如下, 它的逻辑是仅仅打印输入参数:

.. literalinclude:: ./glue_job.py
   :language: python
   :linenos:


Task 2 - Lambda Function
------------------------------------------------------------------------------
我们假设 task2 是一个 Lambda Function, 它的 argument 是任意的 key value pairs 的字典, 例如:

.. code-block:: python

    {"name": "alice"}

完整的 Lambda Function 代码如下, 它的逻辑是仅仅打印输入参数:

.. literalinclude:: ./lambda_function.py
   :language: python
   :linenos:


Step Function 的输入参数
------------------------------------------------------------------------------
我们假设我们的 Workflow 是先 async 运行 Glue Job, 然后直接运行 Lambda Function. 那么 StepFunction 的输入参数应该是:

.. code-block:: python

    {
        "task1": {
            "--parameter1": "value1",
            "--parameter2": "value2"
        },
        "task2": {"name": "task2"}
    }

注意, Glue Job 的底层是 ``spark-submit`` 命令, 所有的入参都是命令行参数. 所以你要在你的参数前面加 ``--``.


Step Function Definition
------------------------------------------------------------------------------
Step Function 的源码中, 最重要的部分是如何把上一节中的输入参数传递给 Glue Job 和 Lambda Function.

其中给 Glue Job 传递参数时最关键的一步是:

.. code-block:: python

    "Task1": {
        ...
        "Parameters": {
            "JobName": "test",
            "Arguments.$": "$$.Execution.Input.task1"
        },
      ...
    },

其中给 Lambda Function 传递参数时最关键的一步是:

.. code-block:: python

    "Task2": {
        ...
        "Parameters": {
            ...
            "Payload.$": "$$.Execution.Input.task2"
        },
        ...
    }

最终的 Step Function Definition 源码如下:

.. literalinclude:: javascript
   :language: ./definition.json
   :linenos:
