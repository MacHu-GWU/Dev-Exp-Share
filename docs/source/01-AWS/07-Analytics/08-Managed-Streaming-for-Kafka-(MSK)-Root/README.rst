Managed Streaming for Kafka (MSK)
==============================================================================


What is Kafka
------------------------------------------------------------------------------

- Linkedin 开发的开源软件
- 分布式消息系统, 实现 发布 / 订阅 模型
- 支持 FIFO, fault-tolerant

重要概念:

- Producer
- Topic
- Broker
- Consumer

Partition:

- Partition
- Replicas of partition
- Leader

- Zookeeper


部署 AWS MSK 集群
------------------------------------------------------------------------------

MSK 是 AWS 的 Kafka 托管服务, 几下点击或者 API Call 就能启动一个 Kafka 集群, 并且能够 Scale Up and Down.

MSK 的部署有几点限制:

1. 你的 Producer 和 Consumer App 都需要位于 Kafka 集群所在的 VPC 以内才能与之通信. 根据 `AWS MSK Architect 架构图 <https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html>`_ AWS 会为每个 MSK 集群分配一个对用户不可见的 VPC, 并且真正的 Zookeeper 调度服务就发生在这个上面. 如果不在一个 VPC 内, 是无法路由跟 Zookeeper 通信的. 如果你的 Producer / Consumer 不在 MSK VPC 上, 那么你需要进行 VPC Pair 或是 Direct Connect 才能使用 MSK.


配置你的客户端程序
------------------------------------------------------------------------------

这里的 客户端程序 既可以是 Producer 也可以是 Consumer

请参考 https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html 官方文档. 总的来说你需要这么几步:

1. 安装 java, java 是 kafka bin tool 的依赖
2. 安装 kafka client java 程序
3. 用 AWS CLI 获得 zookeeper connection str 和 Broker Node Endpoint
4. 用 kafka java 程序 创建 Topic
5. 配置跟你编程语言相关的 kafka 客户端程序, 我习惯用 kafka python.