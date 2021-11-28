.. _dynamodb-index:

Dynamodb Index
==============================================================================

DynamoDB 支持两种二级索引:

- Global secondary index: 其 hash key 和 range key 可以与基表上的 hash key 和 range key 不同的索引. 全局二级索引被视为 "全局", 是因为对索引执行的查询可以跨基表中所有分区的所有数据.

- Local secondary index: hash key 与基表相同, 但 range key 不同的索引. local secondary index的含义是 "本地", 表示 local secondary index 的每个分区的范围都将限定为具有相同 hash key 值的基表分区.


Global Secondary Indexes
------------------------------------------------------------------------------

Ref:

- Global Secondary Indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html


Local Secondary Indexes
------------------------------------------------------------------------------

Ref:

- Local Secondary Indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html



When to use Dynamodb
------------------------------------------------------------------------------

**Is DynamoDB right for your use case?**

- Have had scalability problems with other traditional database systems.
- Are actively engaged in developing an application or service.

    It doesn’t always make sense to migrate legacy applications that are not under development, unless you’re willing to invest time and effort to reimplement the data access layer, inline SQL code, or the stored procedures and functions of that application.

- Are working with an online transaction processing (OLTP) workload.

    High-performance reads and writes are easy to manage with DynamoDB, and you can expect performance that is effectively constant across widely varying loads.

- Are deploying a mission-critical application that must be highly available at all times without manual intervention.

    Dynamodb is Highly Available, low Ops.

- Are understaffed with respect to management of additional database capability and need to reduce the workload of your operations team.

- Require a high level of data durability, regardless of your backup-and-restore strategy.

- Have insufficient data for forecasting peaks and valleys in required database performance.


Ref:

- How to determine if Amazon DynamoDB is appropriate for your needs, and then plan your migration: https://aws.amazon.com/blogs/database/how-to-determine-if-amazon-dynamodb-is-appropriate-for-your-needs-and-then-plan-your-migration/