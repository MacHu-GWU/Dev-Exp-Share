AWS Glue
==============================================================================

.. contents::
    :depth: 1
    :local:

AWS Glue 是一个什么样的服务?
------------------------------------------------------------------------------

AWS Glue 的招牌是 Serverless ETL 服务. 本质上 AWS Glue 的后台是 Spark. 你只要定义了 Source, Transformation, Target, AWS Glue 就会为你分配所需要的计算资源, 并帮你进行 ETL.

同时 Glue 还提供了一个 Universal 的 Data Catalog 的服务, 兼容市场上大部分的数据存储.


AWS Glue 的核心概念
------------------------------------------------------------------------------

**AWS Glue Catalog**:

一个 Universal Data Catalog 的服务, 相当于 Hadoop Metadata Store. 定义了 Source, Schema, Ownership.

Catalog 在 Data 行业就是指用来描述数据集的 Metadata, AWS 的 Catalog 是一个可以描述市场上大部分流行的数据源的产品, 比如 AWS 自家的 S3, DynamoDB, Redshift, Kinesis, Auroram, Time Series 开源社区的 Kafka, MySQL, Postgres, Hadoop HBase 等等. 对于 S3, Catalog 还能够记录数据集的 Partition 情况, 以及每个 Partition 的每个 S3 Object 的列表和索引.

**AWS Glue Crawler**:

能自动扫描 Source, Detect Schema, 并生成对应的 Data Catalog. 然后能自动的发现数据增量.

Crawler 解决的技术问题有:

1. 简化了手动写 DDL (Data Declaration Language 也就是 Hive 的 Create Table 语法) 的麻烦. 自动生成 DDL 并创建 Table.
2. 同时监视多个 Data Source.
3. 对于 Data Catalog, Schema, Location 这些一般不会变, 但是数据对象会不断的被添加进来. 而每次人工添加不现实.

**AWS Glue Job**:

Glue Job 是运行一次 ETL Job 的设置. 包含了你的 Spark ETL 脚本, 运行的集群的节点数, IAM 权限, 并发数等等. 一旦配置好了 Glue Job, 就可以点击 Run Job 真正运行.


AWS Glue 相关的 Service
------------------------------------------------------------------------------

**AWS Glue Studio**:

是一个方便用户编写 Glue ETL Script 的模块, 用可视化的方式. 简化了手动编写 Glue Job, 特别是 ETL Script 的麻烦.

**AWS Glue Dev Endpoint**:

由于每次运行 Job 的时候, 是需要 Launch 一个 Spark 集群的. 如果数据在 VPC 以内, 该 Spark 集群还需要放在 VPC 以内. 而你调试代码就非常不方便了. 通常我们需要自己创建一个 Dev Spark 集群, 然后 SSH 上去编写 ETL script 进行调试, 非常的麻烦. Dev Endpoint 能为你创建一个 AWS 托管的环境, 可以连接到数据, 然后提供一个 Jupyter Notebook 对 ETL script 进行调试. **注意, 这个收费非常贵, 相当于一个 Spark 集群, 你一直开着基本一天就是 4,5$, 一定要调试完记得关掉. 即使每次启动它大约需要 15 分钟**


AWS Glue Job 和 Catalog 配合的哪些坑
------------------------------------------------------------------------------

Source 为 S3 Backed Data Catalog 的时候, 需要先 Crawl 增量:

当你的 Data Catalog 在 Crawler 抓取之后, 是会显示有多少个数据对象的. 如果在这之后你有新的数据进来, 而 Catalog 没有更新. Glue Job 是不会对增量的数据进行 ETL 的, 因为你没有重新处理.



去重:

- Job Detail 里的 Job Bookmark 选项要记得打开. 打开后每次 Job Run 就会标记处理完的数据对象 (S3 的), 之后就不会重复对同一对象进行 ETL 了. 而且你还可以选择重置 Bookmark, 把所有已经处理的数据标记为未完成.

