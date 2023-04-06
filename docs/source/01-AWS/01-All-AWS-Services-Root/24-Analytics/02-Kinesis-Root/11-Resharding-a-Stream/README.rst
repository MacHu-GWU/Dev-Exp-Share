.. _kinesis-resharding-a-stream:

Kinesis - Resharding a Stream
==============================================================================
Keywords: Kinesis, Scale, Shard, Reshard

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Why Resharding?
------------------------------------------------------------------------------
一个 Kinesis Stream 的吞吐量是和 Shard 的数量线性相关的. 每个 Shard 的吞吐量限制如下:

- Write:
    - 1MB / sec, 或是 1000 records / sec
- Read:
    - 2MB / sec, shared by all consumer (You can use Enhanced-fan-out if you need more read quota), 5 Transaction read per sec.

当你的 shard 负载过高, 你就需要增加 shard, 如果你有很多 shard 负载太低有很多浪费, 则你需要减少 shard.

Ref:

- Quotas and Limits: https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html
- Resharding a Stream: https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding.html


How does Re-sharding Work? (Reshard 的内部原理)
------------------------------------------------------------------------------
这个和 :ref:`consistent-hash-algorithm` 中的模式类似. 增加 shard 就是增加物理节点, 也就是将已有的 Ring 分裂. 减少 shard 就是合并两个相邻的 Ring. 你可以先用列出所有 shard 的信息, 然后根据 `Shard Level Monitoring <https://docs.aws.amazon.com/streams/latest/dev/monitoring-with-cloudwatch.html#kinesis-metrics-shard>`_ 的监控数据找出负载过低或是过高的 shard, 然后用下面的 API 进行 分裂 / 合并 即可.

- **List Shard**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.list_shards
- **Split Shard**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.split_shard
- **Merge Shard**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.merge_shards


Strategies for Resharding (再分片策略)
------------------------------------------------------------------------------
一共有 3 种策略:

1. 直接将每片都分裂成两个, 提高一倍的吞吐量. 使用 ``update_shard_count`` API, 直接指定最终的 Shard 数量.
2. 找到 hot shard, 将吞吐量大的 shard 分片. 使用 ``split_shard`` API.
3. 找到 cold shard, 将吞吐量小的 shard 合并. 使用 ``merge_shard`` API.

其中对于 1, 所有的细节都是自动实现的. 对于 2 你需要指定 ``NewStartingHashKey``. 这跟 Sharding 的 Hash key range 的原理有关 (跟 consistent hash 的原理一样).

Ref:

- Strategies for Resharding: https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding-strategies.html


Sharding Hash Principal (哈希分片原理)
------------------------------------------------------------------------------
Kinesis Load Balance 的算法是和 Dynamodb 一样的, 都使用了 :ref:`consistent-hash-algorithm`.

Kinesis 使用 md5 算法对 ``PartitionKey`` 进行哈希. 而结果是一个 128 bit (32 个 16 进制字符) 结果. 是一个 0 ~ 340282366920938463463374607431768211455 (2 ^ 128 - 1) 之间的数, 我们用 0 ~ N 来表示, 这个叫做 ``KeyRange``. 每个 Kinesis Stream Shard 都有一个 HashValue 上限和下限, 落在这个范围内的 Record 就会被分配到这个 Shard 上.

- 如果你只有 1 个分片那么这个区间 就是 (0, N).
- 如果你有 2 个分片, 那么两个 Shard 分别是 (0, 1/2N), (1/2N, N), K 个 Shard 的情况 依次类推, 多个 Shard 的 ``KeyRange`` 永远是首尾连接着的.
- UpdateShardCount 最多只能将 Shard 数量增大一倍, 或是缩小为 1/2. 因为本质上 UpdateShardCount 是对每个 Shard 分片或是两两合并. 如果你想要增加 Shard 数量, 但是数字不是 2 的乘方, 那么你在 UpdateShardCount 之后就的有些 Shard 的 KeyRange 就会跟其他的不一样, 导致从概率上落到每个 Shard 上的数据量不平均. 所以在增大缩小时, 最好使用 2 的倍数.
- Split 操作只能将一个 Shard 分成 2 个, 但你要在已经有的 KeyRange 中选一个数, 将 Range 分割成两个.
- Merge 操作只能将 **相邻的** 两个 Shard 合并成一个.


