AWS Solution Architect Associate, The Ultimate Cheatsheet
==============================================================================

.. contents::
    :depth: 1
    :local:



IAM (Identity and Access Management)
------------------------------------------------------------------------------



S3 (Simple Storage Service)
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


Data Consistency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Eventually Consistency: you may read previous version of object after overwrite put and delete.
- S3 Put Object operation is atomic.
- Provide read-after-write consistency for Put New Object operation.
- There's no object lock, the last put object operation taken effect if two concurrent put object operations.


Storage Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

从上到下, 价格越来越便宜:

- S3 Stardard:
    - at least 3 AZs replica
    - low latency, high throughput
- S3 Standard - Infrequent Access (S3 Standard-IA): for Long-lived, but less frequently accessed data
    - exact 3 AZs replica
- S3 One Zone-Infrequent Access (S3 One Zone-IA): same as Standard-IA, but 20% cheaper
    - only 1 AZ
- Glacier: Long-term archive, 3 options to retrieve data
    - Standard: access data in 3-5 hours, 0.01$ per GB
    - Expedited: access data in 1-5 min, 0.03$ per GB
    - Bulk: access data in 5-12 hours, 0.0025$ per GB


Bucket Feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Bucket Properties:
    - **Versioning (超级重要)**:
        - Managing Objects in a Versioning-Enabled Bucket
            - Add: 自动给予 Object 新的 VersionId.
            - Get: 默认获得最新的, 要获得特定 Version, 需要指定 VersionId
            - Delete: 如果不指定 VersionId, 则在最新的 Object 上加一个 Marker, 标记为已删除, 这个已删除的 Object 则会作为最新的 Object. 此时默认的 Get 操作则会返回 404 错误. 只有指定 VersionId, 才能真正删除某个 Version.
        - Managing Objects in a Versioning-Suspended Bucket:
            - Add: 新加的 Object 会使用 Null 作为 VersionId, 并不会覆盖以前有 VersionId 的 Object, 而新加的同 Key 的 Object 则会覆盖掉 Null VersionId 的 Object.
            - Get: 无论你是否开启 Versioning, 永远是获取最新的那个 Object. Null 被视为最新的 Object.
            - Delete: 只能删除 Null VersionId 的 Object, 无法删除之前的 Versioned Object.
    - **Server Access Logging**:
        - Provides detailed records for requests that are made to a bucket (source bucket).
        - Useful for security and access auditing.
        - Source and target buckets should be in the same region.
        - Need to grant Amazon S3 log Delivery group write permissing on the target bucket.
    - **Object Level Logging**:
        - Logging happens at the object level.
        - Leverage CloudTrail trail.
        - Useful for security and access auditing.
    - Static website hosting:
        - if you want to use custom domain, you need to grant **CORS access to your source domain in the bucket**
    - **Default Encryption**:
        - You can only enable Encryption at bucket creation.
        - It is server side encryption.
        - Protect data in transit to S3:
            - solution1: use client side encryption, store encryption key on secret manager, encrypt the key with KMS, encrypt it before sending to s3.
            - solution2: put your worker machine in VPC, use VPC endpoint of S3 to upload data.
    - Object Lock: 防止某些 Object 被删除.
    - **Transfer Acceleration**: 常用于当你的 Bucket 在美国, 而你的用户在欧洲, 你可以使用 Transfer Acceleration (其实是 CloudFront 在起作用)
    - Events:
    - Request Pay:
- Permissions:
    - Block public access
    - Access Control List: 用于允许 其他 AWS 账户, 对 bucket 进行访问, 以及控制 读 写 的权限. ACL 作用于 Bucket 级.
    - Bucket Policy:  in-line policy provides detailed controls.
    - CORS (Cross-Origin Resource Sharing) configuration: 用于允许 AWS 以外的环境, 比如 Mobile App 上的用户, Web App 上的用户, 访问 S3.
- Management:
    - **Life Cycle Policy (超级重要)**: 为不同的 /Prefix 设定 Life Cycle Policy, 过一定时间自动从 Standard 降级为 Infrequent Access, 继而降级为 Glacier
    - **Replication**: 将 Bucket 内的数据同步到位于另一个 Region 的 Bucket, 作为备份. 该设置需要让两个 Bucket 都开启 Versioning 才能生效. 注意, Bucket 本身是全 Region 可访问, 一个 Region 内的 Bucket 名字, 在另一个 Region 内也不能用. 但是 Bucket 还是有物理意义上的 Region 的, 取决于你在哪里创建的.
    - Analytics: 分析里面的 Object 的占比之类的
    - Metrics: 监控 Storage, Requests, Data Transfer
    - Inventory: 设定一个 Object 清单列表, 每隔一段时间生成报告


