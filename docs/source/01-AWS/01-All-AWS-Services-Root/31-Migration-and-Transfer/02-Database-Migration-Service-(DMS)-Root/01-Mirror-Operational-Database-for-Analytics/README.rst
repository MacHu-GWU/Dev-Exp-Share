.. _mirror-operational-database-for-analytics:

Mirror Operational Database for Analytics
==============================================================================
Keywords: RDBMS, SQL, Database, Datalake, Analytics, Mirror, Migration


Summary
------------------------------------------------------------------------------
"将业务数据库同步到数据仓库进行分析" 是一个很常见的业务需求. 我们在分析案例前, 先确定几个定义:

- 业务查询: 跟实际业务相关的查询. 例如电商数据库根据订单号查询地址和物品. 这类查询通常会利用索引, 并且是常数运行时间.
- 分析查询: 用于数据分析和报表的查询. 例如列出最近 1 个月内被购买次数最多的 10 个商品. 这类查询通常会扫描全表, 并占用大量资源.

之所以会有这个需求是因为:

1. 进行数据分析的查询通常设计表扫描, 这很浪费数据库性能, 使得业务查询性能收到影响.
2. 业务数据库的设计本身就不一定支持大型查询.
3. 不希望数据分析人员的误操作影响业务数据库, 造成商业损失.


AWS DMS
------------------------------------------------------------------------------
**什么是 AWS DMS**?

AWS DMS (Database Migration Service) 是一个全托管的 AWS 服务. 它的本质就是在你的 Source 和 Target data store 之间创建一个 EC2 instance 或是 cluster, 在这个 EC2 上安装 DMS connector 的软件, 然后把数据从 Source 同步到 Target. 在我们的案例中 Source 是 RDBMS, 而 Target 可以是 S3 这样的文件存储, 也可以是 Redshift 这样的数据仓库.

**AWS DMS 的原理**

简单来说就是利用了数据库系统中的 write ahead log, 这个 log 记录了每一个对数据修改的过程. 只要有这个 log 我们是可以从 0 重新 replay 所有的 update action, 从而重新构建整个数据库. AWS DMS 会把 source 在一个时间节点处的 snap shot 抓取下来, 作为 "initial load". 然后把从那个时间节点后的 log 都以 stream 的方式持续写入到 target. 在 stream 中的 data 叫做 CDC (Capture of Data Change).

**AWS S3 as Target**

在项目开始阶段, 通常我们会清晰的知道 1 个 target data store. 但以后得需求可能会变. 我们希望保留一定的灵活性. 所以这时候我们通常是将 "initial load" 和 "CDC" 数据都 dump 到 低成本的 S3, 然后我们自己可以选择随时用 AWS Glue 这样的 ETL 工具将数据 load 到 target data store 中去.

跟直接用 DMS 将 source 和 target 连在一起的好处是 target 会有近实时的数据. 而这个 ETL 是由 DMS 管理的. 而你一旦把数据 dump 到 S3, 你就要自己负责将 CDC 的改变 apply 到 target 中.

**AWS DMS Data Model**

要使用 DMS, 就需要保证每个 row 都要有 Primary Key Column (PK_COL). Initial load 自不用说就是整个数据本身. 而 CDC 中的数据则是 Row 在 update 发生之后的值, 这里包含的是所有的 fields, 而不仅仅是被改变的 field. 例如 update 之前是 ``{"bank_account_id": 1, "name": "Alice", "balance": 500}`` 我们只修改了 balance, 这个 update 是 ``{"balance": {"incr": -100}}``, 那么在 CDC 中的数据则是改变后的状态 ``{"bank_account_id": 1, "name": "Alice", "balance": 400, "dms_timestamp": "2000-01-01T08:30:15.123"}``.


Create Most Recent Snapshot
------------------------------------------------------------------------------
在分析数据仓库中我们希望数据是最新的. 下面我们来讨论如何从 S3 中的 DMS output 数据创建一个 most recent data snapshot.

原理很简单, 把所有的数据 load 到 Glue ETL 中, 然后用 spark sql 写一个 window function 的查询 ``row_number() partition by PK_COL order by dms_timestamp DESC`` 然后 ``where row_number() = 1`` 这样就能获得所有发生过改变的 row 的最新数据了.


Point in Time Snapshot
------------------------------------------------------------------------------
有时候我们希望将查询数据仓库恢复到某个过去的时间节点. 方法其实很简单. 和前面的 Most Recent Snapshot 类似, 你只要加一个 ``WHERE dms_timestamp <= ...`` 的条件, 就能回复数据到某个之前的时间节点了.


Data Latency
------------------------------------------------------------------------------
根据前面的 ETL 逻辑, 每次运行 ETL 都要将全部数据包括 CDC 数据 load 到内存中. 这个数据是肯定大于最终的 RDBMS 的数据量的, 并且如果你的更新频繁的话, ETL 需要 load 到内存的数据可能会远远大于最终数据本身. 那么 ETL 所需的时间则会随着数据量的增加而增加. 而这个 ETL 的所需时间就是你的 Data Latency. 例如这个 ETL 耗时 30 分钟, 那么你的分析数据库至少是 30 分钟以前的.

为了解决问题, 通用的方案是使用 Apache Hudi 这样的 Delta Lake (增量数据湖) 方案. 该方案对 Engineer 的要求比较高, 不是每个公司都能轻松配置好. 但如果你的数据满足一些条件, 我们仍然有廉价的解决方案.

如果你的数据有时效性, 比如一条 record 被创建出来, 3 个月以后这个数据就不会用到了. 那么你可以在 DMS 启用 `date-based folder partition <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.DatePartitioning>`_. 这样无论是 initial load 和 CDC 都会有 partition key, 在 S3 中看起来像这样::

    s3://my-datalake/initial/year=2020/month=01/day=07/1.parquet
    s3://my-datalake/initial/year=2020/month=01/day=07/2.parquet
    s3://my-datalake/cdc/year=2020/month=01/day=07/1.parquet
    s3://my-datalake/cdc/year=2020/month=01/day=07/2.parquet

然后你的 ETL 只要做非常小的改变, 每次读数据的时候只读最近 3 个月的数据. 这样就能保证每次 ETL 的时间能控制在一个常数时间内. 当然代价就是你的查询只能查最近 3 个月的数据.

这种做法在很多企业中都是可行的. 因为之所以你需要尽量小的 data latency 的原因就是你的查询比较关心最近的数据. 所以比如每 5 分钟 build 一次最新数据库, 这是能够满足需求的. 而对历史数据的查询往往不需要最新, 你可以每天晚上 build 一次历史数据仓库即可.