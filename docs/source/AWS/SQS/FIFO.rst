当 consumer 处理一条信息的时间, 超过了 visibility timeout 的时间时, 会导致这条信息被其他的 consumer 收取到, 导致重复处理.

为了避免这种情况, 请一定要在 consumer 的处理逻辑中设置 ``visibility timeout`` 确保整个处理逻辑如果在一定时间内没有完成, 则自动结束. 建议使用 `timeout-decorator <https://pypi.org/project/timeout-decorator/>`_ 这个库.

Dead-Letter Queues
------------------------------------------------------------------------------

简单来说, Dead Letter Queue 就是一个单独的 FIFO Queue, 专门接收那些在原来的 Queue 被多次 Consume, 但是都没有成功的 Message (默认成功之后会删除该条信息, 所以也就是说 Consumer 收到了但没有删除). 原来的 Queue 根据设定的 redrive policy, 将那些多次失败的 Message 转发到 Dead-Letter Queues.

Reference: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html

