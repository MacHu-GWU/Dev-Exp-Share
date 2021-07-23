.. _step_function:

Step Function
==============================================================================

Step Function是一种将许多无状态的 Application 组织到一起的中间件. 通过 Amazon State Language (ASL) 自定义你的 workflow, 决定先执行哪个, 后执行哪个, 成功了怎么样继续, 不成功怎么样继续.

- doc: https://aws.amazon.com/documentation/step-functions/
- amazon state language doc: https://states-language.net/spec.html
- Step Function Use Case: https://aws.amazon.com/step-functions/use-cases/
- Orchestrate multiple ETL jobs using AWS Step Functions and AWS Lambda: https://aws.amazon.com/blogs/big-data/orchestrate-multiple-etl-jobs-using-aws-step-functions-and-aws-lambda/

Step Function 能将互相独立的 Lambda Function 组合起来, 组成一个 Workflow. 用 State Machine 管理中间复杂的执行逻辑.


Step Function 在生产中主要用来做什么?
------------------------------------------------------------------------------

Step Function 实际上可以理解为一系列 Lambda Function 组合起来的流程, 相当于一个大型的 Lambda Function. 通常 Step Function 设置完毕后, 我们会创建一个 Lambda Function 来连接这个 Step Function. 每当我们需要执行这个 Workflow 时, 调用对应的这个 Lambda Function 即可.

当你要在 Lambda Function 中调用其他的 Lambda Function 时, 请使用 Step Function.


Step Function 需要的 IAM Role
------------------------------------------------------------------------------

由于 Step Function 本质就是调用一系列的 Lambda Function, 所以只需要 `AWSLambdaRole <https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSLambdaRole$jsonEditor>`_ 即可.
