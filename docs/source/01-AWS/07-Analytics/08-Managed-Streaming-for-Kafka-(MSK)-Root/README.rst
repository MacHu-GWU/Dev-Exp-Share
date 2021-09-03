Kafka and AWS MSK (Managed Streaming for Kafka)
==============================================================================

.. contents::
    :depth: 1
    :local:


理解 Kafka, 以及 AWS MSK 服务.
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


什么是 Kafka
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Kafka 是**:

- Linkedin 开发的大数据中间件. 后捐给了 Apache 基金会开源.
- 分布式消息系统, 实现 发布 / 订阅 模型.
- 具有 超大吞吐量, 高可用, 数据持久化 等特性.
- 支持 FIFO, 支持消息严格有序性.

**Kafka 中的重要概念**:

- Zookeeper: 一个开源的分布式强一致的元数据管理软件, 用于为分布式系统提供一个高可用, 强一致的元数据管理, 以实现分布式系统的状态查询和调度. Kafka 和 Hadoop 都依赖于 Zookeeper. 不过在 Kafka 3.0 版本中, 社区要推行去 Zookeeper 化, 因为为了部署核心业务还要同时部署一个 Zookeeper 并运维实在是太痛苦了. 所以社区希望用 Sidecar 模式, 即在每一个 Broker 机器上运行一个轻量的服务 Quorum, 用 Raft 一致性协议管理元数据.
- Kafka Cluster: 一个包含多个 Broker 服务器的集群.
- Broker: 负责维护 Topic, Subscription, 接收 Producer 的数据. 一个 Broker 就是一台位于 Kafka Cluster 中的服务器.
- Replication: Kafka 使用的是主从分布式模型, 也就是说同一时间只有一个 Leader, Leader 挂掉后 Follower 会选举出 Leader, 并自动或恢复挂掉的服务器. 从而保证服务的高可用, 以及数据的持久化 (总有 Broker 能提供服务, 数据在所有 Broker 上都有副本)
- Topic: 一个逻辑上的抽象, 发布 / 订阅 都必须指定 Topic. 从而使得一旦有数据发布到 Topic, 所有的订阅者都会收到数据.
- Partition: Topic 的分区, 一条消息会被负载均衡算法分配到一个 Partition 上, Partition 的数量可以是 1 或是多于 Broker 的数量, 使得每个机器上的负载比较均衡. Partition 在文件系统上的表现就是一个文件夹.
- Producer: 一个客户端程序, 不断像 Kafka 发送数据. 比如 Web 服务器不断发送日志.
- Consumer: 一个客户端程序, 跟 Kafka 订阅一个 Topic 并保持连接, 有新数据进来则会立刻收到并处理.
- Consumer Group: 一个 CG 由多个 Consumer 组成. 可以有多个 CG Subscribe 一个 Topic. 此时每个 CG 都会收到相同的消息的副本. 一个 Topic 上的所有消息将会被分散到 Consumer 上进行处理, 一条消息在一个 CG 内只会被一个 Consumer 进行消费. 并且一个 Partition 上的数据都会被导向到同一个 Consumer 上. 不会出现一个 Partition 上的数据被分散到不同的 Consumer 上的情况. 该设计是为了提高吞吐量.


什么是 AWS MSK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MSK (Managed Streaming for Apache Kafka) 是 AWS 的 Kafka 托管服务. 通过几下点击或者 API Call 就能启动一个 Kafka 集群. 相比之下手动配置 Kafka 需要做这么多事:

1. 部署 zookeeper cluster, 这在 Kafka 3.0 正式去 zookeeper 化之前是必须的.
2. 部署 Kafka Cluster 集群, 虚拟机, 网络, 磁盘, 安全 等.
3. 在每台机器上安装 Kafka 服务端, 并且配置服务, 自动启动, 相互发现 等.

一个 MSK 的启动时间大约在 15 分钟左右.


MSK 架构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通过阅读 Apache https://Kafka.apache.org/ 官方文档可以了解到 Kafka 的部署主要有两个集群:

