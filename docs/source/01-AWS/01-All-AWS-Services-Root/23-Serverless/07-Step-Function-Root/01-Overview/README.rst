.. _aws-sfn-overview:

AWS Step Function Overview
==============================================================================


关于编排系统
------------------------------------------------------------------------------
由于 AWS Step Function 是一个工作流编排系统, 如果你没有接触过其他的编排系统, 例如 Airflow, 我推荐先阅读 :ref:`what-is-workflow-orchestration` 这篇文章了解什么是编排系统.


什么是 AWS Step Function
------------------------------------------------------------------------------
如果你知道业内自动化流程编排的事实开源标准 `Airflow <https://airflow.apache.org/>`_, 那么你就可以把 Step Function (简写为 SFN) 理解为一个无需部署服务器, 低代码, 全托管的 Airflow. 另外 SFN 支持 pay as you go 按用量付费的模式, 不像 Airflow 服务器只要开着就要为服务器付费, 而且你不可能说把服务器频繁关闭启动, 所以对于学习开发也非常友好.

Step Function 是一种将许多 Computation 组织到一起的中间件. 通过 Amazon State Language (ASL) 自定义你的 workflow, 决定先执行哪个, 后执行哪个, 什么时候分叉, 什么时候聚合, 根据不同的条件进行不同的操作, 成功了怎么样继续, 不成功怎么样继续. 这种操作在业内叫做 **Workflow Orchestration, 工作流编排**, 也可以简称 **WF**.


AWS Step Function 的发布历史
------------------------------------------------------------------------------
这里我们列出了 SFN 的发布历史和重要更新, 很多 feature 你现在可能还不知道是做什么的, 我们暂时不做解释. 简单来说, 到我写下这篇文章的时候 2023 年 6 月底, SFN 已经是一个非常成熟的产品了, 并且跟其他同类产品起来要优秀很多, 非常适合在生产环境中使用.

- SFN 是 2016 年 12 月第一次发布的, 比 2015 年 6 月的 Airflow 晚了 1 年多.
- 最初 Step Function 可编排的对象只有 AWS Lambda, 而把所有的业务逻辑都放在 AWS Lambda 中运行.
- 最初 SFN 的代码是用 JSON 写的 Amazon State Language, 手写起来很不方便.
- 2019 年 5 月发布了 Callback pattern, 使得它对任何的外部系统, 甚至是 On prem 的系统进行编排. 这使得各种 Human in the loop 变得可能.
- 2019 年 12 月发布了 Express Workflow, 使得对于耗时短, 没有异步调用的工作流的花费大大降低, 提高了更高的性价比以及更灵活的使用方式.
- 2021 年 7 月发布了 Visual Editor, 可以用拖曳的方式把各种 Computation Resource 拖到流程里, 然后稍微调整一下参数, 就可以完成一个 Workflow 了. 它彻底变成了一个 Low Code 的服务, 算是杀手级更新.
- 2022 年 4 月开始, 它原生支持几乎所有的 AWS API 调用. 极大的提高了开发体验.
- 2022 年 12 月开始, 它支持大型并发 (10000 个 Map 并发), 提高了 Distributive type Map, 扩展了它的应用场景.
- 2023 年 6 月开始, 它原生支持 Version, Alias. 使得版本更新, 蓝绿发布, 灰度发布, 出错回滚等运维操作变得极为简单.

我认为到 2023 年 6 月起, AWS Step Function 可以算得上是一个非常成熟的产品. 如果你的 Task 主要是在 AWS 上, 那么 Step Function 有非常多 Airflow 不具备的能力. 例如 Visual Editor 低代码, 超高并发, 原生 AWS API 调用, 以及 Version Alias 滚动发布. 我认为用 Step Function 要远远好于用 Airflow.


Step Function 在生产中主要用来做什么?
------------------------------------------------------------------------------
在实际生产环境里, 我们可能有非常多独立的工作单元, 他们之间有的有联系, 有的没有直接联系. 如果我们要把这些单元串起来工作, 那么必然涉及单元之间的通信, 状态管理. 在软件工程里我们总是要避免系统的高耦合. 我们当然可以在各个单元里的代码中写好, 这个单元的逻辑执行完了然后就通知下一个单元继续做事情, 但这样会导致各个子系统耦合严重, 无法扩展. 一个地方错, 全部错. 通常业内会使用消息队列或通知服务, 一个任务完了就推送一条 message, 然后触发下一个任务. 但是这样仅仅适合两个系统之间的连接逻辑非常确定, 这样你才能根据这个逻辑实现特定的 读 写 message 的代码. 还是不够优雅.

AWS Step Function 则是一个自动化流程编排服务, 能帮你管理多个系统之间的串联. 本质上多个系统之间不直接通信, 而是由 Step Function 来检测上一个单元的输出, 进行简单处理, 然后把输入传递给下一个单元. 这样就实现了多系统的协同和解耦. 开发者可以专注于实现各个子系统的逻辑, 而把需求复杂而又多变的编排交给 Step Function.


Step Function 的开发体验
------------------------------------------------------------------------------
Step Function 使用的是由 Amazon 开发的 `Amazon State Language (ASL) <https://states-language.net/spec.html>`_ 来定义 Workflow Orchestration 的. 简单来说 ASL 是一种基于 JSON 的 DSL (Domain Specific Language), 为特定领域专门设计的语言. 这就像一个有限状态机, 里面定义了很多 **tate (状态)**, 一个 State 通常对应着一个实际的 Task, 可能是基于各种 Computation Resource 的计算, 例如在 EC2 中计算, 用 AWS Lambda 计算, 用 ECS Task 启动容器计算, 用 AWS Batch 启动容器计算. 然后有了这些 State, 我们就可以定义 **Transition (转移)**, 在什么时候, 什么条件下, 以什么方式进行 **状态转移**. 这里面就涉及: 串行, 并行, 条件分叉, 映射, 等等 Workflow 中的常用概念.

从开发者的角度来说, 你定义 Workflow Orchestration 的工作本身就是写 JSON, 在 JSON 里定义一个个的 State, 然后定义各种 Transition, 然后将对 Task 的调用封装为 Resource + Parameter 的形式, 然后在 AWS Console 里创建一个 State Machine, 就可以开始运行了. 当然写过 DSL 的人都知道学习一门新的特定领域语言的成本并不低, 由于是小众领域, 开发工具也不完善. 所以 AWS 提供了一个 Workflow Visual Editor 的图形化工具, 用户只需要用拖曳的方式吧控件拖到流程里, 然后稍微调整一下参数, 就可以完成一个 Workflow 了. 两者结合起来, 用 Visual Editor 来快速搭建代码胚子, 然后进行细微调试, 最后将其参数化放到代码库中. 我认为这种开发体验相当好, 利用上了低代码的直观, 也利用上了代码的可维护性.


参考资料
------------------------------------------------------------------------------
- AWS Step Function Doc: https://aws.amazon.com/documentation/step-functions/
- Amazon State Language doc: https://states-language.net/spec.html
- Step Function Use Case: https://aws.amazon.com/step-functions/use-cases/
- Orchestrate multiple ETL jobs using AWS Step Functions and AWS Lambda: https://aws.amazon.com/blogs/big-data/orchestrate-multiple-etl-jobs-using-aws-step-functions-and-aws-lambda/
