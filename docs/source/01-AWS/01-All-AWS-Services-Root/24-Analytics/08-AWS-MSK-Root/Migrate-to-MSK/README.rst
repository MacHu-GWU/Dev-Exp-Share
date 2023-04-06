前言
------------------------------------------------------------------------------
Kafka 很香, 但是配置并维护一套 Kafka 集群并不容易, 在 On-prem 维护 Kafka 集群有如下痛点:

1. 为很多服务器安装软件, apply 配置文件是很麻烦的工作, 即使用 Ansible 还是很麻烦.
2. 为 Scale up/down 不容易, 因为你要添加并配置新机器, 这个工作很费时间, 所以 Scale 的过程很难做到很快.
3. 实现 high availability 不容易, 你要维护集群, 掉线等问题.
4. 备份容灾自己实现不容易.
5. 为生产环境配置 Cluster 监控系统很麻烦.

这段来自于 `这篇博文 <https://aws.amazon.com/blogs/big-data/how-goldman-sachs-migrated-from-their-on-premises-apache-kafka-cluster-to-amazon-msk/>`_ 的话概括了自己配置 Kafka 的痛点

    However, Apache Kafka clusters can be challenging to set up, scale, and manage in production. When you run Apache Kafka on your own, you need to provision servers, configure Apache Kafka manually, replace servers when they fail, orchestrate server patches and upgrades, architect the cluster for high availability, ensure data is durably stored and secured, set up monitoring and alarms, and carefully plan scaling events to support load changes.

AWS MSK 是 AWS 推出的 Kafka 托管服务, 解决了以上痛点并提供了很多云原生的功能.


本文要解决的问题
------------------------------------------------------------------------------
假设一个大公司主要依赖自己 host 在 on-prem 的 Kafka 负责数据流处理. 现在已经有很多 Producer / Consumer 以及 Service 依赖于这个 Cluster 在跑了. 这些 Producer / Consumer 有的在 On Prem, 有的已经在 AWS Cloud 上. 现在我们想要将 on-prem Kafka 迁徙到 AWS MSK, 同时尽量减少 Service Downtime, 请问该如何做?


迁徙到 MSK 要考虑哪些问题?
------------------------------------------------------------------------------
1. 我们是否也要迁徙 Producer / Consumer?

    在本文中我们不讨论这个, 而是把重点放在迁徙 MSK 上. 我们假设 Producer / Consumer 在迁徙过程中还是运行在原来的环境中, 只会有一些 Redeployment, Configuration 的变动.

2. 网络连接

    首先 MSK 必须跑在 AWS VPC 里的. 那么会有很多之前 On-prem 里的 Producer / Consumer 需要跟 MSK 通信, 那么我们需要用到以下技术

    1. `AWS Direct Connect <https://aws.amazon.com/directconnect/>`_: 让 ISP (Internet Service Provider) 在你的 On-prem 和 AWS Data Center 之间拉一条专线, 使得 On-prem 和 AWS 之间的通信不会经过 Public Network. 同时也保证跟 AWS 通信的延迟和之前 On-prem 内部通信的延迟一致. **这个主要是解决以前位于 On-prem 的 Producer / Consumer 和 MSK 通信的问题**.
    2. `AWS VPC Peering <https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html>`_: 让两个 VPC 联通起来, 从用户的角度看就是将两个 VPC 变成了一个 VPC. 常用于位于两个不同的 AWS Account 上的 VPC 之间的相互通信. **这个主要是解决以前位于已经存在的 AWS Account 上的 Producer / Consumer 和新建的 AWS Account 上的 MSK 相互通信的问题**.
    3. `AWS Private Link <https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc>`_: 当你的服务 Call AWS API 的时候例如 S3 PutObject 的时候, 通常你的 API 请求会通过公网抵达时 S3 service api endpoint. 有的用户需要数据不走公网, 那么这时就要为这些 AWS Service Endpoint 原本在公网上的服务创建一个 VPC Endpoint, 这样从 VPC 内部与这些 Service 通信就是走私网了. 通常是和 S3 / Dynamodb / Load Balancer 配合使用. **这个主要是解决 Producer / Consumer 对 S3 或是 Dynamodb 读写的问题**.



MSK 有四种 Authorization 机制:

1. IAM Policy.
2. Mutual TLS Authentication, 就是 HTTPS 协议里的 TLS, 需要 CA 证书.
3. SASL / SCRAM (Simple Authentication and Security Layer/ Salted Challenge Response Mechanism), 就是基于账号密码的验证.
4. Kafka ACLs (Access Control List). 本质上就是 Kafka 自带的 IAM, 也有 Principal / Resource / Action 的概念, 不过这里的 Principal 都是 CN (canonical name), 也就是 DNS 地址. 这是一种基于网络的验证手段.

除此之外, MSK 本身是 EC2, 那么 Security Group 也可以提供网络级别的管理. 同理 VPC ACLs 也能提供类似的权限管理.


我们来考虑 MSK 的

位于 On Prem 网络中的 Producer 和 Consumer 如何与 MSK 相连?
------------------------------------------------------------------------------

    由于网络

    1. AWS
    2. AWS Certificate Manager

位于 AWS Cloud 中的 Producer 和 Consumer


Cluster 迁徙
------------------------------------------------------------------------------


Topic 数据迁徙
------------------------------------------------------------------------------


Producer 和 Consumer 迁徙
------------------------------------------------------------------------------
1. 先迁徙 Producer, 再迁徙 Consumer, 不使用 Mirror Maker