1. zookeeper 集群 (3.0 以后就不推荐了, 社区正在努力去 Zookeeper 化, 希望用随着 Kafka 服务端的分布式一致性组件来部署, 避免部署两个集群), 用于提供 distributive consistency 的 metadata 服务
2. Kafka 集群, 每台机器上都安装了 Kafka 服务端.

而 AWS 的 MSK 架构也差不多, 唯一不同的是 MSK 启动 Cluster 的时候, Zookeeper 的集群并不会部署到用户的 VPC 内. AWS 估计是维护了一个巨大的 zookeeper 的池子, 用多租户模式对外进行服务. 需要的时候 AWS 内部 VPC 跟用户的 pair 一下并更新路由, 让用户 VPC 内的 Kafka 集群能够跟 zookeeper 通信即可. 这样的设计可以减少在启动 MSK Cluster 时维护 Zookeeper 的麻烦, 减少启动时间.

由于这个设计, **因为 Client 需要跟 zookeeper 通信以获得 broker 的状态信息, 所以 Client 必须要在 VPC 以内**. 比如有的人会想从自己家的网络访问 Kafka, 想要通过修改 Kafka Cluster 的 Security Group 的方式允许自己连接到 Kafka, 可这样并不能连接到 Zookeeper. 所以这种方式是无效的. **不过你如果非常从 VPC 外访问, 那么进行 VPC Pair 或是 Direct Connect 即可**.


Kafka 设计细节
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


点对点模式 vs 发布订阅模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这两种模型都是事件驱动中常用的模式.

点对点模式:

Producer 将消息发送给队列, 队列不会主动通知 Consumer, 而 Consumer 通过 轮询 (Pooling 隔一段时间就去查一下有没有数据) 的方式从 Queue 中拉取数据, 所以 Consumer 需要额外的线程去控制拉取消息的频率. 被 Consumer 正在某一个 Consumer 处理的数据对其他 Consumer 是不可见的. 这也就是说同一条消息只有一个 Consumer 在处理.

发布订阅模式:

Subscriber 和 Broker 建立长连接. 每当 Publisher 将消息发送给 Broker (Topic), Broker 则会将数据发送给所有 订阅了该 Topic 的 Subscriber. 也就是说所有的 Subscriber 都会对该消息进行处理. Subscriber 无需主动询问 Broker 即可获得数据. 但是反过来 Subscriber 的无法控制自己处理的节奏, 只能被动的跟上推送的节奏, 如果消费的速度跟不上推送的速度, 则会发生问题.

根据描述可知 **点对点模式适合每一条消息严格需要被处理一次的情况. 发布订阅模式适合每一条消息要被不同的业务逻辑处理的情况**.

AWS SQS 就是标准的点对点模式, 需要在 Consumer 函数中控制 Pull 的节奏. 但是 SQS 允许触发 AWS Lambda, 该情况下又变成了发布订阅模式. AWS Kinesis 也是标准的点对点模式, Consumer 需要自己控制节奏. 但 Kinesis 允许用多个 Firehose + Lambda 的模式触发 Consumer 业务逻辑, 该情况下就成了发布订阅模式.

**AWS Kafka 则是标准的 发布订阅 模式**.


MSK 的高可用性和安全性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 服务高可用性 是通过让 Broker 在不同的 Availability Zone 实现的.
- 数据高可用性 则是通过 Replica 机制 让数据在不同的 Availability Zone 之间进行备份, 以及通过 Partition 机制让数据分流到多个 Broker 机器上来保证的.
- 数据存储安全性则是通过 Encryption at rest 直接对 EBS Volume 加密实现的.
- 数据传输安全性则是通过 SSL 加密, 保证客户端到服务端, broker 到 broker 之间的通信数据加密.

Kafka跟高可用性的架构:

- Cluster: 一个 Kafka 集群包含很多 Broker 机器, 通常一台 EC2 就是一个 Broker
- Broker / Instance: 一个 Broker 可以处理很多 Topic, 一个 Topic 可以分为很多 Partition, Partition 本质是


