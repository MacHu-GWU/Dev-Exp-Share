.. _aws-msk-authentication-authorization:

MSK Authentication Authorization
==============================================================================
Keywords: MSK, Auth, SaSL

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Summary
------------------------------------------------------------------------------
Authentication 和 Authorization 其实是两个不同但是又相关的概念.

- Authentication 是身份验证, 证明你是谁. 这个 "谁" 也叫 Principal, 是 人, 机器, IP 地址, 账号 的一个抽象概念
- Authorization 是鉴权. 一旦知道了你是谁, 就可以决定你能对什么 "东西" 做 "什么". 这个 "东西" 也叫 Resource, 是 服务器, 数据库, 数据集, 文件 的一个抽象概念. 这个 "什么" 也叫 Action, 比如 Read / Write.

MSK 的访问权限管理问题其实是 "权限管理问题" 的子集. 本质上所有的 "权限管理问题" 就是 Principal, Resource, Action 的排列组合.

根据 `这篇文档 <https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html>`_ MSK 支持多种权限管理方式, 主要有:

1. IAM access control. 既能做 Authentication, 又能做 Authorization
2. Mutual TLS Authentication. 就是 HTTPS 协议里的 TLS, 服务器和客户端都需要 CA (证书). 只能做 Authentication, 不能做 Authorization.
3. `SASL / SCRAM <https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html>`_ (Simple Authentication and Security Layer/ Salted Challenge Response Mechanism), 就是基于账号密码的验证. 只能做 Authentication, 不能做 Authorization.
4. `Kafka ACLs <https://docs.aws.amazon.com/msk/latest/developerguide/msk-acls.html>`_ (Access Control List). 本质上 ACL 和 IAM 的实现是相同的, 只不过管理的精细度不同. 也有 Principal / Resource / Action 的概念. 只能做 Authorization. 根据 Kafka 的 `官方文档 <https://docs.confluent.io/platform/current/kafka/authorization.html>`_ ACL 能提供的管理粒度是:
    - `Principal <https://docs.confluent.io/platform/current/kafka/authorization.html#principal>`_:
        - Wildcard principals
        - SASL/Kerberos principals
        - TLS/SSL principal user names
        - IP, CName
    - `Resource <https://docs.confluent.io/platform/current/kafka/authorization.html#resources>`_:
        - Cluster
        - Delegation Token
        - Group
        - Topic
        - Transactional ID (For exact once delivery)
    - `Action <https://docs.confluent.io/platform/current/kafka/authorization.html#operations>`_


2. Challenge
------------------------------------------------------------------------------


3. Options
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


3.1 IAM Access Control 详解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**AWS 是怎么在 MSK 上实现 IAM Access Console**?

    AWS 是基于开源的 Kafka 源码对其做了一些改动. 每当一个带有 IAM 权限的 Principal (可以是任何机器, 电脑, 只要是 Attach IAM Role 的 EC2, 或是配置了 AWS Named Profile Credential 的任何机器), 跟 MSK 通信的时候, MSK 会跟 Client 握手, 并创建一个临时的 token 储存在 MSK 上, 并获得这个 token 的权限. 这个 token 就代表你的 Principal, 并且 MSK 和 Client 会自动刷新定期检查权限.

    这 MSK 和 Client 的通信协议是由 AWS 实现的. 需要 Client 安装支持这个通讯协议的包. 不然 MSK 是不知道你是 "谁" 的. 目前只支持 `这个 Java 的实现 <https://github.com/aws/aws-msk-iam-auth>`_. 也就是说其他语言目前还不支持用 IAM 跟 MSK 通信, 即使你是用 EC2 和 MSK 通信, MSK 也无法检测到你的流量是从 EC2 来的并自动检测到 EC2 背后的 IAM Role. 目前 AWS 的 `Product Feature Request 文档 <https://aws-crm.lightning.force.com/lightning/r/Product_Feature_Request__c/a2v4z000002RuwRAAS/view>`_ 正在推进对其他编程语言的支持

