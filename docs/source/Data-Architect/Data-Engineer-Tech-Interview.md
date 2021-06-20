
Data Engineer Tech Interview
==============================================================================


Q. Sync data from RDBMS Database to Data Warehouse
------------------------------------------------------------------------------

你有个 RDBMS 数据库, 上面跑着你的业务数据. 你想要将数据库同步到数据仓库中. 该怎么做? 要求:

- 延迟越低越好

**场景**:

我们可以假设一个场景, 电商网站后台是一个 MySQL AWS RDS 数据库, 我们想要将里面的数据 Load 到 AWS Redshift 上.

**为什么要从 RDBMS 把数据同步到 OLAP**?

1. 在 RDBMS 上执行查询会影响 Applicaton 的性能
2. RDBMS 本身的查询性能并不好
3. RDBMS 可能不支持某些查询函数和语句

**同步数据的两种主要思路**:

1. 用 Batch. 定期将 MySQL dump 成数据文件, 然后 Load 到 Redshift 上.
2. 用 Streaming. 每个写入 MySQL 的 SQL 命令, 都以某种方式 Forward 到 Redshift 上. 

Batch 的好处:

- Easy to implement, less likely to have data erro

Batch 的坏处:

- Long 
