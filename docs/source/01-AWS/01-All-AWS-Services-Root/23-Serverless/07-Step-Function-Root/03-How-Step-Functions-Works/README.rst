How Step Functions Works
==============================================================================
本文是我阅读 `How Step Functions Works <https://docs.aws.amazon.com/step-functions/latest/dg/how-step-functions-works.html>`_ 官方文档的笔记. 基本涵盖了 SFN 的大部分重要知识点.


Standard vs Express Workflows
------------------------------------------------------------------------------
你创建 State Machine 的时候有两个选项, Standard 和 Express. Standard 主要是用于长时间运行的, 也符合 orchestration tool 的本质, 只能被 async execute, 按照 transition 的次数计费. 而 Express 主要用于短时间运行, 用完就走, 相当于是把一些短时间运行的 worker 编排到一起, 可以被 async 或 sync execute, 按照 duration / memory 计费.

它两在这几个指标上有重大区别:

- max duration:
    - standard: 1 year
    - express: 5 min
- execute:
    - standard: async only
    - express: async and sync

Reference:

- Standard vs Express (这里有个对比的表格): https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html
- start_execution: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_execution
- start_sync_execution: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_sync_execution

**Synchronous and Asynchronous Express Workflows**

对于 Express Workflows 有 Sync 和 Async 两种执行模式 (因为它的运行时间上限短嘛).

注意: Standard Workflows 只有 Async 模式, 没有 Sync 模式. 因为它的运行时间可能超级长, 所以不适合提供 Sync 模式. 你硬要这么做的话, 可以用 Poll Job 的模式实现.

**Execution guarantees**

- Standard Workflows: exact once, 当你 Start Execution 的时候, Standard workflow 会保证只被执行一次.
- Express Workflows Async: at least once, 对于 async start execution, 这个 workflow 可能会被调用多次. 因为异步调用的原理就是用一个内部的 Queue (只不过循环速度很快) 来存储你的请求, 如果你的请求失败了, 它会重试. 所以这种情况下的你需要保证你的 Workflow 业务逻辑幂等. (里面的 Task 还是只被调用了一次)
- Express Sync: at most once, 如果是 sync start execution, 那么这个 workflow 要么只被调用一次, 要么直接失败, 这也符合你的逻辑. 所以在你运行 SFN 的代码中, 你自己要保证它运行成功了.

这个对于业务还是很重要的. 因为对于编排来说, 很重要的一个事情就是幂等, 如果不实现幂等, 你发送了多个 API Call 就可能会导致不同的结果.

Reference:

- https://docs.aws.amazon.com/step-functions/latest/dg/express-at-least-once-execution.html

**Cost-optimization using Express Workflows**

如何优化成本呢? 首先我们快速回顾一下 Step Function 的收费模型.

- Standard 由于是长时间运行, 常用于 Async run, 它只按照在 State 之间的 transition (转移) 次数来计费. 也就是说你中键即使 Wait 了很久, Wait 的期间不会被计费. 每转移 1000 次收费 $0.025.
- Express 由于是短时间运行, 常用于 Sync Run, 它只按照 Invoke 的次数, 以及 Duration + Memory (和 Lambda 相似) 来计费. 如果你有 Parallel 和 Map, 会有大量的 Payload, 那么这些 Payload 也会被计费. 每 1M 个 request 收费 $1, 然后按照内存加运行时间这样收费:
    - $0.00001667 per GB-Second ($0.0600 per GB-hour) for the first 1,000 hours GB-hours
    - $0.00000833 per GB-Second ($0.0300 per GB hour) for the next 4,000 hours GB-hours
    - $0.00000456 per GB-Second ($0.01642 per GB-hour) beyond that

我们来看这样一个案例: 你有一个用户下单后的订单处理工作流, 一共有 4 步, 从客户提供的支付划款, 到货物仓库给客户安排发货, 更新库存, 并告知客户已经发货. 每一步都是一个 Lambda Function, 运行时间都是 3 秒.

- 如果你使用 Standard workflow, 你处理 1000 个订单大约需要花费 4 + 2 (start 和 end 也算) 乘以 1000 个 transition 也就是 $0.15 美元.
- 如果你使用 Express workflow, 你大约需要花费 12 秒 * 64 MB (都是远程调用, 内存消耗很小) 乘以 1000 个 invoke, 一共是 12 * 64 * 1000 / 1024 = $0.0125 美元. 再加上 $1 * 1000 / 1000000 = $0.001 的 api request 开销, 以供花费了 $0.0135 美元.

