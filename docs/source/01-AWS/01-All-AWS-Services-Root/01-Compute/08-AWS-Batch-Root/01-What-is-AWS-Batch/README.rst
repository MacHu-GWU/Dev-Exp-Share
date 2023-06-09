.. _what-is-aws-batch:

What is AWS Batch
==============================================================================
Keywords: What is AWS Batch, Basic, Tutorial.


1. What is AWS Batch
------------------------------------------------------------------------------
AWS Batch 是为了解决一次性调用大量计算资源而存在的. 传统做法是你要配置好 EC2 集群, 然后定义 Job, 然后将 Job 分发到 EC2 上运行. 你需要管理运算资源, 并且分发 Job, 监控 Job 的运行状态. 有很多个 Job 的时候你还要进行调度. 运算资源不够了还要增加新的 EC2, 没有 Job 需求的时候还要减少 EC2. 可以想象即使是在云上进行计算, 这些事情也是很麻烦的.

AWS Batch 则是将这些步骤抽象化了, 并且由 AWS 对计算资源进行统一调度管理. 你只要定义好你的计算所用的 container image, 并且配置好 job definition, 设置好调度优先级策略, 所使用的 CPU 内存大小, 然后直接用 Submit Job 让 AWS Batch 运行即可. 而对计算本身的编排可以用 AWS Step Functions, 一款全托管, 无服务器的编排服务来实现.

总结下来 AWS Batch 解决了用户的如下痛点:

- 用 Fargate 平台运行你的容器, 免除了管理基础设施的麻烦, 帮你弹性伸缩自动扩容. 还提供了 Spot 的选项, 大大降低了你的计算成本.
- 用 Job Queue 来对 Job 的优先级进行调度, 免除了你自己实现 Message Queue 调度器, 可用资源管理器的麻烦.
- 用 Compute Environment 对计算资源进行管理, 避免了无限制的启动太多的计算资源而导致浪费, 还提供了按照业务优先级来预留计算资源的功能, 对计算资源进行更好的控制.
- 用 Job Definition 对你的计划任务进行抽象和版本管理. 免除了自行维护 Metadata 的运维麻烦.


2. AWS Lambda vs AWS Batch vs ECS
------------------------------------------------------------------------------
**Lambda** 是一个非常流行的, 知名度比 Batch 更高, 同样基于容器, 甚至无需管理容器, 只需要管理代码的无服务器计算服务. 那么 Batch 和 Lambda 有什么区别呢? 什么情况下用哪个呢?

对于很多应用场景, Lambda 都能满足. 而以下场景则是 Lambda 无法做到而 AWS Batch 可以完美解决的:

- 单次计算超过了 Lambda 的 15 分钟限制或 10 GB 内存限制.
- 运行环境的配置比较复杂, 不仅仅是一个编程语言, 你需要自定义很多依赖, 例如复杂的 ML 依赖. Batch 允许你自己用任何镜像构建 container image, 而 Lambda 并不适合用任何基础镜像来构建运行环境 (虽然也可以, 但是比较麻烦, 要为了 Lambda 再包装一层).

那什么场景式不适合用 Batch 而适合用 Lambda:

- 对响应时间有要求, 例如 1 秒内返回结果. Batch 虽然运行时间可以只有 1 秒, 但是还有调度的时间成本. Batch 所支持的最小 Timeout 是 60 秒.
- 计算时间不长不短, 位于 1 分钟到 15 分钟之间, 但是非常高频且碎片化.

**ECS** 是 AWS 容器服务的基础设施, 是一个全托管的容器服务, 让你无需管理基础设施, 只需要专注于你的容器代码本身就可以进行计算的服务. 它也是 Batch 底层的基础架构. 可以说凡是 Batch 能做到的 ECS 也一定能做到. 但是配置 ECS 本身要比配置 Batch 稍微麻烦一些, 因为你要自己实现计算资源的管理和任务调度. 那么什么时候要用 ECS 而不是 Batch 呢?

- 运算时间超过 14 天, 例如 Web 服务器.
- 要以容器集群化的方式运行, 例如 3 个不同的容器为一组, 一个作为代理, 一个作为应用, 一个作为数据处理.


3. AWS Batch Concept
------------------------------------------------------------------------------
现在我们对 AWS Batch 有一个宏观的认识了, 可以开始深入了解它的概念了.

- **Compute Environment** (CE): 你的运行环境. 目前支持 Fargate, Fargate Spot, On Demand EC2, Spot EC2 四种. 可以选择让 AWS Manage Scale 还是你自己 Manage. 最大的能承载的 vCPU 数量是多少, 然后就是一些 VPC 的设置. 本质上这就是一个由 AWS 管理的算力池. 创建 CE 本身完全免费, 且它不是按照最大算力上限收费, 而是按照实际使用的算力收费. 对于允许计算到一半出错的负载你还能用 Fargate Spot capacity 来减少最多 70% 的费用.
- **Job Queue** (JQ): 一个 FIFO Queue (2021 年 9 月 引入了 fair-share scheduling policies, 我们暂时先不管这种). 每个 Queue 有自己的 Priority. 一个 Queue 可以关联 1-3 个 Computer Environment. 这里的 Priority 的意思是, 如果有三个 JQ 都关联了同一个 CE 并且在抢占上面的资源, AWS 会让优先级更高的 JQ 先运行.
- **Job Definition**: 定义你的 Job, 是 Job 的 Metadata.
    - 有 Single node 和 Multi node parallel 两种模式. 这两个都是基于 EC2 的而不是基于容器的. 其中后者常用于大规模并行 GPU 计算, 例如训练大型 ML 模型.
    - Platform 计算平台, 有 Fargate 和 EC2 两种. 在 99% 的情况下 AWS 都推荐 Fargate.
    - Job Configuration 包含就是具体运行的命令, 也就是你在本地运行容器的 ``docker run ${COMMAND}`` 中的 ``${COMMAND}`` 命令部分. 它还支持将命令参数化, 以及定义环境变量.
    - Parameter, 你运行 Job 时的参数.
    - Environment Variable, 环境变量.
    - CPU 和 Memory 的大小.
    - Retry setting, 重试多少次.
    - Revision: 每次修改 Job Definition 都会增加一个 Revision, 也就是说 Job Definition 是 immutable 的, 自带版本控制.
    - Tag: 你可以给每个 Revision 打上不同的 Tag.
