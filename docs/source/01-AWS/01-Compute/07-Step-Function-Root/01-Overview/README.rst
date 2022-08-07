AWS Step Function Overview
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


什么是 AWS Step Function
------------------------------------------------------------------------------
如果你知道业内自动化流程编排的事实开源标准 `Airflow <https://airflow.apache.org/>`_, 那么你就可以把 Step Function 理解为一个无需部署服务器, 低代码, 全托管的 AirFlow.

Step Function 是一种将许多 Computation 组织到一起的中间件. 通过 Amazon State Language (ASL) 自定义你的 workflow, 决定先执行哪个, 后执行哪个, 什么时候分叉, 什么时候聚合, 根据不同的条件进行不同的操作, 成功了怎么样继续, 不成功怎么样继续. 这种操作在业内叫做 **Workflow Orchestration**, 工作流编排, 也可以简称 **Orchestration**.

最初 Step Function 完全是围绕 AWS Lambda Function 构建的, 但后来已经能够支持几乎所有的 AWS 的服务了.

- doc: https://aws.amazon.com/documentation/step-functions/
- amazon state language doc: https://states-language.net/spec.html
- Step Function Use Case: https://aws.amazon.com/step-functions/use-cases/
- Orchestrate multiple ETL jobs using AWS Step Functions and AWS Lambda: https://aws.amazon.com/blogs/big-data/orchestrate-multiple-etl-jobs-using-aws-step-functions-and-aws-lambda/


Step Function 在生产中主要用来做什么?
------------------------------------------------------------------------------
在实际生产环境里, 我们可能有非常多独立的工作单元, 他们之间有的有联系, 有的没有直接联系. 如果我们要把这些单元串起来工作, 那么必然涉及单元之间的通信, 状态管理. 在软件工程里我们总是要避免系统的高耦合. 我们当然可以在各个单元里的代码中写好, 这个单元的逻辑执行完了然后就通知下一个单元继续做事情, 但这样会导致各个子系统耦合严重, 无法扩展. 一个地方错, 全部错. 通常业内会使用消息队列或通知服务, 一个任务完了就推送一条 message, 然后触发下一个任务. 但是这样仅仅适合两个系统之间的连接逻辑非常确定, 这样你才能根据这个逻辑实现特定的 读 写 message 的代码. 还是不够优雅.

AWS Step Function 则是一个自动化流程编排服务, 能帮你管理多个系统之间的串联. 本质上多个系统之间不直接通信, 而是由 Step Function 来检测上一个单元的输出, 进行简单处理, 然后把输入传递给下一个单元. 这样就实现了多系统的协同和解耦. 开发者可以专注于实现各个子系统的逻辑, 而把需求复杂而又多变的编排交给 Step Function.


从用户的角度来看如何使用 Step Function
------------------------------------------------------------------------------
Step Function 使用的是由 Amazon 开发的 `Amazon State Language (ASL) <https://states-language.net/spec.html>`_ 来定义 Workflow Orchestration 的. 简单来说 ASL 是一种基于 JSON 的 DSL (Domain Specific Language), 为特定领域专门设计的语言. 这就像一个有限状态机, 里面定义了很多 **tate (状态)**, 一个 State 通常对应着一个实际的 Task, 可能是基于各种 Computation Resource 的计算, 例如在 EC2 中计算, 用 AWS Lambda 计算, 用 ECS Task 启动容器计算, 用 AWS Batch 启动容器计算. 然后有了这些 State, 我们就可以定义 **Transition (转移)**, 在什么时候, 什么条件下, 以什么方式进行 **状态转移**. 这里面就涉及: 串行, 并行, 条件分叉, 映射, 等等 Workflow 中的常用概念.

从用户的角度来说, 你定义 Workflow Orchestration 的工作本身就是写 JSON, 在 JSON 里定义一个个的 State, 然后定义各种 Transition, 然后在 AWS Console 里创建一个 State Machine, 就可以开始运行了.

当然写过 DSL 的人都知道学习一门新的特定领域语言的成本并不低, 由于是小众领域, 开发工具也不完善. 所以 AWS 提供了一个 Workflow Visual Editor 的图形化工具, 用户只需要用拖曳的方式吧控件拖到流程里, 然后稍微调整一下参数, 就可以完成一个 Workflow 了.


参考资料
------------------------------------------------------------------------------
