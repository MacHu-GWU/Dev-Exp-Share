.. _data-loss-and-double-consume-in-kafka:

Data Loss and Double Consume in Kafka
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Summary
------------------------------------------------------------------------------
"Data Loss (丢数据)" 和 "Double Consume (重复消费)" 是流数据处理中常见的两类问题. 本文详细的探讨下这两个问题产生的原因以及如何应对.


2. Data Loss
------------------------------------------------------------------------------


产生的原因
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Kafka 中位于内存的数据还没有被 flush 到磁盘就断电了. 导致永久丢失这条 message.
2. Replica 的设置为 3, 但是 producer ACK = 1, 只有一个 leader 获得这个数据就继续了, 结果还没来得及 replica 就断电挂掉. 导致永久丢失这条 message.
3. Consumer 使用 auto complete, 结果收到数据后还没有处理完就自动 commit 了, 结果 consumer 挂掉. 物理上没有丢数据, 逻辑上跳过了这条 message.


解决的方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 用集群, 比如 AWS MSK 就没有这个问题
2. ACK 设为 2 或者 3, 不要设置为 all, 因为 all 意味着所有的 broker 确认收到才能继续, 这代价太大了
3. 使用 manual commit. 具体做法请参考 :ref:`kafka-autocommit-vs-manual-commit`


3. Double Consume
------------------------------------------------------------------------------


产生的原因
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 第一类, 由于 Consumer 所引起的: Consumer 在消费完消息, 业务已经完成后, 在 Commit 之前, 这时候 Consumer 因为各种原因 (断电, 代码异常, Consumer 取消了 Subscription 等) 挂掉, 导致 Offset 的 Commit 没有提交.
2. 第二类, 由于 Kafka Server 所引起的: Partition 和 Consumer 是靠 heartbeat 机制判断 Consumer 是否存活的, 如果 Consumer 消费一条 Message 的处理时间较长,  Partition 的 ``session.timeout.ms`` 设置的时间比这个端, Partition 会认为 Consumer 已经挂掉, 而实际上业务已经被处理完成. 那么会触发 Re-balance 重平衡, 这个已经被消费过的 Message 就会被其他的 Consumer 接管并重复消费.


解决的办法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 引入消息去重机制. 例如: 生成消息时, 在消息中加入唯一标识符如消息 id 等. 在消费端, 可以保存最近的 ``max.poll.records`` 条消息 id 到 redis 或 mysql 表中, 这样在消费消息时先通过查询去重后, 再进行消息的处理.
2. 保证消费者逻辑幂等 (idempotent). 可以查看博客 `一文理解如何实现接口的幂等性 <https://cloud.tencent.com/developer/article/1839609>`_
3. 提高消费者的处理速度. 例如L 对消息处理中比较耗时的步骤可通过异步的方式进行处理, 利用多线程处理等. 在缩短单条消息消费的同时, 根据实际场景可将 ``max.poll.interval.ms`` 值设置大一点, 避免不必要的 Re-balance. 可根据实际消息速率适当调小 ``max.poll.records`` 的值.
