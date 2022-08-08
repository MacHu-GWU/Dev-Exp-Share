AWS Step Function - Quick Start
==============================================================================


Concept
------------------------------------------------------------------------------
学一门新技术最重要的就是了解其中的概念.

- Action: 一个具体的计算动作, 比如 "运行一个 Lambda Function", "发送一条消息到 SNS Topic" 这些都是 Action, 每个 Action 有它自己的 Input Output 的接口数据模型.
- State: 一个状态, 是对一个 Action 的封装. 也是编排的最小单位. State 本身也有 Input Output, 而 State Input/Output 和 Action Input/Output 之间是可以进行一些简单的数据处理的.
- Transition: 从一个状态转移到另一个状态
- Workflow: 将所有的 State 用 Transition 组织到一起的一个图, 有一个确定的开始, 以及多个结束. 也是我们编排的重点.
- State Machine: 一个 AWS StepFunction Console 中的 Resource, 里面包含了 Workflow Definition, IAM Role, Tag 等等. 是对 Workflow 的一个封装. 你可以 Execute State Machine, 并用图形化界面查看执行状态和结果.

.. image:: ./workflow.png

Amazon State Language
------------------------------------------------------------------------------
然后我们就可以开始学习 ASL 这门基于 JSON 的语言, 学习如何精准的定义一个 Workflow.

以下两个文档包含了基本上所有需要的资料.

- https://states-language.net/spec.html
- https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html


