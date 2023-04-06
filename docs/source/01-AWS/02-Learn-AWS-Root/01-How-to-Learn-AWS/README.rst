.. _how-to-learn-aws:

How to Learn AWS
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Overview
------------------------------------------------------------------------------
AWS 大约有 200 多种服务, 刚入门的时候你可能会觉得无从下手. 我们在学习一门技术的时候, 通常要结合我们的目标有侧重点的学习. 例如, 我们想要用 AWS 来解决什么问题? 又或者是我的职业目标是 XYZ, 我想要学习这个职业需要知道的知识. 学习AWS 也不例外. 官方推荐按照 Role (你的角色) 和 Solution (需要解决的问题) 选择不同的 Learning Path.

AWS offers around 200 services, and when you first start learning, you may feel overwhelmed. When we learn a new technology, we usually focus on our goals. For example, what problem do we want to solve with AWS? Or what knowledge do I need to learn to achieve my career goal of XYZ? Learning AWS is no exception. The official recommendation is to choose different learning paths based on your Role (your job role) and Solution (the problem you need to solve).

按照角色可以分为这么几类:

- Solutions Architect: 解决方案架构师. 其职业角色是帮助企业提供一个能解决具体问题的架构方案. 侧重点是设计, 而不是写代码. 需要的知识广度高, 深度一般.
- Cloud Practitioner: 云计算工程师, 也叫 Cloud Engineer, 主要是管理企业在云上的资源. 偏向运维. 要求会使用云服务提供商的系统, 对编程的要求不高. 需要的知识广度中等, 深度一般.
- Developer: 开发者, 侧重点是开发应用程序. 需要的知识广度低, 深度高. 能准确的使用特定的云服务构建应用是他的核心技能.
- DevOps Engineer: 运维工程师, 侧重点是自动化运维, 对于基础设施和服务器部署管理的知识要求高. 需要的知识广度低, 深度高.
- Machine Learning: 机器学习, 侧重点是跟人工智能相关的服务.
- Operations: 我个人不了解这个, 感觉这个像是跟客服类似的操作员.

按照解决方案可以分为这么几类:

- Advanced Networking: 网络架构
- Data Analytics: 数据分析
- Databases: 数据库技术
- AWS for Games: 游戏技术
- Machine Learning: 机器学习
- Media Services: 媒体服务
- Security: 安全
- Serverless: 无服务器, 微服务架构
- Storage: 数据存储

Reference:

- `Learning by Role or Solution <https://aws.amazon.com/training/learn-about/>`_:


My Personal Suggestion
------------------------------------------------------------------------------
AWS 官方将 learning level 分为了 4 个等级:

- 100: 仅仅听说过, 对概念有所了解
- 200: 有初步的基础, 大概了解怎么操作
- 300: 有一定的实践经验, 有一定的深度
- 400: 专家

我本人是云技术专家, 以上所有的 Role 和 Solution 分类大部分都达到了 400 的专家级别, 少部分只有 300 (比如 security). 达到现在这个状态大约用了 6 年时间, 而最关键的一段时间其实只有经验暴涨的 3 年. 下面我分享一下我个人的学习经验, 仅供参考.

不仅仅是 AWS 所有的云技术的基础是三大块: 计算, 存储 和 网络. 而 AWS 在 计算的杀手服务是 EC2 (虚拟机), 存储是 S3 (对象存储), 网络是 VPC (虚拟私有云). 这三个服务是 AWS 的核心, 也是 AWS 的基础. 你要想学好 AWS, 你必须要掌握这三个服务. 你可以从这三个服务开始, 逐步深入学习其他的服务. 我建议这三个服务的深度达到 200 ~ 300 左右再开始学习其他的服务.

这三个服务我建议按照 S3 -> VPC -> EC2 的顺序学. 因为 EC2 是在 VPC 的基础上的, 而 S3 比较好学, 并且应用范围更广 (谁都需要存数据).

**S3 需要掌握的知识点有**:

.. image:: https://github.com/MacHu-GWU/aws_icons-project/blob/main/icons/Service/Arch_Storage/64/Arch_Amazon-Simple-Storage-Service_64.png?raw=true

- 了解 Bucket 和 Object 的概念.
- 知道如何上传和下载 Object.
- 知道如何用 API 对 Object 进行各种操作, 例如你对本地文件系统的各种操作所对应的操作.
- 了解 Storage Class 的概念.

**VPC 需要掌握的知识点 (这个是大多数人第一个门槛)**:

.. image:: https://github.com/MacHu-GWU/aws_icons-project/blob/main/icons/Service/Arch_Networking-Content-Delivery/64/Arch_Amazon-Virtual-Private-Cloud_64.png?raw=true

- 了解 VPC, Subnet 的概念
- 了解 CIDR Block IP 地址区间的概念
- 了解 Route Table 路由的概念
- 了解 IGW, NAT 等网络设备的概念
- 了解 Security Group 的概念
- 能动手创建一个新的 VPC, 并包含 public subnet 和 private subnet, 其中 private subnet 要能访问 internet, 而 只有 public subnet 能访问 private subnet

**EC2 需要掌握的知识点**:

