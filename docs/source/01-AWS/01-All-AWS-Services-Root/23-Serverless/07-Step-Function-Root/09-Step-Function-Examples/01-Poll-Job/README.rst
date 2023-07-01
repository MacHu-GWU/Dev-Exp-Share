AWS Step Function Poll Job Pattern
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, Root, Patterns, Poll Job, Async


Summary of the Problem
------------------------------------------------------------------------------
在 Orchestration 中, 经常会有需要 Async 运行一个 Job, 运行之后你需要等待 Job 完成才能进行下一步. 对于支持 `Optimized integrations <https://docs.aws.amazon.com/step-functions/latest/dg/connect-supported-services.html>`_ 模式的服务, 例如 AWS Lambda, Batch, Glue, SageMaker, CodeBuild, Step Function 等服务, 原生就支持 Sync 调用 (等这些 Job 完成后才会进行下一步, 但实际上是异步调用, 等待时间并不收费). 你只需要点击 Workflow Studio 中的一个按钮即可.

官方推荐使用内置的 Widget 有 Poll Job 的模式, 你可以通过拖曳来实现: ``运行 -> 等待 (Wait) -> 检查状态 (Get Job Status) -> 等待 -> 检查状态 (check) -> ... -> 超时或者检查到了成功或者失败的状态``. 不过官方并没有对下面这两个问题做出解释, 我来补充一下:

1. 不是所有的 Service 都有 check status 这种 built in 的 Widget 的. 所以更加通用的方法是用 Lambda 来 run job, 同样用 Lambda 来 check status.
2. Poll Job 默认不支持子循环级的 Timeout, 用整个 State Machine 的 Timeout 来控制也不是个好办法. 因为你一个 State Machine 中可能有多个 Poll Job 的循环, 你无法精确控制每个循环的 Time Out 时间. 这里有两种解决方案:
    1. 在 Wait 的 State 中我们给他一个参数叫 Wait Count. 然后在将这个参数在整个 Wait 的 Loop 中传递, 每运行一次 Get Job Status Task 就将其加 1, 并且传递给 Choice. Choice 每次先检查 Status, 如果还是 in progress 则继续检查 Wait Count, 超过了指定上线则报错. 例如你的 Wait Count 是 10, 而 wait time 是 6, 那么就是 1 分钟后报错.
    2. 在 Get Job Status Task 中用 Lambda, 然后让 Lambda 来调用 API 检查 Status, 并且利用 execution id 来生成一个唯一的 Key, 然后将第一次 get job status 的时间写入到用 Key 决定的外部存储中, 并且每次都跟这个事件比较, 如果超时了就直接 raise error 即可. 这个外部存储可以是 Dynamodb 也可以是 S3.

1 比较好, 但是实现起来没有那么直观. 而 2 比较直观, 但是实现起来稍微麻烦点. 我没有强烈的偏好, 两者都行.


Proposed Solution
------------------------------------------------------------------------------
本例中我们实现了 #2 中的解决方案.

Overview:

- 一定要用 Standard State Machine, 不要用 Express. 因为很多时间都在等待, 并且可能会超过 Express 5 分钟的限制
- 对 Async Job 的调用要包装在一个 Lambda 中, 这样你有更多的控制权. 这个 Lambda 我们叫做 "Run Job".
- "Run Job" 的 Lambda 的 Payload 不要用默认的 "$", 而要用 "$$", "$$" 的意思是将整个 Step Function 的 Context 作为 Lambda 的输入, 其中 State Input 是里面的一个 field. Context 中包含了 execution arn, 你可以用 execution arn 作为一个 Key, 将属于这个 execution 的 metadata 写入到外部存储, S3, DynamoDB 都可以, 其中 Key 可以作为 S3 的 uri, 或是 DynamoDB 的 hash key (我们这个例子中用的是 S3), 这样后续的 Task 就可以读到这些 metadata. 这里的关键是这个 Lambda run job 之前, 将 start time 写入到 S3, 这样后面的 "Get Job Status" Lambda 就可以用这个 start time 作为一个 timeout 的依据.
- 然后就是用 Step Function 里面的 Poll Jober 的 Pattern, 不过 "Get Job Status" 的步骤是一个 Lambda, 这个 Lambda 要干两件事: 一是从 S3 读 Metadata 确认是否 Timeout, 二是查询 Job Status 如果成功或失败就返回代表成功或失败的值, 如果都不是就返回一个默认值, 例如 "running".
- 然后就用 Choice State 来判断, 如果不是成功或失败就回到 Wait.
- 这里的 Wait 的间隔挺重要的, 因为 Standard State Machine 是按照 Transition 收费的, 所以你需要尽量减少 Transition 的次数. 比如你的 Job 需要至少 15 分钟, 至多 30 分钟 完成, 那么你需要在 Start Job 之后直接放一个 Wait 15 分钟, 然后每次循环的 Wait 则是 1 分钟. 我见过很多人不加思考的在循环中每 1 秒 Check 一次 Job Status, 这样非常浪费钱.

``sfn_pattern_job_poll_0_job_runner.py``:

.. literalinclude:: ./sfn_pattern_job_poll_0_job_runner.py
   :language: python

``sfn_pattern_job_poll_1_run_job.py``:

.. literalinclude:: ./sfn_pattern_job_poll_1_run_job.py
   :language: python

``sfn_pattern_job_poll_2_check_status.py``:

.. literalinclude:: ./sfn_pattern_job_poll_2_check_status.py
   :language: python

``definition.json``:

.. literalinclude:: ./definition.json
   :language: json
