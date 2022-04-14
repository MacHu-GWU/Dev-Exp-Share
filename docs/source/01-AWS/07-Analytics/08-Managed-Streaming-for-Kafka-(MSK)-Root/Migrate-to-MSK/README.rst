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