File, Volume, Tape Gateway
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- File Gateway: 把 S3 当文件系统用.
- Volume Gateway: 在你的服务器上安装一个网络硬件, 将机器上的数据备份到 S3
- Tape Gateway: 将备份数据用磁带机的方式备份到 S3 Glacier


Share Object with Other
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

用 SDK 可以为 Object 创建一个 Presigned URL, 并设置失效时间. 这是唯一的能控制失效时间的分享方式. Bucket Policy 并不能自动设置过期时间.


EC2 and EBS (Elastic Block Storage)
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

EC2 Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instance Type:

- General Purpose:
    - A1
    - T3
    - T3a
    - T2
    - M5
    - M5a
    - M4
- Compute Optimized: CPU intense
    - C5
    - C5n
    - C4
- Memory Optimized: memory intense
    - R5
    - R5a
    - R4
    - X1e
    - X1
    - High Memory
    - z1d
- Accelerated Computing: GPU intense
    - P3
    - P2
    - G3
    - F1
- Storage Optimized: high IO
    - I3
    - I3en
    - D2
    - H1

- T/M: general purpose
- C: compute optimized
- R: memory optimized
- P/G/F: accelerated computing
- I (IO)/D (Disk)/H (HDD): storage optimized

Reference:

- Instance Type: https://aws.amazon.com/ec2/instance-types/


EBS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Volume Type:
    - SSD (固态硬盘):
        - EBS General Purpose SSD (gp2): 普通电脑的硬盘
        - EBS Provisioned IOPS SSD (io1): IO 密集型, 例如数据库应用
    - HDD (磁碟机硬盘):
        - Cold HDD (sc1): for large data that is infrequently accessed
        - Throughput Optimized HDD (st1): IO 密集型, streaming workload, data warehouse, big data, log processing, cannot be a boot volume
- Encryption:
    - EBS 使用 KMS 进行 Encryption at rest.
    - 只有在创建 Volume 的时候可以启动 Encryption, 创建后无法启动.
    - 只有部分 EC2 Instance Type 可以支持 Encryption (通常是那些高性能的).
    - 由于 RDS 实际上运行在 EC2 上, 也挂载了 EBS, 所以对数据库数据加密的原理, 和对 EBS 加密的原理实际上是一样的.


ELB (Elastic Load Balancer)
------------------------------------------------------------------------------

简单来说 ELB 就是一个 ``host:port/path`` 到多个具体的 EC2 的 ``host:port`` 的映射.

Concepts:

- Listener:
- Rules:
- Health Check:
- Target and Target Group.

Balancer Type:

- Application Load Balancer: HTTP/HTTPS, 比如 /picture 则送到 图像服务器, /request 则送到 App 服务器
- Network Load Balancer: TCP/IP, 比如 :80 则送到 图像服务器, :8080 则送到 视频服务器
- Classic Balancer: TCP/SSL or HTTP/HTTPS, Classic Load Balancers currently require a fixed relationship between the load balancer port and the container instance port.

简单来说 ASG 就是一个自动启动和关闭 EC2 的管理器, 设定一个 最少, 最多的 EC2 台数, 然后 CPU 利用率高了就启动 EC2, 利用率低了就关闭 EC2.


Auto Scaling
------------------------------------------------------------------------------

Concept:

- Launch Template: Metadata of EC2, 决定了自动启动的 EC2 机器的详细配置, 比如用哪个 Image, 多达的 CPU 和内存.
- Launch Configuration:

Min, Max, Desired:

- min: 最少多少台
- desired: 最开始的时候启动多少台
- max: 最多多少台

Terms:

- Scale-out: 增加机器
- Scale-in: 减少机器

Scaling Your Group:

