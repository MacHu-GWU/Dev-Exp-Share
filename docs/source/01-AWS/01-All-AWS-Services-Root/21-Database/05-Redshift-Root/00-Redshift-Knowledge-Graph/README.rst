Redshift Knowledge Graph
==============================================================================
Keyword: Redshift Knowledge Graph

本文档是 Redshift 的知识图谱.


入门篇
------------------------------------------------------------------------------
Management:

- Cluster:
    - Concepts:
        -
    - Create Cluster:
        - 如何创建 Cluster.
        - Cluster 的网络配置方式, 如何选择 VPC, Subnet, Security Group, Public Subnet 还是 Private Subnet, 是否 Public Accessible.
    - Connect to Cluster:
        - 如何使用 Query Editor 来执行 SQL.
        - 如何使用 SQL Client 软件 (例如 Dbeaver) 来连接到 Cluster (Username Password 和 IAM 两种方式).
        - 如何使用 Python Driver (例如 psycopg2, redshift-connector, sqlalchemy, sqlalchemy-redshift 等) 连接到 Cluster (Username Password 和 IAM 两种方式).
        - 如何使用 Data API 来执行 SQL.
    - Manage Cluster:
        - 如何管理 Cluster 中的 User, User Group, User Permission, Username, Password 等.
        - 如何用 Snapshot 备份和恢复 Cluster.
        - 如何用 Snapshot 复制 Cluster.
        - Resizing a Cluster (Scale up and down)
        - 如何用 Usage limit 来管理使用情况. 主要是用来控制成本, 例如防止 Amazon Redshift Spectrum 用太多产生不必要的账单.
        - 如何用 Workload Management (WLM) 来管理各个用户组分别能占用多少计算资源, 查询的最长运行限制, 扫描的数据量的限制等.
        - 如何用 Redshift-managed VPC endpoints 来管理 Cross Account VPC Access.
    - Security:
        - Data Protection, 如何保护你的数据.
            - Data Encryption, 如何加密你的数据, at rest 和 in transit.
            - Data Tokenization, 如何对数据进行脱敏.
            - Internet traffic privacy.
        - IAM access management.
            - 使用 IAM 来管理对 Redshift Cluster 进行管理的权限.
            - 使用 IAM 来管理对 Redshift API 的管理权限 (特别是 data api).
            - 给 Redshift Cluster 添加 IAM Role, 使得 Redshift 可以访问其他 AWS 服务, 例如 S3, Lambda, SageMaker 等.
        - Logging and monitoring.
            - 如何使用 CloudWatch 来监控 Redshift Cluster 的运行状态, 例如 CPU 和 Memory 的使用情况, 数据量的大小, 读写的 IOPS 的流量大小.
            - 如何使用 Audit Logging 来记录对 Redshift Cluster 的操作情况. 例如登录, 执行 Query 等. 你可以将这些 Log dump 到 S3 以供分析.
            - 如何使用 CloudTrail 来监控 Redshift API 的调用情况.
        - Compliance validation.
    - Cost:
        - 理解 Cluster 模式下的账单构成.
- Serverless:
    - Concepts:
        - Serverless 和 Cluster 架构的主要区别.
        - 理解 Namespace, Workgroup, RPU, Managed Storage 这些概念.
        - Create Serverless Cluster.
    - Create Namespace and Workgroup:
        - 如何创建 Workgroup, 同时创建新的 Namespace 或将 Workgroup 添加到已有的 Namespace 中.
        - Workgroup 的网络配置方式, 如何选择 VPC, Subnet, Security Group, Public Subnet 还是 Private Subnet, 是否 Public Accessible.
    - Connect to Redshift Serverless:
        - 如何使用 Query Editor 来执行 SQL.
        - 如何使用 SQL Client 软件 (例如 Dbeaver) 来连接到 Cluster (Username Password 和 IAM 两种方式).
        - 如何使用 Python Driver (例如 psycopg2, redshift-connector, sqlalchemy, sqlalchemy-redshift 等) 连接到 Cluster (Username Password 和 IAM 两种方式).
        - 如何使用 Data API 来执行 SQL.
    - Manage Namespace:
    - Manage Workgroup:
        - 如何管理 Redshift Serverless 中的 User, User Group, User Permission, Username, Password 等.
        - Managing usage limits, query limits, and other administrative tasks
    - Security:
        - Data Protection, 如何保护你的数据. 这部分和 Redshift Cluster 模式一样.
        - IAM access management.
            - 使用 IAM 来管理对 Redshift Serverless 进行管理的权限.
            - 使用 IAM 来管理对 Redshift API 的管理权限 (特别是 data api).
            - 给 Redshift Serverless 添加 IAM Role, 使得 Redshift 可以访问其他 AWS 服务, 例如 S3, Lambda, SageMaker 等.
        - Logging and monitoring.
            - 如何使用 CloudWatch 来监控 Redshift Cluster 的运行状态, 例如 CPU 和 Memory 的使用情况, 数据量的大小, 读写的 IOPS 的流量大小.
            - 如何使用 Audit Logging 来记录对 Redshift Cluster 的操作情况. 例如登录, 执行 Query 等. 你可以将这些 Log dump 到 S3 以供分析.
            - 如何使用 CloudTrail 来监控 Redshift API 的调用情况.
        - Compliance validation.
    - Monitoring queries and workloads with Amazon Redshift Serverless
    - Working with snapshots and recovery points
        - Restore a serverless snapshot to a serverless namespace.
        - Restore a serverless snapshot to a provisioned cluster.
        - Restore a provisioned cluster snapshot to a serverless namespace.
    - Data Sharing:
        - Data Sharing within AWS Account, or across regions
        - Data Sharing across AWS Accounts, or across regions
    - Cost:
        - 理解 Serverless 模式下的账单构成. 主要由 RPU 部分和 Managed Storage 部分构成.

Developer:


进阶篇
------------------------------------------------------------------------------
Management:

- Cluster:
    - Redshift Cluster 架构
    -
- Serverless:

Developer:


高阶篇
------------------------------------------------------------------------------
- `Amazon Redshift Management Guide <https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html>`_: 主要介绍了管理 Redshift 的知识, 例如创建, 维护, 备份, 删除 Redshift 等. 如果涉及到使用 Redshift 进行开发, 可以参考 Amazon Redshift Database Developer Guide.
- `Amazon Redshift Database Developer Guide <https://docs.aws.amazon.com/redshift/latest/dg/welcome.html>`_: 这个主要是给负责 CRUD 的 data engineer 的文档, 主要介绍了如何创建表, SQL 的功能等跟数据相关的内容. 而关于 Redshift 的维护和管理, 可以参考 Amazon Redshift Management Guide.