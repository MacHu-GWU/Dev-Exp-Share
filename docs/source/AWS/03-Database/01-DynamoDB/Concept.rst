DynamoDB 重要概念
================


Primary Key
-----------
DynamoDB 支持两种 Primary Keys:

1. Partition Key
    - 用于决定该 Item 被储存在哪个实体机器上
2. Partition Key (Hash Key) and Sort Key (Range Key)
    - Partition Key 和 Sort Key 的组合必须是唯一的
    - 最常用的例子是 Unique Key + Date Time 的组合

Primary Key 在当 Table 被创建后不能被更改.


Secondary Index
---------------

reference: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-general.html

一个 Table 除了 Primary Key, 可以有一个或多个 Secondary Indexes, 最多 20 个 GSI 和 5 个 LSI.

每一个 Index 相当于在维护另一个表. 每当主表数据增删改时, Index 表也会发生改变. Index 表的改动也算作 RCU / WCU.

- Global Secondary Indexes (GSI): 就是选择新的两个 Attribute 分别用作 Partition Key. 以供特殊的查询模式.
    - 有自己的 Partition 和 RCU/WCU
    - 在 Table 创建后可以更改
- Local Secondary Indexes (LSI): 就是用原来的 Partition Key, 但是用不同的 Attribute 做 Sort Key. 以供特殊的查询模式.
    - 与 Table 共用 Partition 的 RCU/WCU
    - 在 Table 创建后不能更改