指先将生产消息的业务迁移到新的 Kafka, 原 Kafka 不会有新的消息生产. 待原有 Kafka 实例的消息全部消费完成后, 再将消费消息业务迁移到新的 Kafka, 开始消费新 Kafka 实例的消息.

1. 将生产客户端的 Kafka 连接地址修改为新 Kafka 实例的连接地址.
2. 重启生产业务, 使得生产者将新的消息发送到新 Kafka 实例中.
3. 观察各消费组在原 Kafka 的消费进度, 直到原 Kafka 中数据都已经被消费完毕.
4. 将消费客户端的 Kafka 连接地址修改为新 Kafka 实例的连接地址.
5. 重启消费业务, 使得消费者从新 Kafka 实例中消费消息.
6. 观察消费者是否能正常从新 Kafka 实例中获取数据.

优点:

- 本方案为业界通用的迁移方案, 操作步骤简单, 迁移过程由业务侧自主控制, 整个过程中消息不会存在乱序问题, 适用于对消息顺序有要求的场景.

缺点:

- 但是该方案中需要等待消费者业务直至消费完毕, 存在一个时间差的问题, 部分数据可能存在较大的端到端时延.
- 由于要直接修改已经在运行的 Producer 和 Consumer, 如果迁徙准备不足导致迁徙过程中出错, 则会丢失数据.

总结:

- 适合堆延迟不敏感, 但是对顺序有要求的场景. 例如 E-Commerce 订单验证发货处理. 下单后有充足的时间确认后发货. 但是必须按照先验证用户是否付钱了, 仓库里是否有数据, 然后通知物流发货这样的顺序进行.

改进:

- 修改 Producer 的 Application Code. 不要将 Bootstrap Server 和 Topic 写死, 从外部存储中比如 AWS Parameter Store 中读取参数. 隔一段时间就检查 Parameter Store 的参数是否有更新, 如果有就读取新的 Parameter 并开始将数据写入到新的 Cluster 中. 把这个 Switch 的时间戳记录下来并写入到 Dynamodb 之类的中心存储中.
- 修改 Consumer 的 Application Code. 每当 Topic 没有被消费的数据的时候, 将时间戳于之前 Switch 的时间戳对比, 如果当前时间戳落后于 Switch 时间戳, 则说明旧的 Topic 中的消息已经被消费完了. Consumer Group 内所有的 Consumer 都显示没有数据了, 那么则创建拥有同样 Consumer 数量的 Consumer Group 对新的 Topic 进行消费.
- 这两个修改完成后, 开始更改 Parameter Store 中的参数.
- 这样做只是自动化了何时启动新的 Consumer Group 的过程. 由于 Consumer Group 内有的 Consumer 先没有数据, 有的后没有数据, 你必须等所有的 Consumer 都没有数据了才能切换, 所以还是有延迟. 你不能每当一个 Consumer 没有数据了就添加一个 Consumer 到新的 Consumer Group, 这样会导致新的 Consumer Group 会一直在 Re-balance.

进一步改进:

- 你可以修改 Consumer Group, 为每一个 Consumer Group 在 Dynamodb 之类的中心存储中维护一个 Key Value, 记录这个 Consumer Group 对应的 PartitionId, 以及是否可以 Switch 了.
- 你先创建新的 Consumer Group, 确保 Consumer 的数量以及新 Topic 的 Partition 的数量一一对应. 然后搞清楚新旧的 Consumer 与 Partition 的对应关系.
- 旧的 Consumer 如果发现没有数据了, 那么就更新 Dynamodb 的值.
- 新的 Consumer 开始的行为就是完全空转, 每隔一段时间就去 Dynamodb Check 一下值, 如果 Consumer 和 Partition 的对应关系和之前旧的 Consumer 和 Partition 的对应关系一致, 那么则开始消费. (用 `这个 <https://stackoverflow.com/questions/50164566/how-to-check-which-partition-is-a-key-assign-to-in-kafka>`_ 命令获得 Consumer 和 Partition 的对应关系.

这样可以自动化这个 Switch 的过程, 减少消费延迟. 但这么做需要保证两个 Topic 的 Partition 数量 Key 的设置一致.

2. **同时消费, 后迁生产**

指消费者业务启用多个 Consumer, 分别向原 Kafka 和新 Kafka 实例消费消息, 然后将 Producer 切到新 Kafka 实例, 这样能确保所有消息都被及时消费.

1. 启动新的 Consumer 端, 配置 Kafka 连接地址为新 Kafka 实例的连接地址, 消费新 Kafka 实例中的数据.
2. 原有 Consumer 端需继续运行, 消费业务同时消费原 Kafka 与新 Kafka 实例的消息.
3. 修改 Producer 的 Kafka 连接地址改为新 Kafka 实例的连接地址.
- 重启 Producer, 将生产业务迁移到新 Kafka 实例中.
- 生产业务迁移后, 观察连接新 Kafka 实例的消费业务是否正常.
- 等待原 Kafka 中数据消费完毕, 关闭原有消费业务客户端.
- 迁移结束.

优点:

- 迁移过程由业务自主控制. 本方案中消费业务会在一段时间内同时消费原 Kafka 和新 Kafka 实例. 由于在迁移生产业务之前, 已经有消费业务运行在新 Kafka 实例上, 因此不会存在端到端时延的问题.

缺点:

- 但在迁移生产的开始阶段, 同时消费原 Kafka 与新 Kafka 实例, 会导致部分消息之间的生产顺序无法保证, 存在消息乱序的问题.

总结:

- 此场景适用于对端到端时延有要求, 却对消息顺序不敏感的业务.

