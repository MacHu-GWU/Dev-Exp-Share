.. _kafka-offset-and-commit:

Kafka Offset and Commit
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


.. _kafka-offset:

什么是 Offset (位移)?
------------------------------------------------------------------------------
我们知道 Kafka 每个 Partition 内部是严格保持顺序一致的 (FIFO). 从第一条到达 Kafka 的 消息起, 每条消息都会有一个严格递增的序号, 这个序号就叫做 **Offset**. 我们可以按照 1 算起 (实际上不是从 1 开始的, 但是为了方便理解). Consumer 消费数据的时候也是从序号小的开始往序号大的按顺序消费. 如果 Consumer 中间停机了, 而新的消息还是不断到达 Kafka, **那么 Consumer 再次启动时候如果和从上次停机时消费到的位置开始消费, 而不是消费最新的消息呢**?

原因是 Kafka 服务端会 **保存** Consumer 消费到的 Offset, 然后在 Consumer 再次启动后从 Offset 处开始给新数据. 这个 "保存" 的动作是由 Consumer 发起的, 叫做 :ref:`Commit <kafka-commit>`.

思考题:

1. 为什么 Kafka 不为每个 Message 按顺序创造一个 UUID, 然后建立一个哈希表 Key 是 UUID, Value 是 0, 1, 用此来记录消息被消费到哪里了呢?
2. 为什么 Kafka 不为每个 Consumer 维护一个 Message 的副本池 (因为同一条消息可能会被多个 Consumer Group 所消费多次). 没被消费的按顺序放在一个文件夹, 被消费过的按顺序放在另一个文件夹呢?
3. Consumer 按顺序收到 3 条消息, 1, 3 成功了并 Commit 了, 2 没有. 那么停机断电后重启再开始消费, 会从哪里开始消费呢?


.. _kafka-commit:

什么是 Commit (提交)?
------------------------------------------------------------------------------
根据 :ref:`kafka-offset` 一节的内容, 我们知道 Kafka 靠 Offset 来记录 Consumer 消费到哪一条消息了. 但 Consumer 消费一条消息可能成功也可能失败, Kafka 是怎么知道到底这条消息算成功还是失败呢? 答案就是 Commit 机制. Consumer 在消费成功后, 可以向 Kafka "Commit" 代表这条消息已经被消费过了. 而 Kafka 则 "记录" (这个记录的原理不简单, 后面会详细说) 最新的 Offset. 即使断电重启, 下次 Consumer 拉取消息的时候就不会重复收到这条消息了.





关于消费进度还有一点, 跟 Commit 无关, 就是在流处理程序中可能会执行多次 poll, 每次 poll 都会拉取一批 Message. 每次  poll 的过程中并没有 Commit, 但是仍然不会重复拉取消息, 这是为什么? 这是因为 Consumer 在内存中存了一份 "fetch offset", 每次拉取的时候会告诉 Kafka 从 "fetch offset" 之后开始拉取.


.. _kafka-autocommit-vs-manual-commit:

AutoCommit vs Manual Commit (自动提交 和 手动提交)
------------------------------------------------------------------------------
Kafka 的 Commit 分 2 种, 自动提交 和 手动提交.

**自动提交流程**

在流处理过程中, Consumer 会间隔时间从 Partition 上 Poll 一部分数据, 然后就是进行业务处理. **每次 Poll 数据的时候会把前一次 Poll 的消费进度提交. 提交的时间点是固定的下一次 Poll 的时候**. 这样的可以避免每次提交

可能遇到的问题:

- Q: 业务正常处理完成, 但在 Commit 之前 Consumer 就宕机了. 重启后出现重复消费问题. 这怎么处理?

实际流处理程序中我们还可能自己设计一个缓存, 每积累一定量再业务处理, 这种流程中可能会出现缓存没积累够之前就 Poll 过了至少一次, 即已经提交了消费进度. 这时候如果consumer宕机，则消费数据没来得及处理入库，出现丢数据问题。

**手动提交流程**

手动提交通常只会在业务处理之后才提交消费进度.

可能遇到的问题:

- Q: 业务正常处理完成, 但在 Commit 之前 Consumer 就宕机了. 重启后出现重复消费问题. 这怎么处理?

总结:

不管自动提交还是手动提交, 遇到的问题本质都是数据一致性的问题, 可以理解为业务处理数据并入库的进度和 Kafka 的消费进度出现不一致.

终极方案：

如果对数据一致性要求非常苛刻，可以考虑把消费进度存在业务数据库中，消费进度和业务处理统一管理，并且能保证一致。


Kafka 是如何维护 Consumer 的 Offset (位移) 记录的.
------------------------------------------------------------------------------
**简介**

每个 Consumer 在 Commit 的时候, Kafka 内部会把这个 Commit 命令所带的 Metadata 一起打包成一个特殊的 Message, 这个 Message 里就带有 Offset 的信息. 然后发送到一个由 Kafka 内部维护的叫做 ``__consumer_offsets`` 的 Topic 中. Kafka 在服务端也有自带的 Consumer 不断消费 ``__consumer_offsets`` 中的消息. Kafka 在内存和磁盘中会维护一个哈希表, Key 就是不同的 Consumer 的 Key (这个 Key 不简单, 后面详细说), Value 就是 Offset. 这个自带的 Consumer 就会不断的更新哈希表中的 Value, 这个 Value 就是由 Kafka 所维护的 Offset.

为了避免 Broker 断电丢失数据, 消息会被传播到 Replica Broker 的内存中并确认后才会被认为消费成功. 然后不定期的 Broker 会将这个哈希表落盘. 如果一个 Broker 断电了, Replica Broker 的内存中依然有这个数据.

