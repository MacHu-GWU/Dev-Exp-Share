Wait for a Callback with the Task Token
==============================================================================
**简介**

这是一种比较高级的用法. 这个 Callback Task Token 主要是为了解决在 Orchestration 的过程中, 有些 Task 并不是 AWS 所管理的服务, 对于这种外部服务的 Async 调用, 你无法让 StepFunction 去 Poll 它们的状态, 因为外部服务不是 AWS 所能管理的范畴. AWS 提供的方法是在调用这些外部 Task 的时候, 发一个 Token 给 Task, 然后 StepFunction 就一直等, 直到它收到这个 Token 才会继续进行下一步. 也就是说你的外部的 Task 需要负责在运行成功或者失败之后, 调用 API 给 StepFunction 提交一个 Token, 然后 StepFunction 才会继续运行 (transit 到下一步). 这种让 Task Executor 主动推送的方式要比让 Scheduler 去轮询的性能要好的多. 不过代价就是你依赖于外部服务的实现, 如果外部服务本身出了问题, 很可能会导致你的 StepFunction 一直等待下去.

补充一点, 其实这本身就是 AWS StepFunction 原生的跟其他 Service Integrate 的方式, 只不过 AWS 封装了一层, 让你感觉不到, 从而提高开发体验罢了.

**在这种 Integration Pattern 下, StepFunction 的行为如下**:

- 你定义了一个 Task, 并且勾选了 "Wait for callback" 的选项. 你还可以定义一个 "HeartbeatSeconds" 来决定多长时间内没有收到 heartbeat 就算超时. 这个 Task 通常是一个 Lambda Function 用来调用一个外部服务. 这个外部服务不需要是 AWS 的产品.
- Step Function 在运行 Workflow 的时候, 就会生成一个 Task Token. 这个 Task Token 在整个运行周期只会生成一次.
- Step Function 运行这个 Task 之后, 不会立刻转移到下一步, 而是等待任何人用 ``send_task_success`` 或者 ``send_task_failure`` API 将这个 Task 的状态更新为成功或者失败. 通常调用 task success / failure API 的人就是外部服务, 例如在结束的地方发送成功, 在异常处理的代码中发送失败. 又或者你的外部服务配套的有一个能查看这个服务运行状态的监控器, 让这个监控器检测到成功或失败的事件后调用这两个 API 也可以.
- 注意上面两个 API 调用者还要负责返回这个 Task Output. 这个 Output 会被 StepFunction 传递给下一个 Task.
- 如果你配置了 "HeartbeatSeconds", 那么你的服务还需要负责每隔一段时间就用 ``send_heartbeat`` 发送这个 token 告诉 StepFunction 我还在运行.

为了方便理解这么做的意义, 我们举一个不用这种模式, 但是能达到类似的目的的例子.

假设我们有一个任务, 是运行一个 AWS Glue 的 ETL Job. 耗时约 1 小时. 那么 AWS 原生可以在运行 ETL Job 之后, 当它成功或失败的时候, 继续下一步骤. 这种模式是为了解决长时间运行的任务的调度和等待问题. 由于 Glue 是原生的 AWS 服务, 你无需使用 Token 就能轻易的直到 Glue 的运行状态.

而如果我们的任务是运行在 On-prem 的 Hadoop Cluster 上的一个 Spark Job 呢? 我们只有一个带权限验证的接口, 可以远程 Submit Spark Job, 但我们并没有实现一个 API 能让 AWS StepFunction 能获得这个 Spark Job 的运行状态. 这时候就必须使用 Callback 的模式了.

那么我们可以用一个 Lambda Function 来远程 Submit Spark Job. 然后 StepFunction 就进入等待, 然后把这个 Task Token 也保存在 Spark Job 能访问的地方. 然后 Spark Job 在运行结束或者出错后, 将这个 Token 通过 ``send_task_success`` 或者 ``send_task_failure`` API 发回给 Step Function, 进行下一步.

可以看出这种模式的优点是几乎可以和任何技术, 在任何地方运行的计算单元 (要有网络), 都能集成到 AWS StepFunction 中.

- `Wait for a Callback with the Task Token <https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token>`_

**具体的例子**

我们用 ``task.py`` 模拟外部服务的调用. 它其实什么外部服务都没有调用, 仅仅是将输入打印出来而已.

.. literalinclude:: ./task.py
   :language: python
   :linenos:

我们再来看 Step Function definition.

.. literalinclude:: ./definition.json
   :language: javascript
   :linenos:

其中最重要的是这两段::

    # 表明了要 wait for task token
    "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",

    # 表明了把普通的 input 和 context 对象都传递给 Lambda function
    "Payload": {
      "input.$": "$",
      "context.$": "$$"
    },

我们创建好 lambda 和 stepfunction 之后点击运行. 可以看到 Task1 的 input 里面就有一个 token. 然后将这个 token 放到下面的代码中运行, 告诉 StepFunction 我们成功了. 下面这段代码就相当于是模拟外部的 Job 运行逻辑.

.. literalinclude:: ./test.py
   :language: python
   :linenos:

**FAQ**

- Q: 如果我有多个 Task 都要都要等待 Callback. 那么这些 Token 是一样的还是不一样的?
- A: 是不一样的. Token 是 Context Object 中的一个 Attribute, 这个 Attribute 每次运行到需要 Callback 的 Task 的时候, Token 的值都会变. 另外 Context Object 是一个可读不可写的对象.
