.. _dynamodb-index:

Dynamodb Index
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Overview
------------------------------------------------------------------------------
DynamoDB 支持两种二级索引:

- Global secondary index (GSI): 其 hash key 和 range key 可以与基表上的 hash key 和 range key 不同的索引. 全局二级索引被视为 "全局", 是因为对索引执行的查询可以跨基表中所有分区的所有数据. 本质上 GSI 就是一个另一个隐藏的 Table, 只不过会跟基表联动更新, 以获得更好的查询性能.

- Local secondary index (GSI): hash key 与基表相同, 但 range key 不同的索引. local secondary index的含义是 "本地", 表示 local secondary index 的每个分区的范围都将限定为具有相同 hash key 值的基表分区. 本质上 LSI 就是在同一个物理机器上的一个子 Index, 这和 SQL 中的 Index 比较像, 因为 LSI 的 partition key 和基表必须相同.

这里

- R/W Capacity: 由于 GSI 本质上是另一个表, 你创建 GSI 的时候也要选择 Capacity, 跟 Table 一样可以是 On-demand 也可以是 Provisioned. (详情参考 :ref:`dynamodb-pricing`) 你对 Table 本体的 Query 和对 GSI 的 Query 消耗的是不同的 Capacity, 不通用. 而 LSI 本质上是主表上为其他 Field 建立的索引, 跟主表共享 Capacity.
- Restriction: LSI 必须在创建主表的同时创建. 主表被创建后就无法再创建 LSI 了. GSI 可以在创建主表后随时创建删除.
- Limitation: 全表最多有 20 个 GSI, 5 个 LSI. 由于 LSI 是 Local 的, 每一个 Partition Key 对应的 LSI 数据不能超过 10GB (如果超过 10GB, 你的 Hash Key 的 cardinology 太低, 选择就有问题)


Global Secondary Indexes
------------------------------------------------------------------------------

Ref:

- Global Secondary Indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html


Local Secondary Indexes
------------------------------------------------------------------------------

Ref:

- Local Secondary Indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html


Best Practice
------------------------------------------------------------------------------

