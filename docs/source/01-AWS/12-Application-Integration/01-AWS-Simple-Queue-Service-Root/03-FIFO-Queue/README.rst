FIFO Queues
==============================================================================

.. contents::
    :local:

Reference:

- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html#FIFO-queues-exactly-once-processing

非常重要的一点, FIFO Queue 能保证 Exactly-Once Processing (消息只被处理一次), 而 Standard Queue 不行.


DeduplicationId
------------------------------------------------------------------------------

Reference:

- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html

DeduplicationId 只支持 FIFO Queue. 如果一条带有 ``DeduplicationId`` 的消息被成功接收, 那么在 5 分钟内的 deduplication interval  以后收到任何同样 ``DeduplicationId`` 的消息, 都会被成功接收, 但是被直接丢弃. Consumer 不会见到重复的 Message.

如果你打开了 Content Based DeduplicationId, 那么 Dedpulication 则会根据 Message Body 自动生成.


MessageGroupId
------------------------------------------------------------------------------

FIFO Queue 并不会维护全局顺序. 而是在拥有同一个 MessageGroupId 的所有消息之内保证顺序.

这很好理解, 如果你的系统需要完全保证 产生, 抵达, 被消费处理 的顺序完全一致, 那么你可能需要一个强大的单线程系统, 此时分布式并不适合你.

而 99% 的要求顺序一致的场景, 都是要求局部内顺序一致就够了. 例如一个电商网站用户下订单背后的数据库命令, 只需要保证对于同一个 order id 顺序不乱即可. 由或者银行转账, 你先要确认这边钱到了, 那边再扣钱, 也只需要保证对于同一个 transaction id 顺序不乱即可.
