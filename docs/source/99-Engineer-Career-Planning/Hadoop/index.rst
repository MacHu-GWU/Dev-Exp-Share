
背景:

Google 在 2003 年发表了三篇重磅论文, 建立了大数据的基础:

1. Map Reduce: MR 大数据计算框架 - https://posts.careerengine.us/p/5a0a552c3c4cad02dbc40e39
2. Google FS (GFS): 分布式文件系统 - https://posts.careerengine.us/p/5c1f17f86f311d533b55a93e
3. Big Table: 分布式高性能查询系统 - https://posts.careerengine.us/p/5c1d39514a71552daec78cbe

三者在 Google 内部都有具体的实现, 而这些并不是开源的. 而开源社区 Apache 基金会则借鉴了论文中的设计思想, 在 2006 年使用 Java 实现并开源了 Hadoop.

Hadoop 同样也有三剑客:

1. Hadoop Map Reduce 对应 Google MR
2. HDFS (Hadoop File System) 对应 GFS
3. HBase 对应 Big Table

Hadoop V1 和 V2 版本的变迁历史, Yarn 和 Zookeeper 两个关键组件:

在 V1 版本中, Hadoop 使用的是 Single Master Multi Slave 的模型, 使用 Job Tracker 来调度集群上的计算资源 (Resource) 以及运算工作 (Job, Task). 但是 Single Master 存在单点故障的问题, 所以会有一个 Backup Master, 当从 Master 收不到 Heartbeat 的回复时, 就会接管 Master. 但是这个机制仍然不够稳定, 经常会出现收不到 Heartbeat, 但是 Master 其实没有真正挂掉, 或者 Backup Master 信息滞后, 状态不一致的现象.

所以在 V2 版本中, Hadoop 把 Job Tracker 的功能拆分成 Resource Manager, 实现的工具叫 Yarn (Yet another resource negotiator) 用于管理运算资源的分配, 但不负责调度 Job, 比如创建为 Job 分配 Container (这个和容器不是一个东西, 但是解决的问题类似, 都是从宿主机器上划分资源). 而 Yarn 本身也是有单点故障的问题的, 所以由雅虎研究院研究院开发出来了 Zookeeper, 并捐给了 Apache 基金会. Zookeeper 是一个高可用性, 强一致性的配置管理服务. 保证在部署在集群上时, 保证调度的配置强一致, 并全序. Zookeeper 解决的是分布式系统中的集中式强一致配置管理问题. Yarn 把调度的配置存在 Zookeeper 上, 而 Yarn 的 Master Node 也由 Zookeeper 进行管理, 保证同一时间总是有且只有一个 Master Node.

Hadoop 社区经过多年的发展, 也出现了非常多的工具:

- Yarn: cluster 集群管理工具 - https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html
- Zookeeper: 一个分布式的协调框架