**可以看出来, 如果 State Machine 中的每个 Task 都是短时间运行, 而且基本上都是同步调用 (你需要等它结束), 那么使用 Express Workflow 会比较划算**.

我们再来看一个案例: 你有一个数据处理的工作流, 一共有 2 步. 第一步进行数据处理大约需要运行 3 分钟, 第二步将结果发送给开发者, 这一步速度很快, 跟 3 分钟比起来可以忽略不计. 我们要运行 1000 次. 我们来看看这个案例中两种 Workflow 分别需要花费多少:

- Standard workflow: 以供需要 (2 + 2) * 1000 * 0.025 = $0.1
- Express workflow: 180 * 64 * 1000 / 1024 * 0.00001667 = $0.1875375

**可以看出来, 对于需要异步调用, 然后挂起等待的这种运行模式, 用 Standard Workflow 比较划算**.

根据以上观察, 我们可以得到两个优化成本的原则:

1. 如果一个 workflow 中又有快速解决的同步计算部分, 也有慢慢等待的异步部分 (例如长时间的数据处理, 人工审核等), 那么可以考虑将这个 workflow 拆分成两个, 一个用 Express Workflow, 一个用 Standard Workflow. 然后将 Express Workflow nest 到 Standard Workflow 中.
2. 直接考虑将现有的短时间运行的 workflow 转换成 Express Workflow.

Reference:

- AWS Step Functions Pricing: https://aws.amazon.com/step-functions/pricing/
- Building cost-effective AWS Step Functions workflows: https://aws.amazon.com/blogs/compute/building-cost-effective-aws-step-functions-workflows/


Map state processing modes
------------------------------------------------------------------------------
Map 是用一个数组作为输入, 然后对数组中的每个元素执行相同的操作并且是并行计算. Step Functions 支持两种并行计算模式:

- Inline (默认模式): 每个 sub execution 都是在当前的 workflow 中运行, 当然也分享这个 global context. 而且 sub execution 的 log 也会合并到 parent 中这种模式最多支持 40 个并行计算.
- Distributed (高并发模式): 每个 sub execution 其实是一个 child workflow, 这种模式下每个 child workflow 的 log 都是独立的, 并且可以支持 10,000 个并行计算.

那么该如何选呢? AWS 给出了一个简单的判断依据:

- 用 Inline, 如果: workflow 不超过 25000 个 event 的 quota (所有并发里面的 event 也算在这里), 以及不超过 40 个并发.
- 用 Distributed: 你的 payload 超过了 256KB, 所有并发的 event 加起来超过了 25000 个, 你需要超过 40 个并发.

Reference:

- Map state processing modes: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-map-process-modes.html


Transitions
------------------------------------------------------------------------------


Input and Output Processing in Step Functions
------------------------------------------------------------------------------
Data I/O 可以说是 Step Function 中最复杂的部分了. 但是这种复杂度也带来了更佳的灵活性.

简单来说, 你的每个 State (也就是流程图中的一个节点) 都包含了一个具体的 Task, 这个 Task 就是具体执行运算的那个单元, 例如 Lambda. 当进入一个 State 然后出来的这个过程中, 数据其实是经过了这么几个流程的:

- State Input: 没什么好说的, 就是 State 的总 Input, 通常是上一个 State 的 Output
- Task Input: 就是计算单元接收到的 Input
- Task Output: 就是计算单元返回的 Output
- State Output: 就是 State 的总 Output. 这跟 Result Path, Output Path 有关, 我们后面再说.

然后再这些步骤之间, 还有几个可选步骤:

- State Input: 说过了
- Input Path: 就是将 State Input 的某个 JSON node 作为 Task Input
- Parameters: 通常是一个复杂的 JSON 对象, 可以自己 hard code 一些 key value, 也可以从上一步的 State Input 或是 Input Path 中用 JSON notation 选择数据
- Task Input: 说过了
- Task Output: 说过了
- Result Selector: 和 Parameter 类似, 也是一个复杂的 JSON 对象, 只不过是用来构建 Task Output data 的, 也可以从上一步的 Task Output 中用 JSON notation 选择数据
- Result Path: **非常重要**, 对默认的 Result, 也就是 State Input 进行处理, 语义上是将经过 Result Selector 处理后的 Task Output 插入到指定的 JSON Path 中. 例如 ``"ResultPath": "$"`` 将 Task Output 作为根节点, 也就是用经过 Result Selector 处理后的 Task Output 整体替换掉 State Input. 这也是 Result Path 的默认行为. 你还可以保留原有的 State Input, 只进行部分替换.
- Output Path: 和 Input Path 类似, 只不过是对 Result Path 的返回值进行筛选
- State Output: 说过了

