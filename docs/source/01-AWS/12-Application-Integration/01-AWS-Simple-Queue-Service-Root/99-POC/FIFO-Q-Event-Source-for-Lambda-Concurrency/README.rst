Strict Order FIFO Q working with Lambda
==============================================================================

用普通的 Q + AWS Lambda 来延时处理大量数据是一个非常好的设计模式. 可以有效的应对数据流量波动很大的应用场景, AWS Lambda 能很好的 Scale Up and Down.

但是有些业务的数据被处理的顺序必须和产生的数据的顺序保持严格一致, 比如数据库的增删插改的 Message. 这时候 FIFO Q 是如何保持并发多个 Lambda, 同时保证顺序严格一致呢? 并且在出错时候能够检测到错误?


理解机制
------------------------------------------------------------------------------

机制部分的分析和结论主要来源于下列 AWS Blog 文章:

- New for AWS Lambda – SQS FIFO as an event source: https://aws.amazon.com/blogs/compute/new-for-aws-lambda-sqs-fifo-as-an-event-source/

**1. Q trigger Lambda 的行为是如何运作的**

Q 和 Lambda 的是由 Event Source Mapping 连接起来的. 不同于直接调用 Q 的 receive_messages API 一次最多只能处理 10 条 message, Event Source Mapping 可以一次处理比这多得多的数据. 具体实现是通过 Buffer. 你可以设定 Batch Size 也就是一次 trigger 包含的 Message 的数量, 和 Batch Window, 也就是时间长度. 例如 size = 100, window = 1 min. 也就是说如果到 1 分钟了, 即使还没有满 100 条消息也立刻触发 Lambda. 又或是到了 100 条数据, 即使还没有满 1 分钟也立刻触发 Lambda. 根据官方文档 https://aws.amazon.com/about-aws/whats-new/2020/11/aws-lambda-now-supports-batch-windows-of-up-to-5-minutes-for-functions/#:~:text=Lambda%20will%20wait%20for%20up,of%20up%20to%2010%2C000%20messages. Batch 的上限是 10000 条消息 和 5 分钟. 而这期间的所有消息的数据大小是收到 Lambda Payload 的限制的. 根据官方文档 https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html, 同步触发最大 Payload = 6 MB, 异步触发最大的 Payload = 256 KB. 查询这篇文档 https://docs.aws.amazon.com/lambda/latest/operatorguide/invocation-modes.html 可以知道 SQS 触发的方式是 Polling (轮询), 而触发方式是 同步. 所以最大 Payload 是 6MB.

**2. Q trigger Lambda 的并发机制**

AWS Lambda 本质上是一个容器. Lambda Function 的并发是通过启动多个容器来实现的. 也就是说同一个 Lambda Function 启动了 N 个容器 就是 N 个并发.

如果 Q 的下一次触发来临时, 前一个触发的 Lambda 还没有结束运行, 则 Q 会触发一个新的 Lambda Function. 这篇文档很好的说明了 Lambda 的并发数量是如何根据请求的数量随时间变化的.

**3. 在并发时 Q 发送 Message 的机制**

首先我们要了解一个概念叫做 **MessageGroupId**. FIFO Q 并不是保证所有的消息在全局上保持生产和消费的顺序完全一致的, 而是保证在同一个 MessageGroupId 内是一致的. 当然如果你所有消息的 MessageGroupId 都是一样的, 那就相当于全局一致. 这个设计是因为真正要求严格全局一致的应用几乎不存在, 例如最严格的银行业务, 你可以用涉及的 AccountId 构造一个 MessageGroupId, 只要在这个 GroupId 下多个 transaction 的消息严格按是顺序处理即可. 又或者电商的订单业务, 保证同一个 OrderId 下的消息严格按顺序处理即可. FIFO Q 中的所有 Message 都必须指定 MessageGroupId 并且 MessageGroupId 能够很好的平均算力流量, 提高并发性能, 至于原理我们后面会讲到.

其次还有个概念叫做 **In Flight**, 其含义是消息已经被 Consumer 接收到, 但还没有被从 Queue 中删除, 此时的状态就叫 In Flight.

根据这篇博文 https://aws.amazon.com/blogs/compute/new-for-aws-lambda-sqs-fifo-as-an-event-source/, 每次 trigger 的时候, 发送出去的 message 列表 是按照以下规则构建:

1. 找到最早的, 满足以下条件的 MessageGroupId - 没有任何相同的 MessageGroupId 的 Message 处于 In Flight 的状态. 如果所有的 GroupId 都有处于 In Flight 状态的 Message, 则停止不触发 Lambda. 换言之, 假设 Q 中有 N 个不同的 MessageGroupId. 在没有 Consumer 的情况下 (我们称每一个运行中的 Lambda Function 为一个 Consumer), 最先进来的 Message 的 MessageGroupId 就会被选中. 而很自然的, 由于每个并发都会处理一个不同的 GroupId (不然不可能被触发), **所以最大并发数和不同的 MessageGroupId 数量相等**.
2. 按顺序找到和 #1 中选中的 MessageGroupId 相同的 Message, 越多越好, 不超过 Batch Size 即可.
3. 如果所有消息都被找到还没有达到 Batch Size, 则重复 #1, 找一个新的 MessageGroupId 并按照 #2 添加更多 Message. 也就是一个 Payload 中可能会包含多个 MessageGroupId.

这里我们要注意的一点是, 例如如果有 10 条 Message In Flight, 你直接用 receive_messages API 想再获得 10 条消息是不可能的, 他会返回空数据. 因为在 In Flight 的消息在 receive 的时候依然会按照顺序先传递给客户端, 而由于他们还没有被删除, 而且有 invisible time 的机制存在, 你是无法获得他们的. 如果没有这个机制, 就会导致同一个消息被消费多次, 或者消费的顺序和产生顺序不一致.

