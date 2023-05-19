What is Amazon EventBridge
==============================================================================
Keywords: Amazon, AWS, Event, Bridge, EventBridge


背景知识
------------------------------------------------------------------------------


基于事件驱动模型的系统集成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
将多个系统集成到一起是现代软件架构中重要的组成部分. 相比让系统之间直接通信, 用事件驱动模型来集成系统经过多年的生产实践, 被证明是更佳的选择.

为什么系统之间直接通信不是一个好的选择呢?

1. 系统之间直接通信意味着同步(阻塞)调用模型. 这种模式对错误的容忍较差, 对系统性能的影响也较大. 而通过 Event 异步调用能将系统解耦合, 使得各个系统能相对独立的被维护, 一个系统崩掉也不会影响另一个系统, 并且并发量能做更大.
2. 系统之间直接通信意味着 N * N 的复杂度. 而通过中介 Event 则能将系统复杂度降低到 N + N 的级别.
3. 用专门的 Event Bridge 服务来处理系统集成能提高整体的可维护性, 减少了每个系统自己造轮子来调用其他系统的麻烦.


事件驱动模型的本质
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
简单来说事件驱动模型就是: 发生了一个事件, 我们看看要不要对它进行处理, 如果要处理, 要把它送给谁去处理. 这根 Publisher, Subscriber 模型一致. 只不过 Pub/Sub 中来处理数据的人需要自己去 Subscribe. 而事件驱动则是在系统中定义好了谁要来负责处理这个事件.

事件驱动模型本质上就三个组成部分:

- 事件 event: 系统中发生的任何事情都可以是一个时间, 例如任何 AWS API 的调用都是一个事件. 包括 S3 Put Object, CodeCommit Push 等等.
- 规则 rule: 定义了如何处理 event, 例如可以对 event 进行 filter. 只有满足 filter 的 event 才会被处理.
- 目标 target: 这个 event 将会被发送到哪里去进行处理. 例如可以发送到 SNS, SQS, Lambda 等等.

我们来看下面几个例子:

- S3 Put Object:
    - event: 有个文件被上传到了 S3
    - rule: 看看这个文件名的扩展名是不是我们需要关注的
    - target: 如果是, 这个文件发送给 AWS Lambda 去处理
- CodeCommit Git Push:
    - event: 有人 commit 代码到 Git 了
    - rule: 看看这个 commit 所在的 branch 是不是我们需要关注的
    - target: 如果是, 我们来 trigger 一个 build job 来测试这个代码

对事件驱动的系统集成有基本的理解后, 我们来看看 AWS Event Bridge 是什么.


Event Bridge 是什么
------------------------------------------------------------------------------
AWS Event Bridge 是一个于 2019 年发布的服务, 专门用来解决事件驱动的系统集成问题. 虽然这个服务的发布时间是 2019 年, 但是里面的底层技术在 AWS 生产环境从 2014 年就存在了, 是非常成熟的. 经过多年的发展, AWS 意识到事件驱动模型在现代软件架构中是如此的重要, 所以单独将其包装成了一个服务, 并提供了更多高级功能, 将其扩展到能和 AWS 以外的生态集成.

早期 AWS 的日志服务 CloudWatch 就有 CloudWatch event. 以前用 S3 Put Object 或是 SNS 来 trigger Lambda 就是用 CloudWatch even 来处理的. Event Bridge 的底层同样是 CloudWatch event. 只不过它是一个专门的服务, **提供了更好的用户体验, 更丰富的 API, 提供了权限管理, 编排所用的 pipe, 以及允许跟其他厂商的服务进行集成**. 所以在 2019 年之后就推荐全面使用 Event Bridge 了.


Event Bridge 的功能
------------------------------------------------------------------------------
相比早期 CloudWatch event 的简单功能, Event Bridge 还提供了这些功能:

- Event Rule 是对 Event, Rule, Target 概念的封装.
- 提供了一个 Sandbox 工具能帮助你编写高质量的 Event Rule.
- Event 在此之上又有 Event Buses 可以对多个 Rule 进行管理, 并且提供基于 Resource Policy 的权限控制.
- Event Bridge 是 Regional 的服务, 如果你想要跨 Region 进行集成, 又或是需要跨 Region 进行 Event 复制, 又或是需要容灾, 那么 Global Endpoint 可以帮你达成这些.
- Archive 提供了对 Event 进行的存档, 以供 debug, 安全检查, 审计等用途.
- Replay 提供了对 Event 进行重现, 可以重现过去的 Event.
- Pipes 提供了对 Event 进行处理的管道, 允许你用 AWS Lambda 对 Event 进行处理, 例如做 Enrichment.
- Schema Registry 可以允许用户能自定义 Event Schema.
- Partner event sources 可以允许第三方厂商将自己的 Event 集成到 Event Bridge, 例如 GitHub action.


如何学习 Event Bridge
------------------------------------------------------------------------------
使用 Event Bridge 的关键就是学会用 JSON 数据格式来定义 Event 和 Rule.

- `Amazon EventBridge events <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html>`_: 这是一篇官方文档介绍了所有生成的 event 长什么样子, 并且给出了很多例子.
- `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_: 这是一篇官方文档介绍了 Event Pattern 的语法, 以及如何用 Event Pattern 来过滤 event. 里面的重点是 Match 条件判断的语法.
- `Sandbox <https://us-east-1.console.aws.amazon.com/events/home?region=us-east-1#/explore>`_ 是一个 AWS Console 上的工具, 它列出了各种服务生成的 Event 的数据的例子. 还提供了一个编辑器帮助你生成用来过滤事件的 Event Pattern 样本.
- `Amazon EventBridge input transformation <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html>`_: Event Bridge 允许你用 JSON 语法对 Event 进行基本的 Transformation 之后再发送给 Target.