- **Submit Job**: 一个根据 Job Definition 启动的, 真正运行的 Job 实例, 有着自己独特的 ID..


4. How does AWS Batch Work
------------------------------------------------------------------------------
这里我们用一个架构图来说明 AWS Batch 的工作原理.

.. raw:: html
    :file: How-does-AWS-Batch-Work.drawio.html


5. Job Queue Scheduling Logic
------------------------------------------------------------------------------
本节我们彻底搞清楚 Job Queue 是如何调度的. 特别是在资源紧张, 而很多个 Queue 里面都有很多个 Job 需要计算的情况.

首先我们来回顾一下创建 Job Queue 时的一些参数:

- Priority: 当一个 Compute Environment 跟多个 Job Queue 关联的时候, Priority 高的 Queue 会先被处理.
- Scheduling policy (SP): 当一个 Job Queue 没有 Scheduling policy 的时候, 它会按照 FIFO (先进先出) 的顺序处理. Scheduling policy 的情况我们之后再讨论.
- Compute Environment: 每个 Job Queue 要跟多个 Compute Environment 关联. 这些 Compute Environment 是有顺序的. 当 Job Queue 中的 Job 被判定为当前最高优先级需要下一个执行的时候, 那么按照顺序看每个 CE 是否有足够的计算资源.

这里我们不考虑 Scheduling policy. 来看一个例子:

有 2 个 JQ, 和 2 个 CE. JQ1 的优先级高于 JQ2, CE1 是 Fargate, CE2 是 Fargate Spot. JQ1 绑定计算环境顺序是 CE1, CE2, 因为它比较重要. 而 JQ2 绑定的计算环境顺序是 CE2, CE1, 因为它允许被打断.

从 AWS 调度的角度来看, 它的调度逻辑是这样的:

1. 扫描每个 JQ 里的最新 Job. 按照顺序检查可用的 CE. 例如 JQ1 里的 Job 的检查顺序是 CE1, CE2.
2. 然后检查每个 CE1 是不是有足够的资源来运行 Job, 如果不是那么就检查 CE2.
3. 如果有资源, 那么检查这个 CE 是不是还绑定了其他的 JQ, 如果其他的 JQ 有没有比当前的 JQ 的优先级高的, 如果有, 它们有没有 Job 在等待, 如果有, 那么这个 Job 就暂时等一等. 反之则运行它.

Reference:

- `Job queue parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_queue_parameters.html>`_


6. Scheduling Policies
------------------------------------------------------------------------------
我们先来看看 SP 技术产生的背景. 在企业中, 通常会统一管理 Compute Environment 和 Job Queue, 维护一个同意的计算池和调度队列. 而默认情况下的 FIFO queue 只能做到先进先出. 属于不同业务线, 优先级相同的 Job 都在同一个 queue 里排队 (通常情况下不会创建多个 Priority 相同的 Job Queue, 因为这样没有意义). 举例来说, 如果业务 A 连续进来 10 个需要很长时间的 Job, 然后业务 B 也进来了 10 个短时间的任务. 那么 A 的任务就会长时间的 Block 业务 B. 虽然两者的优先级都相同, 但是这样显然不公平 (不 Fair). 而这个问题不是 FIFO queue 能解决的.

在此背景下 AWS 发布了 SP 的功能. 它的本质就是允许给一个 JQ 绑定一个 SP. SP 中定义了很多个业务线的 Identifier, 以及它们所占用的可用资源比例 (可用资源是指一个 CE 池子里剩下的, 没有被占用的部分), 以及它们的权重. 在前面的例子里, 如果几个业务的资源比例和权重一致, 那么就会 A 的第一个任务先跑, 然后 B 的第一个任务跟着跑, 然后 A2, B2, A3, B3, ... 这样比较公平 (Fair Sharing Scheduling - FSS).

Reference:

- `Scheduling Policies <https://docs.aws.amazon.com/batch/latest/userguide/scheduling-policies.html>`_: 官方文档
- `Introducing fair-share scheduling for AWS Batch <https://aws.amazon.com/blogs/hpc/introducing-fair-share-scheduling-for-aws-batch/>`_: 一篇用动图解释的非常好的官方博客.


7. Summary
------------------------------------------------------------------------------
现在我们对 AWS Batch 已经有了比较详细的了解了. 下一步我推荐实际上手操作一个项目.
