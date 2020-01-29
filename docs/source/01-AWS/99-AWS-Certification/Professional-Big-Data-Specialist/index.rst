AWS Big Data Certification CheatSheet
==============================================================================

.. contents::
    :depth: 1
    :local:



1. Collection - IOT
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

Key Concepts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Device gateway**:
- **Message broker**: 一个 Publish 和 Subscription 模型的中间件, 负责维护 Topic.
- **Device Shadow**: 是一个 JSON Document, 记录了 Device 的当前状态. 官方原话: Device Shadow is a JSON Document used to store and retrieve current state information for a device. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.
- **Device Shadow Service**: 是一个服务, 维护所有 Device Shadow (相当于一个数据库). Device Shadow Service Provides persistent representation of your devices. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.
- **Rules engine**: 一个规则引擎, 使用 SQL 类似的语言从 Message Payload 中选择数据, 然后使用其他 AWS 服务来处理数据, 比如用 Lambda 将数据存入 DynamoDB.
- **Registry**: 将具体 Device 注册到 IOT Things 中, 也就是说在数据库中创建一个条目.
- **Group registry**: 将 Device 注册到一个组里, 从而批量管理 Device.
- **GreenGrass**: 可以在 Device 上安装的 SDK 软件, 在 Local 机器上创建虚拟的 AWS 环境, 在本地运行 AWS Lambda 等. Bring local compute, messaging, data caching, sync, and ML inference capabilities to edge devices.


Authorization and Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS IOT 支持 4 种验证方式:

- X.509 certificates
- IAM users, groups, and roles
- Amazon Cognito identities
- Federated identities

1. IOT Device: 用 X.509 Certification
2. Mobile Application: 用 AWS Cognito
3. Web / Desktop Application: 用 IAM or Federate Identities.

2, 3 都比较好理解, 我们重点来说一下 1.

1 实际上是在 AWS Console 里注册一个 Certification, 然后将 IOT API 的操作权限 Attach 给一个 Policy. 在 IOT 的硬件中, 将 Public Key 和 Private Key 写入硬件, 然后硬件就可以用这个 Certification. 这跟 Https 的 Certification 类似. 只不过 Https 的证书由多家可信的大公司发布, 而这里是由 AWS 发布.




1. Collection - Kinesis
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


Key Concepts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :depth: 1
    :local:

- Ref: https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-concepts.html?shortFooter=true


Kinesis Stream Record and User Records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- User Record: 将用户的数据编码成的 2 进制 Blob. 这个 Blob 可能代表着 Json, CSV 或任何数据.
- Stream Record: 关于 Blob 的 Metadata, 包括 Partition Key, Sequence Number, 以及 Blob 本身.


Batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

将多个同类的操作记录下来, 达到一定数量后统一执行. 这个过程是异步的. **比如说打包多个 PutRecord 的操作, 然后一起发送, 以更高效的利用网络带宽. 如果使用了 Batch, 那么发起第一个 PutRecord 的操作的客户端程序不需要等到 Kinesis 成功的确认, 就可以进行后面的工作了**.

KPL (Kinesis Producer Library) 有两种 Batch 操作, 具体解释见下:

- Aggregation
- Collection



Aggregation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

将多条 Stream Records 合并成一条 Record. 打包的对象是 User Record.


Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

假设用户的数据时 web app 的 click event, **那么 多个 event 合并成一个 Stream Record, 这个过程叫 Aggregation. 多个 Stream Records 被 Collect 到一起, 打包并通过一个 Http Request (Kinesis API) 发送出去, 这个过程叫 Collection**. 打包的对象是 Stream Records.


Firehose Data Transformation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**什么时候使用 Firehose Delivery Stream 而不是 Kinesis Data Stream?**

当你不对数据做任何 Transform 之类的处理时, 使用 Data Stream, 只要做处理, 或是送给多个其他的目的地时, 就要用 Firehose Delivery Stream.

**Firehose 自带几种 Lambda 代码用于处理标准格式.**:

- **General Firehose Processing** — Contains the data transformation and status model described in the previous section. Use this blueprint for any custom transformation logic.
- **Apache Log to JSON** — Parses and converts Apache log lines to JSON objects, using predefined JSON field names.
- **Apache Log to CSV** — Parses and converts Apache log lines to CSV format.
- **Syslog to JSON** — Parses and converts Syslog lines to JSON objects, using predefined JSON field names.
- **Syslog to CSV** — Parses and converts Syslog lines to CSV format.
- **Kinesis Data Firehose Process Record Streams as source** — Accesses the Kinesis Data Streams records in the input and returns them with a processing status.
- **Kinesis Data Firehose CloudWatch Logs Processor** — Parses and extracts individual log events from records sent by CloudWatch Logs subscription filters.

**什么时候在 Firehose 中使用 Lambda?**

- Ref: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/lambda-preprocessing.html

- 转换为 Avro, ORC, Parquet 之外的 CSV, GZip 格式: Transforming records from other formats (such as KPL or GZIP) into formats that Kinesis Data Analytics can analyze. Kinesis Data Analytics currently supports JSON or CSV data formats.
- 改变 Schema, 比如把 Json flatten: Expanding data into a format that is more accessible for operations such as aggregation or anomaly detection. For instance, if several data values are stored together in a string, you can expand the data into separate columns.
- 跟已有的数据(比如 S3 上的)做 join, 连接更多的数据: Data enrichment with other AWS services, such as extrapolation or error correction.
- 使用复杂的逻辑操纵字符串: Applying complex string transformation to record fields.
- 对数据进行筛选: Data filtering for cleaning up the data.

以下两种格式转换的情况是 Firehose 的自带功能, 无需使用 Lambda.

- Transformation to Avro and Parquet Format
- Record Format Convertion


Kinesis Producer Library vs Kinesis Client Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

注意, 这里是 Client Library 而不是 Consumer Library.


Kinesis Producer Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KPL 能做什么:

- Batching, 批量, 异步发送数据
- 自动 Retry


3种写入的方法比较, Put Record, KPL, Kinesis Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Kinesis API Put Record**: 必须等待 Put 操作完成后才能执行后面的代码, 是一条一条的发送 Record.
- **Kinesis Producer Library**: 是一个 Java SDK, 支持 Batch 操作, 使用一个 Buffer 将多个 PutRecord 的操作合并到一起再发送, 而且主程序使用 KPL PutRecord 后无需等待就可以执行后面的代码了, KPL 会异步将数据发送到 Stream. 从而大幅提高吞吐量.
- **Kinesis Agent**: 是一个用于服务器上的日志文件的 Java 软件, 可以检测文件夹或是文件清单, 当文件发生变化时 (增加了新行), 则自动将新数据打入 Kinesis Stream 中. 免去了在你的 Application 中添加 Kinesis 代码的麻烦.


Shared Fan-Out vs Enhanced Fan-Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有下列事实:

- 1个 Shard 能提供 2MB/s 的读取速度. 如果有多个 Consumer 同时读取这个 Stream, 这个带宽由所有 Consumer 分享.
- 如果启用了 Enhanced Fan-Out 功能, 则允许一个 Consumer 独享一个 Stream 2MB/s 的读取速度.
- 如果用 API Consumer, 则可以 Subscribe individual shard.
- 如果用 KCL Consumer, 则自动 Subscribe all shard of the stream.


如何让多个 Consumer 同时读取一个 Stream, 并且数据一 available 就立刻读取?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

首先, 要注意 Stream 的读取数据有限制, 每秒, 每个 Shard 最多同时执行 5 个 GetRecords. 为了避免触发这个限制, Amazon 推荐每一个 Application 每秒钟 polling 一个 Shard. 尽量使用 Batch 获得更高的吞吐量.


Resharding 重新分片
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

你可以执行两种操作:

- Split Shard:
- Merge Shard:

**After Resharding**:

无论是你 将一个 Shard 再分片, 还是合并多个 Shard. **这个过程都不是瞬间完成的. 那么在这个过程中, Producer 和 Consumer 会受到什么影响? 以及相关的 Shard 上的数据又会被怎样移来移去呢?**

