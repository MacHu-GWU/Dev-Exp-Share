Short and Long Polling
==============================================================================

- Reference: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html


什么是 Short Polling
------------------------------------------------------------------------------

SQS 后台是分布式的, 一个队列的许多消息是分布在多台机器上的. Short Polling 是指每次 消费数据 时, 根据权重从这些机器上随机采样, 并汇总返回数据. 但是这是完全可能采样到的机器上没有消息, 导致返回 Empty Response. 或是其他机器上有消息, 但是被采样的机器没有, 这又叫 False Empty Response.


什么是 Long Polling
------------------------------------------------------------------------------

长轮询是指客户端发起消费请求时, 如果队列中没有消息, 队列不会立刻返回, 而是 Hold 住一段时间直到返回数据. 这样能够减少 Empty Response 的概率, 从而节约开支, 提高效率.


Differences Between Long and Short Polling
------------------------------------------------------------------------------

Short polling occurs when the WaitTimeSeconds parameter of a ReceiveMessage request is set to 0 in one of two ways:

The ReceiveMessage call sets WaitTimeSeconds to 0.

The ReceiveMessage call doesn’t set WaitTimeSeconds, but the queue attribute ReceiveMessageWaitTimeSeconds is set to 0.
