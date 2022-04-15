On-prem Username Password Access
==============================================================================


1. 启动 MSK 集群
------------------------------------------------------------------------------
- 确保 MSK 全部放在了 Public Subnet 上.
- 启动 MSK Cluster 的时候 Public Access 是无法打开的, 只要在 Cluster 变为 Active 之后修改.
- 确保 Access Control Method 你只勾选了 ``IAM role-based authentication`` 和 ``SASL/SCRAM authentication``.
- 确保 Security Group 你除了 default (就是允许任何来自于同一个 sg 的 traffic, 每个 VPC 自带的 default sg), 还要有一个自定义的, 其中允许来自于你本地电脑的 IP 的 ``All Traffic``.

启动 MSK 通常需要个 15 分钟. 在启动的期间你可以进行下一步.


2. 准备 Secret Manager
------------------------------------------------------------------------------

参考 `这篇官方文档 <https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html>`_, 配置 Secret Manager.

- 确保你用来 Encrypt Secret 的 KMS key 是 custom managed key, 而不是 AWS managed key.
- 你的 Secret 的内容是 Plaintext, 并且是符合下面的 Format::

    {
        "username": "alice",
        "password": "alice-secret"
    }
- 确保你的 Secret Name 是以 ``AmazonMSK_`` 开头的.


3. 准备 Cloud9
------------------------------------------------------------------------------
我们需要两台 Cloud9:

- 一台拥有 MSK Admin IAM 权限, 作为管理 MSK 集群配置的机器.
- 一台只有基础的 AWS 权限但没有 MSK 的机器, 用于运行 Producer, Consumer 的程序.

两台机器的名字分别叫:

- kafka-admin
- kafka-app

其他要注意的点:

- 这两台机器必须和 Kafka 同在一个 VPC 下. 我们的主要目标是测 Authentication, 而不是测网络.
- 这两台机器放在 Public Subnet 或是 Private Subnet 无所谓, 最好是 Public Subnet 下.
- 两个 Cloud9 都要禁用 AWS Managed Credential
- 两个 Cloud9 都要有 VPC default security group
- kafka-admin 机器可以有 Admin 权限
- kafka-app 机器只需要最基本的几个权限就可以了, 不要给他 MSK 权限


3. 启用 Public Access
------------------------------------------------------------------------------
这一步可以跳过, 你可以先在 Cloud9 里面实验. 账号密码实验成功之后再用


5. 配置 Python Client
------------------------------------------------------------------------------

confluent-kafka

Ref:

- https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html


- FAQ Access Management Section: https://aws.amazon.com/msk/faqs/
- Authentication and Authorization for Amazon MSK APIs: https://docs.aws.amazon.com/msk/latest/developerguide/security-iam.html
- Authentication and Authorization for Apache Kafka APIs: https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html
- Controlling Access to Apache ZooKeeper: https://docs.aws.amazon.com/msk/latest/developerguide/zookeeper-security.html
