Database Migration Service
==============================================================================
Keywords: AWS DMS, Database, Migration, Service, CDC.


亚马逊的 DMS 是什么
------------------------------------------------------------------------------

是一个帮助用户进行数据库迁徙的工具.

1. 支持 Source 和 Target 的 Schema 不同, 用自定义的方式进行 Mapping.
2. 支持已有数据以及增量数据的迁徙.
3. 支持多种 Source 和 Target, 甚至是类数据库系统 (S3, Kinesis Stream) 都可以.


亚马逊的 DMS 服务的基本原理
------------------------------------------------------------------------------
DMS 的三大核心组件:

- Source Endpoint: 对数据来源的抽象, 定义了连接到 Source Database 的
- Target Endpoint: 对数据目标的抽象
- Replication Instance: 一个 EC2 的实体, 里面安装了 DMS 的软件, 是执行一切运算的地方. 可以做两件事, 拷贝数据库已有的数据, 以及捕获 CDC 增量.

DMS 是如何捕获 Source 的已有数据和增量数据的:

如何捕获增量数据:

在现代数据库系统中, 在将数据更改 Commit 到磁盘之前, 都会有一个 log 或 journal (或者叫做 write ahead log / WAL, 不同的数据库叫法不同), 记录了数据库从没有数据到当前状态的所有历史. 只要这个 log 在, 从 0 重新恢复数据库就变得可行. 根据 Transaction 发生的时间的不同, 这个 log 是严格有序的. 那么这个 log 就可以被其他系统用来做 ETL 或者迁徙. 这类似于 DynamoDB Stream 的概念. 而各个主流数据库系统有不同的软件或是插件将这个功能更好的集成. 下面列出了各主流关系数据库的用于捕获 cdc log (或者叫做 write ahead log / WAL) 分别叫什么:

- Oracle: LogMiner
- MSSQL: MS-Replication / MS-CDC
- Postgres: logical replication
- MySQL: binary logging
- MongoDB: operations log
- DB2: ongoing replication


AWS DMS Data Model
------------------------------------------------------------------------------
DMS 在 Migrate 一个数据库的时候, 你可以选择把 data dump 到 S3. 其中会有两种类型的文件:

1. Initial Load: 某个时间节点的数据库 full copy.
2. CDC: 每一个 data change 的数据, 粒度是行, CDC 里的每一行就是一个 Row 在 change 发生后的所有 value. 例如我们给某一行的一个 field value 进行了修改, 在 CDC data 中会有所有的 field 的 value 而不是这一个 field.


Create Point-in-time (Most Recent) Snapshot of the Database in Data Lake
------------------------------------------------------------------------------
在企业实际需求中, 我们需要对最终的数据而不是 CDC 数据进行分析, 而且这些数据需要放在一个 Analytics Friendly 的环境中, 这有该怎么做呢?

在 PySpark SQL 里用一个 Window Function, 先 Sort On Primary Key Column, 然后用 ``row_number() over (partition by pk_column order by dms_timestamp``, 最后 ``where row_number() == 1`` 就可以筛选出所有行的最新状态而了.

当然如果数据量非常大的时候这个很难做, 可能运行一次的时间要一小时, 那么我们的 data 就会有一小时的 Latency. 这时候我们可能要有所取舍, 比如用 `date-based folder partition <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.DatePartitioning>`_ 让 DMS 的 output 有 partition, 然后再 Glue Job 里只读取最近几个小时的 Data.