在你执行 Resharding 的过程中, Stream 是 Inactive 的. 你需要在你的代码中加入异常处理的部分, 当捕获到 Stream Inactive 的错误时, 要进行等待重试, 直到 Stream 恢复 Active.

定义 Parent Shard

- 在 Split Shard 中, 则那个被 Split 的 Shard 就是 Parent Shard
- 在 Merge Shard 中, 则两个被 Merge 的 Shard 都是 Parent Shard

开始执行 Resharding 时候, Parent 处于 Open State, 执行完了之后 Parent 处于 Close State, 当 Parent 过了 Retention Period 之后, 里面的数据已经无法 Accessible 了, 此时出于 Expire State.

执行 Resharding 之后, PutReocrd 到 Parent Shard 的数据会被 Route 到 Child Shard, 而 GetRecord 则会从 Parent 和 Child Shard 上读取数据.


2. Storage - S3
------------------------------------------------------------------------------

2. Storage - DyanamoDB
------------------------------------------------------------------------------


Global Secondary Index Overloading vs Sharding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这是两种通过构建 GSI 来优化查询的技巧.

- GSI Overload: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html. 简单来说, 由于 DynamoDB 是 Schema Free 的, 所以在同一个 Field 下, 我们叫他 Field2 好了, 值的类型可以完全不同. 通常情况下, 会有一列 Field1 表示该 Item 是属于哪种类型, 同类型 Item 的 Field2 的类型相同. 如果你使用 Field1 作为 Partition Key, Field2 作为 SortKey 建立 GSI, 则你可以对不同类的 Item 根据 Field2 做各种各样的查询.
- GSI Sharding: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-gsi-sharding.html. 举例来说你有 log event, event 有 uuid, time, type (error, debug, info, ...) 通常 uuid 肯定是 Partition Key. 如果 Partition Key 的变化非常大, 则会有非常多的实体机器 (可能 100 台), 而且 Item 的分部会非常散. 当你选择某个时间段内的所有 Error 日志时, 就算你对 time 建立了 Sort Key, 由于数据分散的很厉害, 合并的操作花费了很多时间, Sort Key 的利用率并不高. 但是如果你创建新的一列, 随机赋予了 1-10, 将此列作为 Partition Key. 然后将 type 和 time 合并在一起, 比如 ``ERROR-2018-01-01-06:00:00``, 作为 Sort Key, 建立 GSI. 那么新查询则只会用到 10 台机器, 而且对 Sort Key 的利用率会很高.




3. Processing - EMR (Elastic Map Reduce)
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


EMRFS (Elastic Map Reduce File System)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ref: https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-it-works-kinesis-video-api-producer-sdk.html

- Hadoop 原生的存储层是 HDFS (Hadoop File System), 是一个分布式的文件系统. 而亚马逊使用 S3 实现了 HDFS, 作为 EMR 的存储层.
- EMRFS 不支持 S3 Server Side Encryption, 只支持 Client Side Encryption.


Options to Launch Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 用 API (包括 Console): 默认情况下, 集群在工作完成后会自动关闭. 适用于实验性质或是单次工作.
2. 用 ALB 自动启动: 适用于生产环境, 集群在工作完成后不会自动关闭.


3. Processing - Data Pipeline
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

**Task Runner**:

Task Runner 是一个 Application, 不断的对 Data Pipeline 进行轮询 (Polling). Task Runner 是一个由代码定义的抽象概念. Pipeline 会启动 Instance 然后交给 Task Runner 执行.

**Data Nodes**:

Data Nodes 是 Data Pipeline 各个环节的 Input Output.

- DynamoDBDataNode
- SqlDataNode
- RedshiftDataNode
- S3DataNode

**Databases**::

- JdbcDatabase
- RdsDatabase
- RedshiftDatabase


3. Processing - Amazon Machine Learning
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

Amazon Machine Learning 使用预先编排好的训练策略, 只需要让工程师 (不需要很懂模型) 选择是哪一类的问题? 分类还是回归, 二元分类还是多类, 然后选择模型, 然后把数据喂给 AWS ML, 就可以创建模型了.

AWS ML 支持三种问题:

- Binary Classification:
    - Algorithm: Logistic Regression
    - Evaluation: AUC 曲线, Accuracy, Precision, Recall, False Positive Rate.
- Multi Classification Model:
    - Evluation: Macro Average F1 Score 作为模型指标, Confusion Matrix 作为 Visualization.
- Regression Model
    - Algorithm: Linear Regression
    - Evluation: RMSE


什么时候用 Amazon Machine Learning, 什么时候用 SageMaker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Amazon ML 是封装好的机器学习算法服务, 比如分类, 回归. 有成熟的 语音转文本, 文本转语音, 提取文本主题, 图像识别等. 然后通过 API 调用, 异步的批量预测, 或同步实时的单个预测. 目标用户是 不是很懂机器学习的的开发者.

而 SageMaker 实现了 ML 各个环节中的开发, 训练, 存储, 调参, 等环节, 是一个完整的机器学习平台, 但本身不提供具体的算法. 目标用户是 很懂机器学习的模型开发者.



3. Processing - Amazon Sage Maker
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

3. Processing - Amazon Lambda
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

3. Processing - Elastic Transcoder
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

- Ref: https://docs.aws.amazon.com/elastictranscoder/latest/developerguide/introduction.html?shortFooter=true

Elastic Transcoder 是一个多媒体视频转码服务. 主要用来实现视频网站. 用户的原始视频上传到 S3 时, 当访问的时候, 用户可以选择不同的清晰度, 客户端根据平台(手机, 电脑)选择不同的视频输出编码, 而 Elastic Transcoder 则在中间提供转码.

Elastic Transcoder 的重要概念有:

- Jobs: 一个任务.
- Pipelines: 一个 Queue, 比如转换为 1080P Mp4 可以是一个 Pipeline, 转换为手机的 3GP Mp4 可以是另一个 Pipeline, 当你创建 Job 时你要选择一个 Pipeline.
- Presets: 预定义的视频编码方式, 比如 MP4
- Notification:


3. Processing - AWS Glue
------------------------------------------------------------------------------


4. Analytics - Redshift
------------------------------------------------------------------------------

STL  和 STV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- STL (System Table for Logging): 储存了 Redshift 集群的各种系统级历史信息的日志, 比如执行过的 SQL.
- STV (System Table for View): 隔一段时间储存一次系统的数据的各种 Snapshot 信息(不包含数据本身, 只包含 Metadata).
- System Views: STL 和 STV 的子集, 保存了一些常用的关于系统的信息.
- System Catalogs Tables: 以 PG 开头的表, 储存了表的定义, 列的定义, Index 的定义.


Enable Encryption to existing Redshift Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你的 Redshift 还没有加密, 而你想以后都给数据加密, Redshift 有一个自带的服务可以暂时将你的 Cluster 设为 Read Only, 然后状态变为 Resizing, 然后自动为你启动一个新的 Cluster, 完成后自动切换 Endpoint. 你需要 Disable Cross Region Snapshot, 因为之后你不需要 Snapshot 了, 而新的 Cluster 一旦完成, 旧的就可以不要了, 需要关闭这个选项才能自动改删除旧的 Cluster.



4. Analytics - Elastic Search
------------------------------------------------------------------------------


Encryption at Rest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ref: https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/encryption-at-rest.html?shortFooter=true

如果你启用了 KMS Encryption at Rest, 下列数据将会被加密:

- Indices
- Automated snapshots
- Elasticsearch logs
- Swap files
- All other data in the application directory

下列数据 **不会被加密**, 但你可以采用别的方法保护这些数据:

- **Manual snapshots**: Currently, you can't use KMS master keys to encrypt manual snapshots. You can, however, use server-side encryption with S3-managed keys to encrypt the bucket that you use as a snapshot repository. For instructions, see Registering a Manual Snapshot Repository.
- **Slow logs and error logs**: If you publish logs and want to encrypt them, you can encrypt their CloudWatch Logs log group using the same AWS KMS master key as the Amazon ES domain. For more information, see Encrypt Log Data in CloudWatch Logs Using AWS KMS in the Amazon CloudWatch Logs User Guide.




4. Analytics - Athena
------------------------------------------------------------------------------


4. Analytics - Kinesis Analytics
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

- Ref: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/streaming-sql-concepts.html?shortFooter=true

Kinesis Analytics 是在 Stream 中运行的实时分析工具. 可以允许你使用类 SQL 语言对实时数据进行分析. 比如:

- 统计当前时刻的股价. 实时报警.
- 最近 1 小时内的股票交易统计数据.
- 每天统计 24 次, 每小时一次, 一小时内的交易量.


Streaming SQL Concepts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ref: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/streaming-sql-concepts.html?shortFooter=true

- Continues Query: 用于追踪实时数据, 比如当前的股票价格.
- Window Query:
    - Stagger Window: 交错窗, 多个窗口之间宽度可能不一致, 首位可能有重叠. 用于 VPC Flow Log.
    - Tumbling Window: 翻滚窗, 多个窗口之间首尾相连, 宽度大多数情况下是一致的. 比如每1分钟计算一次.
    - Slide Window: 滑窗, 窗口的宽度(时间区间一致), 不断的滑过去. 比如最近 5 分钟内的统计数据
- Stream Join:


In-Application Stream Time columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kinesis Anlalytics 实际上内部也是一个 Stream, 不过有一个虚拟的滑窗

- ROWTIME: record 被打入 Stream 的时间
- Event time: 物理上事件发生的真实时间, Client Side Time
- Ingest time: Server Side Time
- Processing time


- Ref: Timestamps and the ROWTIME Column: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/timestamps-rowtime-concepts.html

5. Visualization - QuickSight
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


QuickSight 中的概念
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Data Analysis**: 是创建和观看 Visuals 的系统.
- **Visuals**: 一个可视化图表.
- Insights: 对数据的解读.
- Sheets: set of visuals in a single page.
- **Stories**: 一连串的 Visuals 所构成的故事.
- Dashboard: 一个 Read Only snapshot of Data Analysis.
- **Spice**: 是一个 基于内存的 并行 计算引擎. https://docs.aws.amazon.com/quicksight/latest/user/welcome.html?shortFooter=true#spice
- Data Source: 一个数据源, S3, RDS, 或者用户上传的数据.
- Datasets: 一个数据源的指定部分, Dataset 同时也包含了你对 Data Source 做的所有 Preparation, 包括 transform, rename.


QuickSight 所支持的数据源
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Amazon Athena
- Amazon Aurora
- Amazon Redshift
- Amazon Redshift Spectrum
- Amazon S3
- Amazon S3 Analytics
- Apache Spark 2.0 or later
- MariaDB 10.0 or later
- Microsoft SQL Server 2012 or later
- MySQL 5.1 or later
- PostgreSQL 9.3.1 or later
- Presto 0.167 or later
- Snowflake
- Teradata 14.0 or later


Visualization 的概念和图表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Topic (重要的概念):

- Measures and Dimensions in Vxisuals: 在决定使用哪种类型的图表时, 首先要考虑你的数据里有多少个 dimension, 所谓 dimension 就是数据有多少列, 不同的列就算是 1 个 dimension. 简单来说时间序列就是 2 dimensions, Time, Value.
- Display Limits in Visuals

Graph Type:

- 各种图表类型的 AWS 官方文档: https://docs.aws.amazon.com/quicksight/latest/user/working-with-visual-types.html
- AutoGraph: 让 QuickSight 自动选择哪种图表.
- Bar Charts: Single Measure,
- Combo Charts: 混合型, 例如 Bar + Line
- Donut Charts: 甜甜圈 (环装) One Value Single Dimension
- Gauge Charts: 计量表 (体重计的图形)
- Geospatial Charts (Maps)
- Heat Maps
- KPIs: KPI指标, 一条横杠, 看达成了多少
- Line Charts
- Pie Charts
- Pivot Tables:
- Scatter Plots: 点图
- Tables as Visuals: 二维数据表本身作为 Visual
- Tree Maps: 由很多不同大小的矩形组成


