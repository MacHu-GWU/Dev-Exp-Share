

Connect to MSK and Authentication / Authorization
==============================================================================

对 MSK 的访问大致可以分为以下几类操作:

1. MSK API, 例如启动集群, 改变配置等. MSK API 是通过 AWS SDK 来操作的, 你必须要有 IAM 权限才能执行这些操作.
2. Apache Kafka API, 也就是 Kafka ``bin`` folder 下的那一堆 ``.sh`` 命令行. 例如获得 zookeeper connect str, 创建 topic 等, 这是 Kafka 内置的一些命令, 只不过操作对象是 MSK 上的 Kafka
3. Data Access, 包括 producer, consumer, subscribe 的这些行为
4. Zookeeper Access, 对 MSK 背后的 zookeeper 的访问, 由于 MSK 背后的 zookeeper 并不是随着 MSK 部署的, 而是由 AWS managed, 所以能进行的操作优先.

无论是哪些操作, 你首先要满足网络连接的条件, 然后才是满足访问权限.

这个 MSK API 比较简单, 跟其他 AWS SDK 一样, 都是通过 IAM 进行的. 这里重点说一下高频需求. 2 / 3.

MSK 有四种 Authorization 机制:

1. IAM Policy.
2. Mutual TLS Authentication, 就是 HTTPS 协议里的 TLS, 需要 CA 证书.
3. SASL / SCRAM (Simple Authentication and Security Layer/ Salted Challenge Response Mechanism), 就是基于账号密码的验证.
4. Kafka ACLs (Access Control List). 本质上就是 Kafka 自带的 IAM, 也有 Principal / Resource / Action 的概念, 不过这里的 Principal 都是 CN (canonical name), 也就是 DNS 地址. 这是一种基于网络的验证手段.

除此之外, MSK 本身是 EC2, 那么 Security Group 也可以提供网络级别的管理. 同理 VPC ACLs 也能提供类似的权限管理.


我们来考虑 MSK 的


https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html

位于 On Prem 网络中的 Producer 和 Consumer 如何与 MSK 相连?
------------------------------------------------------------------------------

    由于网络

    1. AWS
    2. AWS Certificate Manager

位于 AWS Cloud 中的 Producer 和 Consumer



Ref:

- FAQ Access Management Section: https://aws.amazon.com/msk/faqs/
- Authentication and Authorization for Amazon MSK APIs: https://docs.aws.amazon.com/msk/latest/developerguide/security-iam.html
- Authentication and Authorization for Apache Kafka APIs: https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html
- Controlling Access to Apache ZooKeeper: https://docs.aws.amazon.com/msk/latest/developerguide/zookeeper-security.html


Setup Username Password Authentication with AWS Secret Manager for AWS MSK
------------------------------------------------------------------------------

Ref:

- Username and password authentication with AWS Secrets Manager: https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html