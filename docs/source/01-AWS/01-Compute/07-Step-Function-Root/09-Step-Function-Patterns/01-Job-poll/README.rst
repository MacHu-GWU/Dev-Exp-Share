AWS Step Function Job Poll Pattern
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, Root, Patterns, Job Poll, Async


Summary of the Problem
------------------------------------------------------------------------------
在 Orchestration 中, 经常会有 Async 的 Job, 运行之后你需要等待 Job 完成. 内置的 Widget 有 Job Poll 的模式, 你可以通过拖曳来实现: ``运行 -> 等待 -> 检查状态 -> 等待 -> 检查状态 -> ... -> 超时或者检查到了成功或者失败的状态`` 这种模式. 这种官方推荐的方式有两个问题:

1. 不是所有的 Service 都有 built in 的 Widget 的. 所以更加通用的方法是用 Lambda 来 run job, 同样用 Lambda 来 check status.
2. Job Poll 默认不支持 Timeout, 用整个 State Machine 的 Timeout 来控制也不是个好办法. 因为你一个 State Machine 中可能有多个 Job Poll 的循环, 你无法控制每个循环的 Time Out 时间.


Proposed Solution
------------------------------------------------------------------------------
Overview:

- 一定要用 Standard State Machine, 不要用 Express. 因为很多时间都在等待, 并且可能会超过 Express 5 分钟的限制
- 对 Async Job 的调用要包装在一个 Lambda 中, 这样你有更多的控制权. 这个 Lambda 我们叫做 "Run Job".
- "Run Job" 的 Lambda 的 Payload 不要用默认的 "$", 而要用 "$$",
"$$" 的意思是将整个 Step Function 的 Context 作为 Lambda 的输入, 其中 State Input 是里面的一个 field. Context 中包含了 execution arn, 你可以用 execution arn 作为一个 Key, 将属于这个 execution 的 metadata 写入到外部存储, S3, DynamoDB 都可以, 其中 Key 可以作为 S3 的 uri, 或是 DynamoDB 的 hash key (我们这个例子中用的是 S3), 这样后续的 Task 就可以读到这些 metadata. 这里的关键是这个 Lambda run job 之前, 将 start time 写入到 S3, 这样后面的 "Get Job Status" Lambda 就可以用这个 start time 作为一个 timeout 的依据.
- 然后就是用 Step Function 里面的 Job Poller 的 Pattern, 不过 "Get Job Status" 的步骤是一个 Lambda, 这个 Lambda 要干两件事: 一是从 S3 读 Metadata 确认是否 Timeout, 二是查询 Job Status 如果成功或失败就返回代表成功或失败的值, 如果都不是就返回一个默认值, 例如 "running".
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
