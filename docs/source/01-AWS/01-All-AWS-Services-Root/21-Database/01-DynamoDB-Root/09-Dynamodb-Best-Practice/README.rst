.. _dynamodb-best-practice:

Dynamodb Best Practice
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Partition Key Design
------------------------------------------------------------------------------
由于 Hash Key 决定了 Item 在哪个实体 Node 上被处理. 作为一个分布式系统, 每个 Partition (分片, 实体 Node) 的吞吐量是有上限的, 这个软上限在 Dynamodb 中是 3000 RCU 和 1000 WCU. 换言之当有节点的吞吐量快要达到这个值, Dynamodb 就会自动增加节点. 如果你的 Hash Key 选择合适, 你的 workload 会被非常平均的分配到每个节点.


Using Burst Capacity Effectively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference:

- Using Burst Capacity Effectively: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html#bp-partition-key-throughput-bursting

``Burst Capacity`` 是 Dynamodb 最大化你的 R/W Capacity 的一种机制. 在 Provisioned Billing Mode 的模式下, 当你 5 分钟内有没有使用的 RCU / WCU, 这些 Capacity 会被保留起来. 如果你需要多余你设定的读写速度, 则可以利用这期间保存的读写带宽. 该情况在你知道你的流量波动是在每 5 分钟以内只会有很少的 Spike, 比如一次. 那么这个机制可以让你用远低于 Spike 所需的 Capacity 来处理 Spike 的请求.

Understanding DynamoDB Adaptive Capacity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference:

- Understanding DynamoDB Adaptive Capacity: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html#bp-partition-key-partitions-adaptive

``Adaptive Capacity`` 是 Dynamodb 在为 workload 不平均的 Partition 分配 Capacity 的一种机制. 由于 Dynamodb 有 Partition, 所以你的总 RCU WCU 的带宽在每个 Partion 上是要均分的. 如果某个特别 Hot 的 Partition 的带宽超过平均值 (比如你用 User Id 作为 Partition Key 而超级明星用户在这个 Partition 上) 也是可以的, 只要总数没有超过你的总 RCU WCU. 要知道单个 Partition 是有 3000 RCU 1000 WCU 的软上限制的, 但是假设你的总数是 9000 RCU 3000 WCU, 而有 3 个 Partition, 那么其中的 Hot Partition 可以超过 3000 RCU 1000 WCU 的限制. 不过在设计表的时候要尽量避免该情况的发生.


Isolate Frequently Accessed Items
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果某个 Partition 上有很多 Hot Hash Key, Dynamodb 会通过修改 Consistent Hash Ring 的方式, 将其 reblance 到其他的 Node 上. 原则上让热数据分散到不同节点上. 极端情况下如果有一个 Key 非常热, 可能一个 Partition 上就只有这 1 个 Key.


Distributing Workloads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
例如你有一个 hash key 同时有 range key 时, 由于 Dynamodb 只要求 hash key + range key 的 combination 是唯一的, 所以可能有非常多的 item 都落在一个 hash key 上. 例如在电商数据中, 你把 date 作为 hash key, time stamp 作为 short key. 那么同一天内的 item 都会落在一个 partition 上. 这显然是不好的. 一个做法是, 在 hash key 后面加 surfix, 比如加 ``2000-01-01_1``, ``2000-01-01_2``, ..., ``2000-01-01_25``, 这样写操作的 workload 就会被分散开了. 可代价是你在查询的时候, 为了获得一个数据, 需要发起 25 次 get 并将其汇总.


Write Sharding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
该方法是加 Surfix 的进阶版. 当你明确知道除了 hash key, 还有某一个 field 也是一定会存在的, 而这个 field 的 cardinalogy 非常高. 那么你可以用这个 field 计算出一个 Surfix. 这样在查询的时候, 你依然可以只用一个 Get 就找到这个 item.

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-aggregation.html


Aggregation in Dynamodb
------------------------------------------------------------------------------
在 Dynamodb 中是没有 Aggregation 函数的. 但是我们依然有办法做 Aggregation, 下面我们举例说明:

举例来说有个超时的销售数据, 每一个 item 代表着一个订单的日期. 由于 order_id 更为随机, 比较适合做 partition key. 而 一个 order 中的 item 是唯一对应关系, 你可以用 quantity 等信息来描述销售额, 所以 item 可以作为 range_key. 这样 order_id 和 item_id 的 combination 可以保持唯一. 数据看起来像这样::

    {
        partition_key_oder_id: ...
        range_key_item_id: ...
        date: ...
        total: ... <--- sales amount
    }

你想要知道每个商品在每天的销量总和. 你有三种办法:

1. Scan 整个表, 然后再 In memory 做计算.
    - 优点: 简单直白易于实现
    - 缺点: 需要扫描大量数据, 消耗 Capacity
2. 用特殊的 item 为每个 item 每天的销售额做统计, 由于 item_id 和 order_id 前缀不同, 不可能重复, 所以把 item_id 放在 partition key 里是没有问题的. 同样把 date 放在 range key 里也是没有问题的, item 就像这样 ``{partition_key_oder_id: item_id: ..., range_key_item_id: date, total: ...}``. 每次 create / update / delete Item, 都用一个 transaction 把对 order 的修改和对特殊的的 Aggregation item 的修改打包在一起. 这样你就可以随时获得 aggregation 的数据了.
    - 优点: 容易实现.
    - 缺点: transaction 使得对 capacity 的需求提高了一倍. 性能也降低了一半.
3. 用 Dynamodb Stream, 把 Write 的 event 发送到一个 Stream 里, 然后触发 Lambda, 维护另一个 Table.
    - 优点: 对性能没有影响, 无论是原表的 R/W 还是 Aggregation 表的 R/W 都不需要 transaction. 异步调用.
    - 缺点: 需要维护额外的 resource, 并且对 lambda 进行更新并不容易.

对于 方法 2,3, 为了做 Aggregation, 你需要预先知道你的业务中 Aggregation 的逻辑. 你没法先存数据, 然后再设计 Aggregation 逻辑. 如果你新增了 Aggregation 逻辑, 你不但需要更新 Application 代码, 如果历史的 Aggregation 依然重要, 你还需要 Scan 来创建这些 Aggregation 数据的初始值, 在这期间新的 Update 触发的对这些 Aggregation 的修改还不能影响初始值的计算, 比较难设计.


Time Series Data
------------------------------------------------------------------------------
Reference:

- Time Series Data: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-time-series.html

对于时间序列数据, 必然有冷热数据之分. 近期数据一般都是比较热的, 而历史数据都比较冷. Dynamodb 建议将 Date 作为 PK, Time 作为 Range Key. 然后 Date 作为 Table Name. 然后对于旧的 Date 的 Table, 降低 Capacity Quota, 这样可以大大降低花费.

但是要注意一个 AWS Region 只能创建 256 个 Table. 所以这些 Table 成为冷数据之后, 你需要将其进行手动 Merge. 同时在你的 Application Code 中也要对其进行适配. 还是有蛮多工作要做的.
