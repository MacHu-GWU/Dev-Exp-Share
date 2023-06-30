AWS StepFunction Knowledge Graph
==============================================================================



入门篇
------------------------------------------------------------------------------
- 什么是工作流编排系统? 和你直接写一个流程 if else 脚本有什么区别?
- StepFunction 是什么, 不是什么, 能做什么?
- StepFunction 的核心概念, State, Task, Transition, Parallel, Map, Choice, Pass.
- StepFunction State Language 的基本语法.
- StepFunction Visual Editor 的使用.
- 给 StepFunction 合适的权限.


进阶篇
------------------------------------------------------------------------------
- Standard vs Expression 的区别, 何时使用哪种?
- Idempotent 幂等性, 以及在 Expression 模式中 sync 和 async 的 Execution guarantees.
- Step Function Pricing.
- 基本的成本优化策略.
- Input Output data processing. 如何对输入输出数据进行处理.
- Context Object, 如何利用 Context Object 来实现 external data source, pass parameter across tasks 等技巧.
- Map 并行计算的 inline 和 distributive 两种模式的区别, 何时用哪种? 在并行计算时如何处理异常?
- Error Handling.
- Optimized Integration, 使用优化过的那些常用的计算单元, 例如 Lambda, Glue, Batch, StepFunction 等.


高级篇
------------------------------------------------------------------------------
- 使用 Version 和 Alias 来进行持续部署和错误回滚.
- 使用 Poll Job Pattern 来将异步调用变成 "伪同步" 调用.
- 使用 Wait for Task Token 来异步调用外部服务, 并通知 StepFunction 状态.
- AWS SDK Integration.
- 用 VPC Endpoint 来调度位于 VPC 内的资源.
- 用 Assume Role 来实现 cross account access.
- 开发, 测试, 部署的最佳实践.
