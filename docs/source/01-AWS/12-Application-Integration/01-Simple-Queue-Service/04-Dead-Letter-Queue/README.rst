Dead Letter Queues
==============================================================================

.. contents::
    :local:

Reference:

- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html

简单来说, Dead Letter Queue 就是一个单独的 Queue, 专门接收那些在原来的 Queue 被多次 Consume, 但是都没有成功的 Message (默认成功之后会删除该条信息, 所以也就是说 Consumer 收到了但没有删除). 原来的 Queue 根据设定的 redrive policy, 将那些多次失败的 Message 转发到 Dead-Letter Queues.

- 如果原来的 Queue 是 Standard Queue 那么 DLQ 也需要是 Standard Queue
- 如果原来的 Queue 是 FIFO Queue 那么 DLQ 也需要是 FIFO Queue


消息是如何被自动发送的哦 Dead-Letter-Queue 的
------------------------------------------------------------------------------

当消息首次通过 send_message 被发送到 Q 中时, 就算 1 次接受. 如果被 consumer 使用 receive_message 获取消息后, 消息会进入一定时间的 invisible time, 避免被其他的 consumer 重复接受. 当然这个 invisible time 比通常处理所需的时间要长. 如果 consumer 没有及时在 invisible time 到时之前删除 message, 那么 message 就会被重新 "发送"
回 Q 中, 之所以打引号是因为实际上仅仅是 receive_count 自加 1. 无论是因为 consumer 失败, 还是其他别的原因. 当这个 receive_count 达到设定值, 则消息自动被转发到 dead-letter-queue 中.

这里需要注意的是, 如果 consumer 自己的程序设计失误, 导致处理完成但没有删除消息, 导致消息被重复消费, 这个部分由 consumer 程序自己负责.


什么时候 要用 Dead-Letter-Queue
------------------------------------------------------------------------------

- 如果你的系统对消息处理的顺序没有要求, 那么你使用的是 Standard Queue, 那么这时可以用 DLQ 来存放那些无法被处理的消息, 以用于之后的 Debug. 比如创建缩略图图像.
- 用 DLQ 来过滤那些 poison pill message, 也就是能被接收但无法被处理的消息, 避免无限循环重试. 比如过滤掉数据格式不规范的垃圾消息.


什么时候 不用 Dead-Letter-Queue
------------------------------------------------------------------------------

- 不要将 DLQ 和 Standard Queue 一起使用, 如果你的业务需要无限循环重试直到消息送达. 例如你的消费者需要依赖于外部系统可用. 比如微信消息推送, 假如用户手机 App 没有打开, 我们一直没有收到用户手机 App 上的确认, 那么这个消息就无限循环, 直到用户打开 App 为止.
- 不要将 DLQ 和 FIFO Queue 一起使用, 如果你不想要破坏消息被处理的顺序. 比如视频转码服务器可能对一个视频有多个步骤, 如果你的某个步骤的消息处理失败就放到 DLQ 中, 那么如果后面的步骤成功, 就会导致结果异常. 所以此时你需要在你的代码中加入处理失败时的应对办法, 比如删除其他后面步骤的消息.


使用 DLQ 构建可靠的 Serverless 应用
------------------------------------------------------------------------------

- https://aws.amazon.com/blogs/compute/robust-serverless-application-design-with-aws-lambda-dlq/
