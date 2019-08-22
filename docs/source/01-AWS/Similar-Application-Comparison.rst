Kinesis Stream vs Spark Stream

1. Kinesis 可以一条条的处理信息, 而 Spark Stream 只能够 Batch 批量处理.


SQS vs Kinesis Stream:

1. SQS 没有 Sharding, 吞吐量没有 Kinesis 大.
2. SQS 常用于不是马上就要 Consume 的场景, 通常会有延迟.
3. SQS 的 Payload Size 上限是 256 KB.
4. SQS 的 FIFO Queue 可以保证保证顺序, Kinesis Stream 也可以保证顺序.

EMR 里的工具:

- Ganglia: 一个用于监控 EMR 集群的性能的分布式开源系统.
- Yarn (Yet Another Resource Negotiator): 用于管理 EMR 集群上的资源.
- Zeppelin: 一个和 Jupyter Notebook 类似的 Notebook 应用.
- Mahout: Machine Learning Framework for Apache Hadoop
- Hue (Hadoop User Experience): 一个开源的, 用于管理 EMR 和 Hadoop 集群的图形界面应用.



- Presto: 开源的分布式 SQL 查询引擎. Redshift 和 Athena 背后的引擎.

AWS 里看到文字无法立刻联想到功能的工具:

- Flume
- GreenGrass: Bring local compute, messaging, data caching, sync, and ML inference capabilities to edge devices.
- Snowball:

- HighChart: Javascript library for visualization
- Chart.js: Javascript library for visualization