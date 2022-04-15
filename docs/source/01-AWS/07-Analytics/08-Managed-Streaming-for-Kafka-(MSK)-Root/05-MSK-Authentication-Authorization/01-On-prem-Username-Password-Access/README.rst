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
- 等 MSK Cluster 启动完毕后, 用 Console 里 Associate Secret 的功能将 Secret 关联到 MSK Cluster


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
- 两个 Cloud9 的 IAM Role 的 Trusted Entity Document 必须要有 ``"cloud9.amazonaws.com", "ec2.amazonaws.com"`` 两个, 光有 EC2 没用. 自己创建的 IAM Role 一般只有 EC2, 你需要手动添加 Cloud9.
- kafka-admin 机器可以有 Admin 权限
- kafka-app 机器需要有 ``arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile`` 这个 AWS 提供的 IAM Policy 即可, 该 Policy 让你能用 System manager 来连接 Cloud9 EC2. 你还要有 ``arn:aws:iam::aws:policy/SecretsManagerReadWrite`` 才能获得 Credential, 避免了把密码直接写在代码里的风险.


3. 启用 Public Access
------------------------------------------------------------------------------
这一步可以跳过, 你可以先在 Cloud9 里面实验. 账号密码实验成功之后再用


5. 配置 Python Client
------------------------------------------------------------------------------
我们这里使用 `kafka-python <https://kafka-python.readthedocs.io/en/master/index.html>`_ Python 库作为 Kafka Client.

我们使用 `pysecret <https://github.com/MacHu-GWU/pysecret-project>`_ 库来从 AWS Secret Manager 中获得 username, password.

在 MSK Cluster 中选定的 SASL/SCRAM authentication 在 ``kafka-python`` 中对应的是 ``SASL_SSL`` 方式, 使用的是 ``SCRAM-SHA-512`` 验证方式.

Ref:

- MSK SASL authentication: https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html#msk-password-tutorial
- Consumer: https://kafka-python.readthedocs.io/en/master/_modules/kafka/consumer/group.html
- Producer: https://kafka-python.readthedocs.io/en/master/_modules/kafka/producer/kafka.html


6. 测试 Python Client
------------------------------------------------------------------------------
- FAQ Access Management Section: https://aws.amazon.com/msk/faqs/
- Authentication and Authorization for Amazon MSK APIs: https://docs.aws.amazon.com/msk/latest/developerguide/security-iam.html
- Authentication and Authorization for Apache Kafka APIs: https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html
- Controlling Access to Apache ZooKeeper: https://docs.aws.amazon.com/msk/latest/developerguide/zookeeper-security.html


7. 管理 Username, Password 对应的 User 的权限
------------------------------------------------------------------------------
请注意 https://docs.aws.amazon.com/msk/latest/developerguide/msk-acls.html 里的一段话:

    Apache Kafka ACLs have the format "Principal P is [Allowed/Denied] Operation O From Host H on any Resource R matching ResourcePattern RP". If RP doesn't match a specific resource R, then R has no associated ACLs, and therefore no one other than super users is allowed to access R. To change this Apache Kafka behavior, you set the property allow.everyone.if.no.acl.found to true. Amazon MSK sets it to true by default. This means that with Amazon MSK clusters, if you don't explicitly set ACLs on a resource, all principals can access this resource. If you enable ACLs on a resource, only the authorized principals can access it. If you want to restrict access to a topic and authorize a client using TLS mutual authentication, add ACLs using the Apache Kafka authorizer CLI.

这段的意思是, 默认情况下 ``allow.everyone.if.no.acl.found`` 是 ``true`` 他的意思是, 当你验证权限的时候, 假设你有一个 Resource 通常是一个 Topic, 如果你所有已有的 ACL 中的 ResourcePattern 的模式都没有 Match 这个 Resource, 换言之这个 Resource 在 ACL 中找不到任何他的定义, 那么任何 Principal 都能访问这个. 说白了当这个设置为 ``true`` 的时候, 如果没有设置, 默认是 Allow. 这就导致了默认情况下, 你在 Secret Manager 中的 User 可以访问任何 Resource, 因为 ACL 里什么都没有. 这样有一个隐患, 就算你为所有的 Resource (Topic) 定义了 ACL, 没有权限的 Principal 是无法访问这些 Topic 的, 但对于之后新创建的 Topic, 总有一段时间你来不及定义 ACL, 这段时间所有的 Principal 都能访问这个 Topic.

而如果把这个设为 ``false``. 说白了就是默认是 Deny. 你必须在 ACL 中显式允许 Principal 访问某个 Resource. 也就是说你在得为 Secret Manager 中的 User 创建 ACL. 这也是 AWS 推荐的模式.

下面我们一步步操作实现用 ACL 精细化管理 Secret Manager 中的 User:

1. 在 MSK Cluster Configuration 中创建一个新的 Configuration, 里面的值就是 AWS 的默认值. 然后在最后添加一行 ``allow.everyone.if.no.acl.found=false``. 然后在 Cluster 中选择 Edit Configuration, 这需要一段时间才能使得 Configuration 生效.
2. MSK 架构中真正处理 Data 的 Broker 是跟 Zookeeper 在一个 VPC 里的, 而你的 MSK 的 VPC 里的 Broker 是 bootstrap broker. 由于你的 broker 本身也是个 Principal (是基于 CName 的 Principal), 你的 ACL 中并没有定义这个 broker, 所以这个 broker 是无法从真正管理 Topic 的 broker 那里读取 topic 数据发送给客户端的, 所以你需要在 ACL 中给你的 bootstrap broker READ 权限. 一直都是 ````::

    ./kafka-acls.sh --authorizer-properties zookeeper.connect="${zookeeper_conn_str}" --add --allow-principal "User:CN=*.${bootstrap_server_endpoint}" --operation Read --group=* --topic "${topic_name}"

关键的 ACL 命令::

    # 列出已经存在的 ACL
    ./kafka-acls.sh --authorizer-properties zookeeper.connect="${zookeeper_conn_str}" --list

    # 给指定 Secret Manager 中的用户 Read / Write 的权限
    ./kafka-acls.sh --authorizer-properties zookeeper.connect="${zookeeper_conn_str}" --add --allow-principal "User:alice" --operation Read --group=* --topic "DatabaseStream"
    ./kafka-acls.sh --authorizer-properties zookeeper.connect="${zookeeper_conn_str}" --add --allow-principal "User:alice" --operation Write --topic "DatabaseStream"

    # 允许你的 Broker 读取 Topic
    ./kafka-acls.sh --authorizer-properties zookeeper.connect="${zookeeper_conn_str}" --add --allow-principal "User:CN=*.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com" --operation Read --group=* --topic "DatabaseStream"