**4. 失败重试机制**

首先我们要了解 Dead letter queue (DLQ) 的机制. SQS 允许为你的每一个 Q 指定一个 DLQ 和 MaxReceivedCount, 当一个消息被 receive_message 后立刻 ReceivedCount + 1, 如果没有被删除, 则在 VisibilityTimeout 结束后返回 Q. 当 ReceivedCount 达到上限, 则自动被移动到 DLQ 并从原 Q 中删除. 普通 Q 的 DLQ 也必须是普通 Q, FIFO Q 的 DLQ 也必须是 FIFO Q. DLQ 主要是用来储存那些失败的消息, 同时避免 Consumer 在错误的消息上无限循环重试. **注意! Lambda 的设置中也可以配置 DLQ 用来捕获失败的 Lambda Invoke, 这类的 DLQ 要直接在 Q 上配置, 而跟 Lambda 毫无关系**.

其次我们要了解一个概念叫 RetryAttemptId. 如前面所说, 如果消息 In Flight 你是无法再用 Consumer 接受到的. 而如果你第一次接手时指定了 RetryAttemptId. 则可以在失败后, 并且还没有读过 VisibilityTimeout 的这段时间里使用 RetryAttemptId 重新访问那些消息进行重试. 而这个重试也是要耗费 ReceiveCount 的.

根据官方文档 https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html, 每次 Q 触发的 Lambda 时候所传递的那些 Message 都是包含 RetryAttemptId 的. 当 Lambda 抛出异常, 没有删除消息就结束时, 所有的 ReceivedCount 会 + 1. Event Source Mapping 会用 RetryAttemptId 再次获取数据重新出发 Lambda. 如果 ReceiveCount 达到了 MaxReceiveCount 的设置, 消息则会全部被送往 DLQ. 如果直到 VisibilityTimeout 了还没有达到 MaxReceivedCount, 那么则会重复这一过程.

**官方推荐, MaxReceivedCount 设为 5, VisibilityTimeout 为你的 Lambda Function Timeout 的六倍. (VisibilityTimeout 一定要比 Lambda Function Timeout 长)**

根据官方文档 https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html, 如果你成功处理完所有的 message, 你无需手动删除这些 message, 这些 message 会自动被删除 (未证实). 如果 lambda 报错, 即使只有一个消息出错, 所有的消息都会被返回队列. 所以你要保证 lambda 的操作要么有幂等性, 处理 N 次和处理 1 次的效果一样. 要么有原子性, 要么全部成功要么全部不成功. 通常幂等性可以通过 DynamoDB 轻松实现.

**5. Only One Delivery**

根据这篇博文 https://aws.amazon.com/blogs/compute/new-for-aws-lambda-sqs-fifo-as-an-event-source/, FIFO Q + Lambda 可以保证顺序的严格一致, 但是无法保证 Only One Delivery, 只能保证 at-least-one-delivery. 所以你要保证你的 Consumer 对于消息的处理得是 idempotent (幂等性, 你执行一次和执行无数次的效果是一样的. 比如 + 1 这个操作就不是幂等的). 这可以通过使用 DynamoDB 并用 MessageId 作为 Key 来实现, 每次消费成功后将 Value 设为 True 即可.


最佳实践
------------------------------------------------------------------------------

1. Producer 产生的 Message 要根据业务逻辑产生不同的 MessageId. MessageId 越丰富, Scale 的性能越好.
2. 为你的 Lambda Function 配置 ReservedConcurrent, 实现并发的上限.
3. 合理设置 Batch size 和 Batch window, 根据你的 Message 的大小, 不要超过 Payload 的上限. 并且由于只要有一个出错, 全部的消息都会被打回 Q 重试, 所以一次处理的消息太多会导致出错的概率变大.
4. 为你的 FIFO Q 配置 DLQ, MaxReceivedCount 设为 5. visibiility timeout 为 lambda function timeout (处理 batch 所需的最多时间) 的 6 倍.
5. 使用 DynamoDB, 用 message id 作为 key 实现对每一个 message id 只消费一次.
6. 优化你的 Lambda Function, 减少冷启动时间.


实战代码
------------------------------------------------------------------------------

我们这里不使用 IAC (CloudFormation) 来启动资源. 我们用 AWS Console 来创建测试所需资源.

- DLQ:
    - Name: poc-fifo-q-dql.fifo
    - Visibility Timeout: 60 Sec
    - Delivery Delay: 0 Sec
    - Message Retention Period: 14 Days
    - Receive Message Wait Time: 0
    - Max message size: 256KB
    - Deduplication Scope: Message Group
    - FIFO throughput limit : Per Queue

- FIFO Q:
    - Name: poc-fifo-q.fifo
    - Visibility Timeout: 60 Sec
    - Delivery Delay: 0 Sec
    - Message Retention Period: 4 Days
    - Receive Message Wait Time: 0
    - Max message size: 256KB
    - Deduplication Scope: Message Group
    - FIFO throughput limit : Per Queue
    - Dead Letter Queue:
        - use the DLQ created before
        - max receive count: 5 (retry 5 time then go DLQ)

- Lambda Function:
    - Function Name: poc-fifo-q-consumer
    - Runtime: Python3.7, handler = consumer.main
    - Configuration:
        - General Configuration: Memory = 128 MB, Timeout = 10 Sec
    - Trigger:
        - Batch Size: 10
        - Batch Window: 30


