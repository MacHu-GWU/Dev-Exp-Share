.. _aws-batch-root:

AWS Batch Root
==============================================================================
Keywords: AWS

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is AWS Batch
------------------------------------------------------------------------------
AWS Batch 是为了解决一次性调用大量计算资源而存在的. 传统做法是你要配置好 EC2 集群, 然后定义 Job, 然后将 Job 分发到 EC2 上运行. 你需要管理运算资源, 并且分发 Job, 监控 Job 的运行状态. 有很多个 Job 的时候你还要进行调度. 运算资源不够了还要增加新的 EC2, 没有 Job 需求的时候还要减少 EC2. 可以想象即使是在云上进行计算, 这些事情也是很麻烦的.

AWS Batch 则是将这些步骤抽象化了, 并且由 AWS 对计算资源进行统一调度管理. 你只要定义好你的计算所用的 container image, 并且配置好 job definition, 设置好调度优先级策略, 所使用的 CPU 内存大小, 然后直接用 Submit Job 让 AWS Batch 运行即可.


AWS Lambda vs AWS Batch
------------------------------------------------------------------------------
对于很多应用场景, 同样基于容器, 甚至无需管理容器, 只需要管理代码的 AWS Lambda 就能满足. 而以下场景则需要使用 AWS Batch:

- 单次计算超过了 Lambda 的 15 分钟限制或 10 GB 内存限制.
- 运行环境的配置比较复杂, 不仅仅是一个编程语言, 你需要自定义很多依赖. Batch 允许你自己用任何镜像构建 container image, 而 Lambda 并不适合用任何基础镜像来构建运行环境 (虽然也可以).


AWS Batch Concept
------------------------------------------------------------------------------
- Compute Environment: 你的运行环境. 目前支持 Fargate, Fargate Spot, On Demand EC2, Spot EC2 四种. 可以选择让 AWS Manage Scale 还是你自己 Manage. 最大的能承载的 vCPU 数量是多少, 然后就是一些 VPC 的设置. 本质上这就是一个由 AWS 管理的算力池, 并且不是按照最大算力上限收费, 而是按照实际使用的算力收费. 对于允许计算到一半出错的负载你还能用 Fargate Spot capacity 来减少最多 70% 的费用.
- Job Queue: 一个 FIFO Queue (2021 年 9 月 引入了 fair-share Queue, 我们暂时先不管这种). 每个 Queue 有自己的 Priority. 一个 Queue 可以关联 1-3 个 Computer Environment. 这里的 Priority 的意思是, AWS 会自动调度所有被 submit 到 Queue 里的 Job. 我们算有 3 个 Queue 好了, 这时有 3 个 Job 在 Queue 的末端准备被计算, 这时 AWS 就会自动给优先级最高的 Queue 里的 Job 分配计算资源.
- Job Definition: 定义你的 Job, 是 Job 的 Metadata.
    - 有 Single node 和 Multi node parallel 两种模式
    - Platform 计算平台, 有 Fargate 和 EC2 两种
    - Job Configuration 就是具体运行的命令, 就是一个 bash 命令而已
    - CPU 和 Memory
    - Retry setting
    - Parameter, 你运行 Job 时的参数
    - Environment Variable 环境变量
- Job: 一个根据 Job Definition 启动的, 真正运行的 Job 实例.


How does AWS Batch Work
------------------------------------------------------------------------------
.. raw:: html
    :file: How-does-AWS-Batch-Work.drawio.html