这个消费进度信息在老版本 (<= 0.9) 是由 Zookeeper 管理, 在新版本存由 Kafka 管理. 放在 Zookeeper 的问题很明显, Zookeeper 是面向整个系统的协调服务, 侧重于数据一致性, 每次更改都会开启事务同步各个子节点. 流处理业务提交频繁, Zookeeper 会负载过高, 影响到整个系统的性能.

**__consumer_offsets 详细原理**

``__consumer_offsets`` 是 Kafka 自行创建的, 和普通的 Topic 相同. 它存在的目的之一就是保存 Consumer 提交的 Offset.

``__consumer_offsets`` 中的每条消息格式你可以理解为一个 Key Value 形式, 就像这样::

    {
        "Key": {
            # Kafka 对 __consumer_offsets 实现的版本信息, 在 2.x 中的值都是 1
            "key_version_id": "key_version_id",
            "topic_name": "topic_name",
            "consumer_group_id": "consumer_group_id",
            # Consumer 所 Commit 的消息是从哪个 partition 上读来的
            "partition_id": "partition_id",
        },
        "Value": {
            # 和 key_version_id 类似
            "value_version_id": "value_version_id",
            "offset": "offset",
            # 用户自定义的 metadata 有大小上限
            "metadata": "metadata",
            "commit_timestamp": "commit_timestamp",
            # commit_timestamp 与设置中 offsets.retention.minutes 参数值之和
            # 过期了就会被清理掉
            "expire_timestamp": "expire_timestamp",
        }
    }

考虑到一个 Kafka 生产环境中可能有很多 Consumer 和 Consumer Group, 如果这些 Consumer 同时提交位移, 则必将加重 ``__consumer_offsets`` 的写入负载, 因此 Kafka 默认为该 Topic 创建了 50 个 Partition. 对于这个特殊消息, Kafka 会对 ``consumer_group_id`` 做哈希求模运算, 从而将负载分散到不同的 ``__consumer_offsets`` Partition 上. **这样就可以保证消费位移信息与消费组对应的 GroupCoordinator 处于同一个 Broker 节点上, 省去了中间轮转的开销, 这一点与消费组的元数据信息的存储是一样的 (我还不理解)**.


**一个典型的案例**

- Cluster: 有 3 个 Broker Node
- ``data`` Topic: 有 4 个 Partition, 我们记为 data_p1 到 data_p4
- Consumer Group: 有 2 个 Consumer, 分别负责 data_p1, data_p2 / data_p3, data_p4
- ``__consumer_offsets``: 有 12 个 Partition, 我们记为 offset_p1 到 offset_p12. 其中 1 ~ 4 位于 Broker1, 5 ~ 8 位于 Broker2, 9 ~ 12 位于 Broker3.

**Consumer Commit 后发生了什么**

- 根据你 ``group_id`` 哈希取模计算出 offset_pX, 我们假设是 offset_p6 好了. 那么这个 Consumer Group 所有的 Consumer 的 commit 都会被 offset_p6 处理. 而 offset_p6 位于 Broker2 上, 所以这个 HashMap 也是被维护在 Broker2 上. 同理, ``__consumer_offsets`` 也会有 12 个 Consumer, 每个 Consumer 都位于对应 offset partition 所在的 Broker 上, 用于不断更新 HashMap.

**Consumer 重启后如何获得 Offset (OffsetFetchRequest)**

Consumer 随机找一个 bootstrap brokers list 中的 Broker 发起 ``OffsetFetchRequest`` 请求. 可以计算取模获得这个 HashMap 位于哪个 Broker 上, 然后找这个 Broker 要 HashMap 中的信息即可知道对于 Data Topic 的每个 Partition, offset 是多少了.




0人点赞
消息中间件



Ref:

- kafka commit机制以及问题: https://www.jianshu.com/p/bd19445fed7d
- __consumer_offsets的介绍: https://www.jianshu.com/p/66efaead2302
- Kafka 中的消费者位移 __consumer_offsets: https://www.i4k.xyz/article/qq_41049126/111311816
- 消费者偏移量__consumer_offsets_相关解析: https://blog.csdn.net/z69183787/article/details/109810468
- kafka系列之(3)——Coordinator与offset管理和Consumer Rebalance: https://www.jianshu.com/p/5aa8776868bb
- 消息存储和offset提交机制: https://codeantenna.com/a/phPsKdEPfk



**思考题**

- Q: Consumer 的 Offset 由 Kafka 维护. 那么 ``__consumer_offsets`` 的 Kafka 内部 Consumer 的 Offset 又由谁维护呢?

    Kafka 自己在缓存中管理的

- Q: 为什么要用 ``__consumer_offsets`` 来维护? 而不是直接在 Commit 的时候更新 Hashmap 中 Offset 的值吗? 反正 Consumer Commit 的顺序肯定是严格有序的.

    Commit 的顺序是严格有序的, 但是 Hashmap 更新本身不是严格有序的, 在高并发的情况下可能无法维护顺序. 并且这会导致 Broker 是有状态的, 因为它要在内存中保持这个状态, 在每次落盘之间如果所有 Broker 断电就可能导致数据丢失.

    而 Kafka Topic 本身已经实现了严格按顺序消费的机制, 那么把这个 Set Hashmap Value 的一系列操作编程一系列有序的 Message 能保证 Hashmap 的更新也是严格有序的. 就算 Broker 全部挂掉, 由于 Message 本身是持久化保存的, Broker 重启后只要在 Message 还没有 Expire 之前都是可以恢复计算出 HashMap 中 Offset 的正确值的.


Kafka 术语中英列表
------------------------------------------------------------------------------
- Cluster: 集群
- Node: 节点
- Broker: 代理
- Producer: 生产者
- Consumer: 消费者
- Partition: 分区
- Replica: 副本
- Message: 消息
- Offset: 位移
- Commit: 提交
