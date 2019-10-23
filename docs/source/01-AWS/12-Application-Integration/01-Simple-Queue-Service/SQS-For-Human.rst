By default, Amazon SQS uses short polling, querying only a subset of its servers (based on a weighted random distribution), to determine whether any messages are available for a response.

Short polling occurs when the WaitTimeSeconds parameter of a ReceiveMessage request is set to 0 in one of two ways:

The ReceiveMessage call sets WaitTimeSeconds to 0.

The ReceiveMessage call doesn’t set WaitTimeSeconds, but the queue attribute ReceiveMessageWaitTimeSeconds is set to 0.

Note

For the WaitTimeSeconds parameter of the ReceiveMessage action, a value set between 1 and 20 has priority over any value set for the queue attribute ReceiveMessageWaitTimeSeconds.


- Long Polling (长轮询): 长轮询本质上也是轮询, 只不过对普通的轮询做了优化处理, 服务端在没有数据的时候并不是马上返回数据, 会hold住请求, 等待服务端有数据, 或者一直没有数据超时处理, 然后一直循环下去. 这样能减少 Empty Response 和 False Empty Response (消息实际存在, 但是返回的是 Empty), 参考资料: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-long-polling.html
- Reduce Cost 降低 SQS 的开销: SQS 按照操作次数收费, 你可以用 Batch 操作, 一次性读取多条 Message 或是删除多条 Message.

