.. _dynamodb-table-and-item:

Dynamodb Table and Item
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Table
------------------------------------------------------------------------------

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

What is Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 Dynamodb 中没有 Database 的概念, 只有 Table 的概念. 一个 Table 实质上是许多自动扩容的物理节点.

Cross Region Global Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dynamodb Table 的所有物理节点都只能在同一个 Region 中. 但是会自动跨 Availability Zone. 如果你需要多地容灾备份, 你可以开启 Global Table 功能. 本质上并不是说你的请求会被 Route 到其他 Region 进行处理, 而是在主 Region 中被处理后同步备份到其他 Region. 当主 Region 挂掉, 系统能自动切换到其他 Region 继续进行服务, 以确保 High Availability. 这个切换过程会导致非常小的延迟. 默认是自动的, 但也可以设定成手动的. 当你开启了 Global Table 时, 你的 Write 会被确认被备用 Region 收到后才会返回成功. 但备用 Region 确认收到并不代表备用 Region 中的所有节点上的数据已经一致了.

设定为手动的是因为有的 Business 对数据正确性的要求高于可用性. 可以在客户端设定为如果连接不上 Region 则等待 5-10 秒, 然后再切换到备用 Region 继续进行服务.

Hash Key and Range Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
每个 Table 有两种可能:

1. 有一个 Hash Key, 没有 Range Key (情况 1)
2. 有一个 Hash Key 和一个 Range Key (情况 2)

注意这个 Hash Key 概念跟 SQL 中的 Primary Key 类似, 但不完全一样. Hash Key 用来决定该 Item 被哪个物理节点所处理. 在情况 1 中, Hash Key 必须是 Unique 的. 而在情况 2 中, Hash Key 可以重复, 但是 Hash Key + Range Key combination 必须要是唯一的. Range Key 是用于在同一个物理节点上进行排序索引以提高查询效率的.

简单来说, 对 Hash key 的查询效率是 O(1), 而对 Range Key 的查询效率是 O(log(N)).

Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Dynamodb 中查询有三种模式:

1. get item: 直接定位到某一条记录, 只支持 hash key 列的查询.
2. query: 利用 hash key, range key, 或是用 secondary index 索引进行查询. **这是 Dynamodb 推荐的查询方式, 比较有效率, 可以利用索引, 避免全表扫描**. 要使用 query, 你必须包含 hash key
3. scan: 对全表进行扫描, 支持任意列的条件判断. 性能差, 如果非必要不推荐.

Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果要利用非 Hash key, range key 的 field 进行查询, 又不想用 Scan, 那么可以建立 Secondary Index 为数据做索引. Dynamodb 有两种 Index, Global Secondary Index 和 Local Secondary Index, 这里不展开讲, 详情参考 :ref:`dynamodb-index`.


Item
------------------------------------------------------------------------------

Dynamodb 中的 Item 相当于 SQL 中的 Row. 本质上是一个 JSON object.