.. image:: https://github.com/MacHu-GWU/aws_icons-project/blob/main/icons/Service/Arch_Compute/64/Arch_Amazon-EC2_64.png?raw=true

- 了解什么是 EC2, EC2 Type, EC2 Instance, AMI.
- 了解什么是 EBS, EC2 是如何用 EBS 作为存储磁盘的.
- 了解 EC2 如何选择放在 VPC 中的 Subnet 上, 如何给 EC2 配置 Security Group.
- 了解什么是 Key Pair, 如何 SSH 到 EC2 上, 就像操作 Mac / Ubuntu 那样操作 EC2.
- 学习如何管理 EC2 的生命周期, 例如如何创建, 如何停止, 如何重启, 如何删除.
- 了解什么是 AMI 镜像, 如何用 AMI 来备份和恢复 EC2.

这三个服务学习完毕之后, 还有一个重要的服务, IAM (identity access management) 权限管理. 这个服务是使用任何其他服务的基础, 你只要需要动手, 那么基本上绕不开 IAM. **IAM 需要掌握的知识点有**:

.. image:: https://github.com/MacHu-GWU/aws_icons-project/blob/main/icons/Service/Arch_Security-Identity-Compliance/64/Arch_AWS-Identity-and-Access-Management_64.png?raw=true

- 什么是 IAM Group, User, Role, Policy.
- 什么是 Role 里面的 trusted entity, 什么是 Policy Document 里的 statement.
- 如何给人类使用者或机器使用者配置 IAM Role.
- 如何通过 IAM Policy 给使用者合适的权限.
- IAM 的基本的最佳实践 (如果你的权限管理配置不当, 请不要到公司生产环境中操作, 可能会造成重大影响)

至此, 你已经有学习 AWS 的基本知识了. 接下来你就要根据你的需求, 在 Role 和 Solution 中选择一个方向深入了. 如果你没有具体的短期目标, 而是希望从长期上看获得最大的收益, 那么我建议你选择 Solution Architect 的 Role. 因为这个 Role 会涉及所有其他的 Role 的知识点, 而本身也是为了提供 Solution 而存在的, 所以基本涵盖了 AWS 的方方面面. 你之后可以有基础转型任何一个 Role 和 Solution.

这里我列出了一个学习的列表, 你可以自行按照分类来有选择性的学习.

**By Role**

- Solutions Architect:
- Cloud Practitioner:
- Developer:
    - CodeCommit: Git 仓库
    - CodeBuild: CI build 运行环境
    - CodeArtifact: 云原生 artifacts, 类似 Nexus Repository
    - CodePipeline: CI/CD Pipeline 以及编排
    - Parameter Store: 云原生配置管理
    - Secret Manager: 敏感信息管理
    - CloudFormation: 用代码管理云资源
    - ECR: 容器仓库
    - SQS: 消息队列
    - SNS: 消息退送
    - Kafka (MSK): 消息中间件
    - Kinesis Stream / Firehose: 流数据处理
    - EC2, Lambda, ECS Fargate, Batch: AWS 云原生计算四件套
    - API Gateway: 全托管式的 API
    - Elastic Beanstalk: 云原生全托管式的 Web App 部署.
    - AppSync: GraphQL
- DevOps Engineer:
    - System Manager: 管理 EC2 的利器, 相当于 Ansible + SSH 等更多功能
    - Image Builder: AWS 版本的云原生 Packer
- Machine Learning: 请参考 Solution
- Operations:

**By Solution**

- Advanced Networking:
    - VPC Peering: 多个 VPC 组成一个大网
    - VPC Client VPN: 通过 VPN 连接到 VPC
    - VPC Direct Connect: 通过专线把物理机房连接到 VPC
    - Elastic Load Balancer: 负载均衡
    - Route53: 域名管理
    - Transit Gateway: 中心化的网络管理
- Data Analytics:
    - Glue
    - Athena
    - Redshift
- Databases:
    - RDS (传统关系数据库)
    - Aurora / Aurora Serverless (云原生关系数据库)
    - DynamoDB (NoSQL, 无服务器 Key Value 数据库)
    - ElasticCache / MemoryDB (高速缓存)
    - ElasticSearch / OpenSearch (文本搜索)
    - DocumentDB (MongoDB, 文档存储)
    - Keyspaces (Cassandra, 宽列存储)
    - 特定领域数据库:
        - Neptune (图数据库)
        - TimeStream (时序数据库)
        - AQLD (区块链账本)
- AWS for Games:
- Machine Learning:
    - SageMaker
    - Augmented AI: 人类辅助机器学习 (Human in the loop)
    - GroundTruth: 人工标注
    - Textract: OCR, 文本数据提取
    - Comprehend: 文本理解
    - Rekognition: 图像识别
    - Personalize: 推荐系统
    - Polly: 文本到语言
    - Translate: 翻译
    - Transcribe: 语音到文本
- Media Services:
- Security:
    - IAM
    - Cognito
    - Macie
- Serverless:
    - Lambda: 无服务器容器计算
    - ECS, ECS Fargate: 无服务器容器集群计算
    - Step Function: 编排服务, 无服务器版本的 AirFlow
- Storage:
    - S3
    - EBS
    - EFS
    - FSx
