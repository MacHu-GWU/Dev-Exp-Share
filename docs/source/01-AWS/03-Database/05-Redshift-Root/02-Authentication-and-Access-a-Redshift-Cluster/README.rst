Authentication and Access a Redshift Cluster
==============================================================================

Keywords: Redshift, Auth, Authentication, Access Management

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


How Access Management Works in Redshift
------------------------------------------------------------------------------
Redshift 的访问权限管理一共分两层:

1. 网络层, 直接从网络层面拒绝未授权的访问.
2. 应用层, 有两种方式:
    - Database User: 跟传统关系数据库类似, 用 username password 的方式管理权限
    - IAM Role: 云原生模式, 用 IAM Role 来管理权限

**你需要同时满足两层的要求才能成功访问 Redshift**

**网络层管理**

Redshift 和 RDS 的网络层管理很类似, 本质上是一个 EC2 集群, 不过是对用户不可见, 由 AWS 自动管理. 既然是类数据库, 就有 DB Subnet Group, 决定了节点放在哪个 VPC Subnet 上, 既然在 Subnet 上, 就会受到 Route Table (路由表) 的管理.

网络层有两种常见部署模式:

1. DB Subnet Group 全部是 Private Subnet, 这是生产环境中常用的情形, 意味着不允许从公网随便一台机器访问. 通常只能由位于同一个 VPC 上的 Public Subnet 或是 Private Subnet 上的机器访问. 如果真的有从公网环境访问的必要, 那么你可以在 Public Subnet 配置一台 EC2 作为 Jumpbox, 使用作为 SSL tunnel 作为通信协议. 这种模式下推荐把每个 VPC 都有的特殊 default security group 给 Redshift cluster, 以及客户端机器. 具体做法请参考 :ref:`connect-to-private-subnet-rds-via-jump-host-using-sql-client`.
2. DB Subnet Group 全部是 Public Subnet, 这通常是开发环境中常用的情形, 意味着允许从公网访问, 但是要经过 Security Group 同意. 要注意的是在创建 Cluster 的时候一定要勾选 ``Enable Public Access``, 不然就算放在 Public Subnet 上也连接不上. 这时你的 Redshift Cluster 的 Security Group 建议单独配置一个 Rule 允许你的 IP 访问.

总结:

两种方式都是安全的, 都不怕 DDOS 攻击.

**应用层管理**


Redshift Service Role
------------------------------------------------------------------------------
Redshift 本身也是 EC2, 也是有需要访问 AWS 账号内的其他服务, 例如从 S3 读取数据. 那么你也是需要给 Redshift 本身 attach 一个 IAM Role, 这就和 EC2 instance profile 类似. 由于这个 Role 的 Principal (使用者) 是一个 AWS Service, 所以这种给 AWS Service 使用的 IAM Role 叫做 Service Role.