- Manual Scaling: 手动指定增加/减少多少台 EC2
- Scheduled Scaling: 预定时的任务, 常用于可预测的高峰, 例如 Black Friday
- Dynamic Scaling: 简单来说就是设定一个 最小 和 最大 的 EC2 数量, 用 CloudWatch 检测 EC2 的 Metrics, 比如一旦 CPU 占用率达到 90%, 则增加一台机器. 而 CPU 低于 10%, 则关闭一台.
- Scaling Cooldowns: 简单来说就是在成功的进行一次 Scale 之后, 多久之内不进行 Scale. 常用于 Dynamic Scaling 非常频繁的增加和减少你的机器的情况.

Controlling Which Auto Scaling Instances Terminate During Scale In:

- Default Termination Policy: 哪个 AZ 上 EC2 最多, 就在那个 AZ 上关闭一个. apply to most of case
- Customizing the Termination Policy
- Instance Protection


CloudWatch
------------------------------------------------------------------------------



VPC (Virtual Private Cloud)
------------------------------------------------------------------------------



Database
------------------------------------------------------------------------------



Route 53
------------------------------------------------------------------------------


Snowball
------------------------------------------------------------------------------


AWS Kinesis
------------------------------------------------------------------------------


CloudFront
------------------------------------------------------------------------------


KMS (Key Management Service) and CloudHSM
------------------------------------------------------------------------------


EMR (Elastic MapReduce)
------------------------------------------------------------------------------


AWS Athena
------------------------------------------------------------------------------


EFS (Elastic File System)
------------------------------------------------------------------------------


Elastic Cache
------------------------------------------------------------------------------


CloudFormation
------------------------------------------------------------------------------


OpsWork
------------------------------------------------------------------------------


Direct Connect
------------------------------------------------------------------------------


AWS Lambda
------------------------------------------------------------------------------


Elastic Beanstalk
------------------------------------------------------------------------------


Trusted Advisor
------------------------------------------------------------------------------

Trusted Advisor 能自动检查你的 AWS Resource, 发现潜在的能 减少开支, 提高性能, 提高可靠性, 增加安全性 的机会.

Cost Optimization:

Under utilized EC2 Instance
Ideal Elastic Load Balancer
Unassociated Elastic IP

Performance:

Highly utilized EC2 instance
Rules in EC2 security group
Over utilized EBS Volume

Security:

Security Group unrestricted access
IAM Password policy

Fault Tolerance:

EC2 instance distribution across AZs in a region
AWS RDS Multi AZ

Service Limits:

Service Limits on AWS VPC, EBS, IAM, S3 etc



CloudTrail
------------------------------------------------------------------------------


WAF (Web Application Firewall) and Shield
------------------------------------------------------------------------------

- WAF:
    - Helps protect your web application from common web exploits that could affect application availability, compromise security, or consume excessive resource.
    - Monitor the HTTP ans HTTPS requests that are forwarded to an Amazon API Gateway API, Amazon CloudFront or Application Load Balancer
    - AWS WAF gives you control over which traffic to allow or block your web application by defining customizable web security rules.e
- Shield: Protect you from DDOS attack.


SQS, SNS and SWF
------------------------------------------------------------------------------

- SQS: Simple Queue Service
    - Visibility Timeout: 当一条 Record 被 consumer 读取到时, 一定时间内是无法被其他 consumer 读取到的 (不可见), 默认值是 30 秒, 最高能到 2 小时.
    - Queue Type:
        - Standard: 默认情况下可以保证大部分的record先进先出, 如果两条一样的record就无法保证了. 并发数量几乎无限.
        - FIFO: 完全保证先进先出. 并发数量为 3000 records/s with batch, 或是 300 records/s without batch.
    - Dead-Letter Queues: 一个专用的 FIFO Queue (只能是 FIFO Queue), 用于保存那些在别的 Queue 中出错的 record.
    - Short-Polling vs Long-Polling: 服务端在没有数据的时候并不是马上返回数据, 会hold住请求, 等待服务端有数据, 或者一直没有数据超时处理, 然后一直循环下去. 这样能减少 Empty Response 和 False Empty Response (消息实际存在, 但是返回的是 Empty). SQS 默认使用 Short-Polling.
- SNS: Simple Notification Service, SWF makes it easier to build application that coordinate work across distributive system
    - Publisher
    - Topic
    - Subscriber
- SWF: Simple Work Flow
    - Task:
    - Worker: 执行 Task 的 AWS Resource, EC2, Lambda, etc...
    - Actor:
        - Starter: 任何可以执行 Workflow 的 Application
        - Decider: 实现了 Workflow 的具体逻辑
        - Activity Work:




