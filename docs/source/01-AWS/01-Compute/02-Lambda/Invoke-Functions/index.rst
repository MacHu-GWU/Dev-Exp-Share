Invoke Functions
==============================================================================


Invokation Types
------------------------------------------------------------------------------

术语:

- Sync (同步): 发送了请求后, 没收到回复前无法做下面的事.
- Async (异步): 发送了请求后, 就可以做下面的事情了.
- Poll Based (轮询): 隔一段时间检查一下有没有事情要做.

两种 Invoke 类型:

- Request and Response: 通过 AWS CLI 发送 Invoke 请求. 所有的 Request and Response 类型的 Invoke 都是同步的. 也就是说发起请求的客户端在收到回复之前, 无法做下面的事.
- Event Triggered: 通过 Event 触发 Lambda 时, 根据不同的 Event 类型, 亚马逊预先定义了执行是用 Sync 还是 Async.
    - Sync:
        - Elastic Load Balancer
        - Amazon Cognito
        - Amazon Lex
        - Amazon Alexa
        - API Gateway
        - CloudFront
        - Kinesis Data Firehouse
        - Poll-based AWS Service: Kinesis, DynamoDB, SQS.
    - Async:
        - S3
        - Simple Notification Service
        - Simple Email Service
        - CloudFormation
        - Cloudwatch Log
        - Cloudwatch Events
        - Code Commit
        - AWS Config

Reference:

- Invokation Types: https://docs.aws.amazon.com/lambda/latest/dg/invocation-options.html
- Services That Invoke Lambda Functions Synchronously: https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html
- Services That Invoke Lambda Functions Asynchronously: https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html


Retry Behavior
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/lambda/latest/dg/retries-on-errors.html


- Event sources that aren't stream-based:
    - Synchronous invocation: X-Amz-Function-Error, error 200
    - Asynchronous invocation: automatically retry the invocation twice, store failed invokation in dead letter queue
- Poll-based event sources that are stream-based: 由于对于 Poll-based Event, invokation records 是批量进行处理的, 如果1个 record 发生错误, lambda 会继续执行其他的 record, 直到处理完全部 records, 最长持续 7 天.
- Poll-based event sources that are not stream-based: 例如 SQS, 由于 SQS 同样也是一次 Batch 发送多个 records 给 lambda 进行处理, 如果 1 个 record 发生错误, lambda 会立刻返回.

使用 Dead Letter Queue 保存执行失败的 Lambda 函数的信息.

任何 Async (异步) 触发的 Lambda, 默认情况下在失败后会重试两次.

- SQS: put record to SQS
- SNS: public record to topic
