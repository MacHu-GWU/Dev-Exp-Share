AWS工具名称速查
==============================================================================

在 AWS Certification 的考试中, 很多工具名词是只需要知道它是干什么的, 并不需要知道其细节的. 本文档列出了大量 AWS 考试中涉及的工具名称, 便于查找.


IOT 相关
------------------------------------------------------------------------------

- **Device Shadow**: 是一个 JSON Document, 记录了 Device 的当前状态. 官方原话: Device Shadow is a JSON Document used to store and retrieve current state information for a device. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.
- **Device Shadow Service**: 是一个服务, 维护所有 Device Shadow (相当于一个数据库). Device Shadow Service Provides persistent representation of your devices. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.
- **Rules engine**: 一个规则引擎, 使用 SQL 类似的语言从 Message Payload 中选择数据, 然后使用其他 AWS 服务来处理数据, 比如用 Lambda 将数据存入 DynamoDB.
- **GreenGrass**: 可以在 Device 上安装的 SDK 软件, 在 Local 机器上创建虚拟的 AWS 环境, 在本地运行 AWS Lambda 等. Bring local compute, messaging, data caching, sync, and ML inference capabilities to edge devices.



EMR 相关
------------------------------------------------------------------------------

- **Apache Hue (Hadoop User Experience)**: 一个开源的, 类似于 SQL Query Client 的图形界面, 用于执行 Hive Query, Pig Script, Impala 以及其他 Hadoop 组件的软件. 关键字: Graphical User Interface.
- **Apache Yarn (Yet Another Resource Negotiator)**: 管理 Hadoop 集群的协调管理器.
technology in the open source Hadoop distributed processing framework. ... YARN stands for Yet Another Resource Negotiator, but it's commonly referred to by the acronym alone; the full name was self-deprecating humor on the part of its developers.
- **Apache Tez**: 构建于 Apache YARN 之上, 将 Map 操作拆分成 Input, Processor, Sort, Merge, Output; Reduce操作拆分成 Input Shuffle, Sort, Merge, Output; 然后组装成一个 DAG 有向图任务. 是一个 Application Framework.
- **Apache Flink**: 一个流数据的处理框架, 比 Spark 新, 对标 Spark, 是新一代的流数据处理大数据引擎. 关键字: Streaming Dataflow Engine
- **Apache Spark**: 大数据分析引擎, 一个基于内存的并行计算引擎, 可以理解为高速度的 Hadoop. 底层数据结构是 RDD. 关键字: unified analytics engine for large-scale data processing
- **Apache Phoenix**: 允许用户使用 SQL 查询 Hbase 的查询工具. 类似于 psql 的命令行. 关键字: OLAP and operational analytics.
- **Apache HCatalog**: Hive Metastores Tables, 用于保存数据的 Schema 以及 Metadata.
- **Apache ZooKeeper**: 中心化的配置管理, 同步工具. Apache ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
- **Apache Sqoop**: 在 S3, Hadoop, HDFS, RDBMS 之间传数据用的. Apache Sqoop is a tool for transferring data between Amazon S3, Hadoop, HDFS, and RDBMS databases.
- **Apache Zeppelin**: 和 Python Jupyter Notebook + Bokeh 类似, 提供了交互式的数据探索界面, Use Apache Zeppelin as a notebook for interactive data exploration.
- **Apache Mahout**: Hadoop 上的机器学习框架. A machine learning framework for Apache Hadoop.
- **Apache Livy**: 通过 Rest API 跟 EMR 上的 Spark 交互. Livy enables interaction over a REST interface with an EMR cluster running Spark. You can use the REST interface or an RPC client library to submit Spark jobs or snippets of Spark code, retrieve results synchronously or asynchronously, and manage Spark Context.
- **Ganglia**: EMR 集群的性能监控工具. The Ganglia open source project is a scalable, distributed system designed to monitor clusters and grids while minimizing the impact on their performance.
- **Apache Oozie**: 安排, 协调 Hadoop Jobs, Use the Apache Oozie Workflow Scheduler to manage and coordinate Hadoop jobs.
- **Apache Flume**: 分布式的, 移动大量日志数据的工具. a distributed, reliable, and available software for efficiently collecting, aggregating, and moving large amounts of log data. It has a simple and flexible architecture based on streaming data flows.


Redshift 相关
------------------------------------------------------------------------------

- **Spectrum**: 使用 Redshift 底层的查询引擎, 查询 Redshift 外的数据 (比如 S3)的一个工具.


QuickSight 相关
------------------------------------------------------------------------------




Athena 相关
------------------------------------------------------------------------------

- **Presto**: 是一个开源的分布式的 SQL 引擎, 由 Facebook 开发.
- **DDL**: Data Definition Language
- **DML**: Data Manipulation Language
- **DCL**: Data Control Language
- **TCL**: Transaction Control Language


Machine Learning 相关
------------------------------------------------------------------------------

- **Comprehend**: 从该文本中提取主题, 自然语言处理服务.
- **Rekognition**: 从图像和视频中国提取物件, 图像识别服务.
- **Amazon Transcribe**: 从音频中提取文本, 语音识别即服务. 语音转文字. 和 Polly 相反.
- **Polly**: 将文字转化为语音. 和 Transcribe 相反.
- **SageMaker**: 机器学习即服务.