Kafka 数据持久化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

比如你有 2 个 broker, 一个 Topic 有 4 个 Partition, 我们来看一下 **数据在磁盘上是如何存储的**::

    b1@/t1/p1/seg1/000000000000000000000000.log
    b1@/t1/p1/seg1/000000000000000000000000.index
    b1@/t1/p1/seg1/000000000000000000000000.timeindex
    b1@/t1/p1/seg1/000000000000000000368795.log
    b1@/t1/p1/seg1/000000000000000000368795.index
    b1@/t1/p1/seg1/000000000000000000368795.timeindex
    ...
    b1@/t1/p3/seg1/000000000000000000000000.log
    b1@/t1/p3/seg1/000000000000000000000000.index
    b1@/t1/p3/seg1/000000000000000000000000.timeindex
    b2@/t1/p2/seg1/000000000000000000000000.log
    b2@/t1/p2/seg1/000000000000000000000000.index
    b2@/t1/p2/seg1/000000000000000000000000.timeindex
    b2@/t1/p4/seg1/000000000000000000000000.log
    b2@/t1/p4/seg1/000000000000000000000000.index
    b2@/t1/p4/seg1/000000000000000000000000.timeindex

b = broker, t = topic, p = partition, seg = segment; ``.log`` 保存了消息数据, 每一行是一条消息. 例如 ``00...00.log`` 保存了 offset 从 0 ~ 368795 的数据 . ``.index`` 和 ``.timeindex`` 文件则是索引文件, 一个是 offset - 磁盘寻址 索引, 一个是 时间戳 - 磁盘索引.

**而 offset 则是 Kafka 中非常重要的概念**. 你的 Consumer 在消费时是要指定 offset 的, 表示消费者从哪里开始消费. 而根据 offset 寻址的操作在 Kafka 上是 O(1) 的复杂度, 所以无论你的数据量有多少, 或是你的 offset 是多少, 总体上无论从哪里消费是一样的.

由于 Kafka 的数据都会被编码为 binary, 所以 .log 文件是无法直接打开的. 里面的格式是每一行是一条消息. 每一行包含了 body, size, offset, compress type 等信息.

无论消息是否被消费, Kafka 都会保存所有的消息. 这点和 Message Queue 有很大的不同, 比如 AWS SQS 是需要 Consumer 在消费完毕之后告诉 Queue 删除消息的. 而在 Kafka 中消费完毕之后只会 Commit 标记 Offset, 从而使得 Consumer 挂掉恢复后从上一次 Commit 后的 Offset 开始消费, 并不会删除消息. Kafka 中删除就消息的策略是这样的:

1. 基于时间, 默认配置是 168 小时 (7 天)
2. 基于大小, 默认配置是 1073741824 Bytes (1TB)

由于根据 offset 寻址的操作在 Kafka 上是 O(1) 的复杂度, 所以这里删除过期的文件并不会提高Kafka的性能.


严格有序化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

维护 Topic 级别的全局有序的成本是很高的因为 Topic 下的数据量根据应用的不同可以很大. Kafka 支持 Partition 级的严格有序, 因为一个 Partition 所占据的数据量是可以保证在一个比较小的范围内的, 那么就可以针对这个数量级进行优化, 从而实现 Partition 内严格有序.


生产环境中的消费策略
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




启动和配置 MSK Cluster
------------------------------------------------------------------------------


1. 为 MSK Cluster 创建 VPC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

配置你的客户端程序
------------------------------------------------------------------------------

这里的 客户端程序 既可以是 Producer 也可以是 Consumer

请参考 https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html 官方文档. 总的来说你需要这么几步:

1. 安装 java, java 是 Kafka bin tool 的依赖
2. 安装 Kafka client java 程序
3. 用 AWS CLI 获得 zookeeper connection str 和 Broker Node Endpoint
4. 用 Kafka java 程序 创建 Topic
5. 配置跟你编程语言相关的 Kafka 客户端程序, 我习惯用 Kafka python.