让用户控制数据子集
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有一个很常见的需求, 你建立了一个时间序列的可视化, 用户想要能够自定义这个时间区间, 但是用户不希望自己写 SQL. 此时你可以为你的可视化创建两个 Parameter (参数), start, end, 然后创建一个 Control (控制) 控件让用户自行调整.




5. Visualization - Data Visualization Tools
------------------------------------------------------------------------------



6. Security - Access
------------------------------------------------------------------------------

6. Security - Auditing
------------------------------------------------------------------------------

6. Security - Encryption
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

只要讨论到加密的话题, 都有 Encryption at Rest 磁盘存储加密 和 Encryption at Transit 传输过程加密两种. 无论哪种加密, 都有 Server Side 和 Client Side 两种方式. Server Side 加密主要是防止有敏感信息数据被拖库. Transit 主要是防止数据拦截和监听.


Kinesis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :depth: 1
    :local:




Redshift
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :depth: 1
    :local:

- Ref: https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-db-encryption.html

- 在启用加密之后的 Cluster 的 Snapshot 自动都是加密的.
- 任何时候, 只要你愿意手动操作, 你都可以使用 KMS 进行 Client Side Encryption, 当然是对每个 Column 中的数据分别加密.


Rest Encryption - 新的 Cluster 启用加密
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- 支持 Server Side S3 Managed Key 加密.
- 支持 Server Side Encryption, 使用 AWS Managed Key, Customer Managed in KMS.
- 也可以用其他 AWS Account 上的 KMS Key, 只要你在 Policy 中设置了权限.
- 如果你的企业要求对加密使用的密钥有完全的控制权, 你也可以用 On-Premised Key (你自己数据中心的), 或是 Hardware Security Module (HSM 硬件加密). 有两种方法能让 Redshift 使用你的密钥:
    1. 在你的数据中心网络和 VPC 之间建立 VPN 连接.
    2. 使用 Client and Server Certification 建立可信连接, 连接 Redshift 和你的 HSM.


Rest Encryption - 已有的无加密 Cluster 启用加密
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- 如果使用 AWS Manged Key 或是 Customer Managed Key in KMS (总之在 AWS 上), Redshift 会启用新的 Cluster, 并且自动将 Cluster Migrate 到新的 Cluster 上, 此时原来的 Cluster 会变成 Read Only. 无需手动 Migrate 数据.
- 如果使用的是 HSM, 那么你需要手动 UNLOAD 和 Load


Rest Encryption - 加密 Redshift Unload 的数据
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Unload 是将查询结果中的大量数据 dump 到 S3 的操作, 有时我们需要对其加密.

1. S3 Server Side with KMS Keys
2. Client Side Encryption with a custom-managed-key
3. default AWS encryption

Unload **不支持** Server Side custom-managed-key


Transit Encryption
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. 在 JDBC/ODBC SQL Client 和 Redshift 之间传输加密: 你需要使用 Security Socket Layer (SSL), 然后使用 Amazone Certificate Manager (ACM) 管理证书.
2. Redshift 和 S3, DynamoDB 之间传输加密: Amazon 使用 SSL 在传输过程中加密, 对于 S3 和 DynamoDB, 可以用 KMS 进行 Server Side Encryption.
3. AWS CLI, SDK, API Client 与 Redshift 之间传输加密: 可以创建 Redshift Https endpoints, 提供一个 redshift 专用的 URL 作为 endpoint, 然后通过 HTTPS 对传输中的数据进行加密.



Snapshot - 将已加密的 Snapshot 拷贝到其他 Region
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

你必须要允许 Redshift 使用在 Destination Region 上的 Master KMS Key. 因为拷贝加密副本的过程其实是, 在原 Region 解密, 拷贝到目标 Region, 再加密.


Snapshot - 灾难恢复
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- Snapshot 是数据库级操作, 保存了整个数据库的快照, (压缩过后的数据)
- 你可以选择将从 Snapshot 中恢复整个数据库, 本质上是创建一个新的设置一摸一样的数据库, 然后拷贝数据.
- 也可以选择从 Snapshot 中恢复一个表, 你需要创建一个新的表, 然后把数据存到里面去.