**如何在 Java Client 中使用 IAM Access Control**

    1. 配置 Client 客户端

    - 首先确保你安装了 Java, 如果是基于 Amazon Linux 的 EC2 和 Cloud9, 你可以用 ``sudo yum install java-1.8.0``
    - 然后根据 `这篇文档 <https://docs.aws.amazon.com/msk/latest/developerguide/msk-working-with-encryption.html>`_ 中搜索 ``truststore`` 关键字附近的命令, 参考教程把 ``truststore`` 文件拷贝到 ``/tmp/kafka.client.truststore.jks`` 位置供以后使用. 如果你不懂什么是 ``truststore`` 文件, 请参考这篇博文 :ref:`java-keystore-and-truststore-in-jsse`.
    - 为你的 Client 客户端用 AWS CLI 配置 AWS named profile
    - 然后根据 `这篇文档 <https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html>`_ 中搜索 ``Configure clients for IAM access control
`` 后面的教程, 创建好 ``client.properties`` 文件; 然后下载 `aws-msk-iam-auth <https://github.com/aws/aws-msk-iam-auth/releases>`_ JAR, 并放在正确的位置以供 import
    - 最后为这个 named profile 创建 IAM User (只给 program access 权限), 然后 attach 一个合适的 Policy.


3.2 SASL / SCRAM 详解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SASL 就是账号密码验证. 只不过账号密码的管理在社区版 Kafka 中是由 Kerberos 管理的. 创建 User, Password 都是通过 `kadmin <https://web.mit.edu/kerberos/krb5-1.12/doc/admin/admin_commands/kadmin_local.html>`_ 这个 Kerberos 命令行工具来进行的. 而 AWS 则是用 Secret manager 来管理用户名和密码, 只要将 Secret Attach 给 MSK, 那么 MSK 中的 User 就会自动和 Secret manager 保持一致 (我估计 AWS 还是用了 Kerberos, 只不过 AWS 把密码管理给自动化了).

显然 AWS 的方式更方便, 更强大, 支持更精细化的密码管理和自动 Rotate.

而 SASL 只能告诉 MSK 你是谁, 在 MSK 中你的 Principal 就是你的 username. 但是 Principal 具体能做什么 SASL 并不管, 也就是说 SASL 只管 Authentication 而不管 Authorization.

那么对于 SASL 提供的 Principal 的 Authorization 由谁负责呢? 答案是 ACL.


3.3 ACL 详解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




4. Solutions
------------------------------------------------------------------------------



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



对 MSK 的访问大致可以分为以下几类操作:

1. MSK API, 例如启动集群, 改变配置等. MSK API 是通过 AWS SDK 来操作的, 你必须要有 IAM 权限才能执行这些操作.
2. Apache Kafka API, 也就是 Kafka ``bin`` folder 下的那一堆 ``.sh`` 命令行. 例如获得 zookeeper connect str, 创建 topic 等, 这是 Kafka 内置的一些命令, 只不过操作对象是 MSK 上的 Kafka
3. Data Access, 包括 producer, consumer, subscribe 的这些行为
4. Zookeeper Access, 对 MSK 背后的 zookeeper 的访问, 由于 MSK 背后的 zookeeper 并不是随着 MSK 部署的, 而是由 AWS managed, 所以能进行的操作优先.

无论是哪些操作, 你首先要满足网络连接的条件, 然后才是满足访问权限.

这个 MSK API 比较简单, 跟其他 AWS SDK 一样, 都是通过 IAM 进行的. 这里重点说一下高频需求. 2 / 3.



除此之外, MSK 本身是 EC2, 那么 Security Group 也可以提供网络级别的管理. 同理 VPC ACLs 也能提供类似的权限管理.


我们来考虑 MSK 的


https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html


Setup Username Password Authentication with AWS Secret Manager for AWS MSK
------------------------------------------------------------------------------

Ref:

- Username and password authentication with AWS Secrets Manager: https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html