可以看出 Input Path 和 Output Path 是对应的, 都是单节点筛选. 而 Parameters 和 Result Selector 是对应的, 都是复杂的 JSON 对象, 可以进行复杂数据处理. 而 Result Path 则是为了给开发者提供更多的灵活性, 允许将原有的 State Input 以及 Task Output 结合起来进行更复杂的处理而存在的.

**Context Object**

这里还有一个重要的概念就是 Context Object. 这是对于所有的 State 全局可见的一个 JSON 对象. 你可以用 ``$$`` 语法来访问它, 从而用里面的数据来构造你的 Task 的 URI, 也可以用来构造你的 Task 的 Parameter. 它的格式是这样的:

.. code-block:: javascript

    {
        "Execution": {
            "Id": "String",
            "Input": {},
            "Name": "String",
            "RoleArn": "String",
            "StartTime": "Format: ISO 8601"
        },
        "State": {
            "EnteredTime": "Format: ISO 8601",
            "Name": "String",
            "RetryCount": Number
        },
        "StateMachine": {
            "Id": "String",
            "Name": "String"
        },
        "Task": {
            "Token": "String"
        }
    }

**Data flow simulator**

AWS StepFunction 还提供了一个可视化界面来让你 debug input output data handling. 非常好用, 推荐使用.

Reference:

- `Input and Output Processing in Step Functions <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-input-output-filtering.html>`_
- `Context Object <https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html>`_:
- `Data flow simulator <https://docs.aws.amazon.com/step-functions/latest/dg/use-data-flow-simulator.html>`_:
- `Intrinsic Function <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-intrinsic-functions.html>`_: 基于 JSON 的数据处理语言的参考文档.


Orchestrating large-scale parallel workloads in your state machines
------------------------------------------------------------------------------
本节我们来说说用 MAP 进行大规模并行计算时的一些注意事项.

如果你是 Airflow 的用户, 你可能会知道 Airflow 对并行计算是有 ``trigger_rule`` 的概念. 也就是说 Map 之后的一部到底要不要执行是依赖于 Map 并行计算的错误率的, 可以是 ``{ all_success | all_failed | all_done | all_skipped | one_success | one_done | one_failed | none_failed | none_failed_min_one_success | none_skipped | always }`` 中的一个. Step Function 也有类似的机制.

在 Step Function 中有两种机制可以控制 Map 的并行计算是否视为失败:

- Tolerated failure percentage: 最多百分之多少的可以允许失败. 0 就是不允许失败, 100 是允许全部失败.
- Tolerated failure count: 最多多少个 item 可以允许失败.

而对于 Parallel 的并行计算, 你需要自己确保每个 Parallel 的 Task 自己进行了 Cath Error 的处理, 如果不进行处理, 那么任意一个 branch fail 了就会导致整个 branch fail.


Manage continuous deployments with versions and aliases
------------------------------------------------------------------------------
Step Function 作为一个 Serverless 的服务, 它的本质就是 Workflow Definition. 一个简单的 JSON 文件以及相关的配置. 这种轻量化部署的行为就使得对其进行版本管理变得可行. Step Function 的版本管理机制和 Lambda 一摸一样, 都是用 Version 和 Alias 来管理. 我们简单的介绍一下这种机制:

- 每次你更新 Step Function, 它的 Workflow Definition 和配置都被视为 ``$LATEST``.
- 你可以在任何时候用 ``$LATEST`` 的版本创建一个 Snapshot, 这个 Snapshot 就是一个 Version. 这个 Version 是 immutable 的, 并且每次更新后会自动按照 1, 2, 3, ... 递增. 注意, ``$LATEST`` 本也是一个特殊的 Version.
- 而 Alias 只是一个指向单个 Version 或多个 Version 的的指针. 如果是指向多个 Version, 则你需要配置每个 Version 的权重.
- 在开发阶段部署的时候, 都只是更新 ``$LATEST`` 但不创建新版本. 而每次发布新版本时, 则自动创建一个 Version.
- 我们维护一个长期的叫做 ``LIVE`` 的 Alias, 默认指向 production 中的 $LATEST. 如果实在需要回滚, 则我们更改配置文件将 Alias 指向上一个 Version 即可.
- 如果我们需要滚动发布, 那么可以用 ``LIVE`` 的 Alias 将 80% 的流量指向旧版本, 20% 的流量指向新版本. 然后定时查看它的错误率, 如果没有问题则提高新版本的权重.

Reference:

- https://docs.aws.amazon.com/step-functions/latest/dg/concepts-cd-aliasing-versioning.html