Splitting a Shard (增加吞吐量)
------------------------------------------------------------------------------
通常将吞吐量过大的 Shard 分片, 增加吞吐量.


Merging Two Shard (减少 Shard 浪费)
------------------------------------------------------------------------------
通常用于将吞吐量少的 Shard 合并, 减少费用, 因为 Amazon 按照 Shard 数量收费.


After Resharding (重分片之后发生的事)
------------------------------------------------------------------------------
无论是你 将一个 Shard 再分片, 还是合并多个 Shard. **这个过程都不是瞬间完成的. 那么在这个过程中, Producer 和 Consumer 会受到什么影响? 以及相关的 Shard 上的数据又会被怎样移来移去呢?**

**在你执行 Resharding 的过程中, Stream 是 Inactive 的**. 此时可以 ``PutRecords`` 但是不能 ``GetRecords``. **也就是 只能写, 不能读**. 你需要在你的代码中加入异常处理的部分, 当捕获到 Stream Inactive 的错误时, 要进行等待重试, 直到 Stream 恢复 Active.

**为了解释在 Split 和 Merge 的时候, 数据是怎样被读写的, 以及怎样被移动的**, 我们需要定义: ``Parent Shard``

- 在 Split Shard 中, 则那个被 Split 的 Shard 就是 Parent Shard, 分离出的两个新 Shard 就是 Child Shard.
- 在 Merge Shard 中, 则两个被 Merge 的 Shard 都是 Parent Shard, 形成的信 Shard 就是 Child Shard.

**Split时的情况**

- 平时 Parent 处于 Open State.
- 执行 Split Shard 或是 Update Shard Count 之后, Parent 变成 Close State, 此时写入到 Parent 上的新数据会被 route 到 Child 上. 在 Resharding 之后你仍然可以使用 GetRecords 从 Parent Shard 上读取数据, 不过你读不到在执行 Resharding 之后的新数据, 因为新数据都被 route 到 Child Shard 上了.  在完成之前是也就是 只能写, 不能读的状态. 而 Parent 上的旧数据仍然在 Parent 上.
- 过了 Retention Period 之后, 里面的数据已经无法 Accessible 了, 此时 Parent 处于 Expire State.


在同一个 Shard 上的数据顺序是得到保证的. 所以如果你希望 Resharding 不会影响读取, 那么你需要优先从 Parent 上读取数据, 然后再从 Child 上读取. 当你看到 ``getRecordsResult.getNextShardIterator`` 返回 ``null`` 时, 你就知道 Parent 上已经没有数据了.


How long it takes to change the throughput by resharding it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ref: https://aws.amazon.com/kinesis/data-streams/faqs/

本质上 Split Sharding 是将一个 Shard 上的数据按照 hash 拷贝到新的 Shard 上, 所以 Resharding 的时间主要消耗在拷贝数据上. 但是由于相比全部通过的数据总量, 运行中的流数据并不会有那么多, 所以实际上不会太夸张的.

1 个 Shard 大约 3 秒. 1000 个 Shard 大约 3000 秒, 大约 8.3 小时.




How many shard do I need?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kinesis 吞吐量的基础单位是 Shard:

- Write to Shard: 1MB/sec.
- Read from Shard: 2MB/sec, 在没有启用 enhanced fan out 的情况下多个 reader. 共享这一带宽; 在启用了 enhanced fan out 的情况下, 每个 reader 使用 2MB/sec 的带宽. 多个 reader 通常是指多个 Kinesis Delivery Stream 连接到一个 Stream 的情况.
- Put records: 1000 API Call/sec, 所以最好使用 Batch put 来提高吞吐量.

在计算你的业务的平均数据吞吐量的时候要注意的地方:

- 你的一条数据用 JSON 编码压缩后的大小, 要加上 Kinesis Record 的 Metadata, 比如 Partition Key, 时间等信息之后, 才是最终的大小. 这些 Metadata 大约要占据 0.25KB.






