.. _aws-athena-basic:

AWS Athena Basic
==============================================================================
学习一个 IT 产品的时候的逻辑顺序应该是:

1. 理解这个产品解决了什么痛点, 我们可以用来做什么. 这样才有一个清晰的目标.
2. 了解这个产品是如何工作的, 原理是什么, 这样才不会想当然的有不切实际的幻想.
3. 详细了解实际解决问题的过程中, 有什么样的挑战, 解决方案是什么.


Athena 是什么? 解决了什么问题?
------------------------------------------------------------------------------
Athena 是一款分布式, 高性能, 用来 run ad-hoc query 的 SQL 查询引擎. 允许用户无需配置任何数据库, 虚拟机, 就能对 AWS S3 上的数据进行查询.

我们可以看出来, Athena 的关键就是让用户只要准备好数据, 而无需配置繁琐的数据库, 就能用 SQL 进行数据分析的工具.


Athena 的内部原理
------------------------------------------------------------------------------
**SQL 查询引擎原理**

Athena 是构建在 Presto 分布式 SQL 查询引擎之上的云产品. Presto 最早是由 Facebook 开发, 于 2013 年在 Apache Software License 下开源. 本质上 Presto 就是一对虚拟机集群, 可以对多种数据源进行并行查询并汇总的 SQL 执行引擎. 也可以理解为一个不带 Storage Engine 的分布式数据库.

使用 Athena 无需配置 Presto 服务器, AWS 自己的数据中心里配置了无数 Presto 服务器, 并且抽象出来给用户使用, 用户只要为之付费即可. Athena 主要是按照被扫描的数据量大小收费. $5 / TB.

**Database Table 原理**

要使用 SQL 前你需要定义 Database, Table. 其中 Database 仅仅是一个逻辑概念, 是一对 Table 的集合. 每个 AWS Account 下有一个内置的 Database. 而每一个 Table 对应的其实是一堆描述你的 Dataset 的 metadata. 包括了你的数据储存在哪里 (location), 数据格式是什么 (format), 数据二维组织结构是怎样的 (schema), 如何对其进行反序列化, 也就是将其读取到内存 (serde), 有哪些人可以访问这个数据 (access), 数据量有多少, 有多少个文件 (statistics), 有没有 partition key 可以利用以避免全量扫描 (partition / index).

AWS Glue Catalog 是 AWS 基于 Hadoop Hive 开发的中心化 Metadata Store, 你为定义的 Database / Table 又被叫做 Glue Database, Glue Table. 有了这些定义, Presto 就知道如何在你的 Dataset 上执行 SQL 查询了.
