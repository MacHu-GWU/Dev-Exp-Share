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

- VPC
- Subnet
- Route Table
- Internet Gateway
- NAT Gateway
- Network Control List: Stateless, inbound 和 outbound 都要验证, 一个没有验证成功都不行. 有 Rule Number 的概念, 从小到大依次验证, 小的成功了, 大的就不用管了. 作用于 Subnet 级别.
- Security Group: Stateful, 比如发起者是位于公网的用户, 那么只用考虑 inbound, 一旦连接建立, 就不用管 outbound 了. 作用于 EC2, Lambda, RDS, 等 AWS Resource 级别.
- VPC Peering: 连接两个 VPC. 但无法连接 3 个, 只能将它们两两连接.
- VPC Endpoint: 允许位于 VPC 内部的机器. 当你的公司对安全要求很严格, 需要 VPC 内的机器不通过 Public Internet 访问 S3, 而是在 VPC 内, 通过 Amazon Network 访问 S3.
- VPC FlowLog: 记录了所有的网络端口通信细节 (不包括数据本身), **主要用于 Debug**.


Database
------------------------------------------------------------------------------


Route 53
------------------------------------------------------------------------------

**Route 53 是干什么的**:

1. 注册域名.
2. 将通往你域名的流量, 正确地 Route 到你位于 AWS 上的 Resource, 例如 EC2, Load Blancer.
3. 检查你的 AWS 资源 的健康度. 隔一段时间 Ping 一次, 如果 Ping 不通, 则写入 CloudWatch, 并触发 SNS 通知.

**重要概念**:

- Domain Name: google.com
- Top Level Domain (TLD): .com / .gov 这类的后缀
- Subdomain: google.com / maps.google.com / images.google.com 这类的共享一个根域名的域名.
- Domain Registrar: 一些特定的国际大公司, 有权利帮你注册某些域名.
- Domain Registry: 域名拥有者, 也就是找 Registrar 花钱注册了该域名的公司或人.
- Name Servers: 具体的某台服务器, 用于将你的 Domain Name 翻译成 IP 地址
- Authoritative Name Server: 根服务器, 负责某个区域, 比如北美, 亚洲的域名解析.
- DNS Resolver: 通常是 ISP (Internet Service Provider) 互联网服务提供商管理的服务器, 位于用户和 Name Server 之间.
- DNS Query: 查询一个 domain name 的过程.
- DNS Record: 一系列具体的 domain name 到 IP 的对应关系. 相当于是多个 ``A Record``
- Time to Live (TTL): DNS Server 上 DNS Query 的缓存持续时间.
- A Record:
    - CNAME (Canonical Name 权威的) Record: 规范的名字, 用于将多个域名导向同一个 EC2 或是 ELB. 例如 maps.google.com 和 mail.google.com 导向同一个 EC2.
    - Alias Record: AWS Route 53 的自定义 映射.
- Record Set, 多个 Record:
    - Type of Record Set:
        - IPv4 Address: xxx.xxx.xxx.xxx
        - CNAME: 规范的名字, 用于将多个域名导向同一个 EC2 或是 ELB. 例如 maps.google.com 和 mail.google.com
- Zone Apex: Root Domain, google.com, amazon.com
- Routing Policy: A setting for domain that determine how Route 53 responds to DNS queries and route the traffic.


**一些例子**:

- 你有一个 S3 Bucket 开启了 Static Website Hosting, http://example-bucket.com.s3-website-us-east-2.amazonaws.com, 你想将你的域名 www.example-bucket.com 连接上你的 Static Website. **IPv4 Address with Alias**
- 你有 4 个 EC2, 被放在了 Load Balancer 背后. 你想将你通往你域名 www.example-web-application.com 的流量导向 Load Balancer. **IPv4 Address with Alias**
- 你有一个 RDS, endpoint 是 example-a1b2c3d4xyz.us-west-1.rds.amazonaws.com. 你用 Route53 注册了一个域名. **CNAME without Alias**
- 你有一个公司的域名 www.example.com, 想要用 Route 53 作为 DNS provider, 并将其导向到 CDN 上. **Create an Alias record which point to CloudFront Distribution**.


**Route 53 能将流量导向哪些 AWS 服务**:

Logging, Monitoring, and Tagging:

- AWS CloudTrail
- Amazon CloudWatch
- Tag Editor

Routing Traffic to Other AWS Resources:

- Amazon API Gateway
- Amazon CloudFront
- EC2
- Elastic Beanstalk
- Elastic Load Balancer
- RDS
- S3
- VPC
- Workmail

**Troubleshoot Server Not Found error**:

- You didn't create a record for the domain or subdomain name
- You created a record but specified the wrong value
- The resource that you're routing traffic to is unavailable

**Routing Policy**:

- Simple routing policy – Use for a single resource that performs a given function for your domain, for example, a web server that serves content for the example.com website. 1 对 1 路由
- Failover routing policy – Use when you want to configure active-passive failover. 如果第一个 Resource 不 Healthy, 则换下一个.
- Geolocation routing policy – Use when you want to route traffic based on the location of your users. 你预先设定好, 哪个区域的用户被路由到哪里
- Geoproximity routing policy – Use when you want to route traffic based on the location of your resources and, optionally, shift traffic from resources in one location to resources in another. 根据用户的位置, 自动选择路由到最近的 (或其他自定义规则) Resource
- Latency routing policy – Use when you have resources in multiple AWS Regions and you want to route traffic to the region that provides the best latency. 当你的 App Host 在多个 Region 上时, 选择延迟最小的.
- Multivalue answer routing policy – Use when you want Route 53 to respond to DNS queries with up to eight healthy records selected at random. 同时返回多个可路由的目的地.
- Weighted routing policy – Use to route traffic to multiple resources in proportions that you specify. 加权路由, 给每个目的地加一个 Weight, 按概率取.

**Route 53 的 Health Check 能检查哪些指标**:

- Health checks that monitor an endpoint
- Health checks that monitor other health checks (calculated health checks)
- Health checks that monitor CloudWatch alarms

**Monitor Health Check**:

- To view the status of a health check on **route 53 console**
- To **receive an Amazon SNS notification** when a health check status is unhealthy (console)
- To view **CloudWatch alarm status** and edit alarms for Amazon Route 53 (console)
- To view **Route 53 metrics on the CloudWatch console**


Elastic Container Service (ECS)
------------------------------------------------------------------------------

What is ECS:

- Run containers at scale
- Flexible container placement
- Integrated and extensible

Features:

- Task
- Task Definition
- Cluster

Launch Type:

- Fargate Launch Type: set configuration of your Container, AWS launch the EC2 you need and run container.
- EC2 Launch Type: run container on EC2 Cluster you owned.

Note:

- You have root access to the OS of your container instance. enabling you to configure additional sotfware.


Snowball
------------------------------------------------------------------------------

简单来说, 就是几百 TB 甚至更多数据迁徙到 AWS 的一个方案.
实际上是 AWS 会寄给你很多 Snowball 机器, 然后连接上你的电脑, 里面有客户端将你的电脑系统, 或是数据存入 Snowball, 然后 AWS 会派人取走, 然后迁徙到 AWS 上.


AWS Kinesis
------------------------------------------------------------------------------

TODO


CloudFront
------------------------------------------------------------------------------

TODO


KMS (Key Management Service) and CloudHSM
------------------------------------------------------------------------------

TODO


EMR (Elastic MapReduce)
------------------------------------------------------------------------------

TODO


AWS Athena
------------------------------------------------------------------------------

TODO


EFS (Elastic File System)
------------------------------------------------------------------------------

一句话解释 EFS 的作用: 给 EC2 提供文件系统, 更重要的是, 给多个 EC2 提供 共享文件系统. 而一个 EBS 卷只能挂载到一个 EC2 上.

- EFS: 给 VPC 内的 EC2 提供文件系统, 必须为 EFS 指定 VPC 配合使用.
- Mount Target: 必须为 EFS 指定 Mount Target.
- 1 Mount Target on each AZs, on one of the subnets
- EFS has dedicated Network File System Port, restricted by Security Group
- EFS has two encryption, storage encryption (at rest) and network transit encryption.
    - storage encryption: can only be enabled on creation
    - network transit encryption: enable EFS Mount Helper, detach and re-attach the same EFS to enable it.
- Performance Mode:
    - General: under 50 EC2, low latency
    - Max IO: 50 ~ 1000+ EC2 sharing same EFS, higher latency
- Throughput Mode:
    - Burst:  是大多数时间很普通, 5MB/s, 一天能有 18 分钟提供 100MB/S 的速度
    - Provisioned: Provisioned 适用于 100MB ~ 1TB /S 级别的速度

EFS vs EBS:

- EBS, 块存储, 文件被分为 64KB 大小的块存储.
- EFS, 一个完整的 NTFS 文件系统.


Elastic Cache
------------------------------------------------------------------------------

TODO


CloudFormation
------------------------------------------------------------------------------

TODO

OpsWork
------------------------------------------------------------------------------

- AWS OpsWork is a configuration management service that helps you configure and operate application in a cloud enterprise by using Puppet or Chef.
- Help devops teams manage application and infrastructure.


Direct Connect
------------------------------------------------------------------------------

通过 Amazon 的 ISP (Internet Service Provider) 合作商, 例如 ATT, Comcast, Verizon, 为你的网络拉一条专线连接到 Amazon 的数据中心, 从而得到超高的网速.

- 通过 Direct Connect 的数据传输费用比通过公网更低.
- 常用于解决 私有数据中心 到 AWS VPC 的连接问题.


AWS Lambda
------------------------------------------------------------------------------

- Invoke Functions:
    - Request and Response: 通过 AWS CLI 发送 Invoke 请求. 所有的 Request and Response 类型的 Invoke 都是同步的. 也就是说发起请求的客户端在收到回复之前, 无法做下面的事.
- Event Triggered: 通过 Event 触发 Lambda 时, 根据不同的 Event 类型, 亚马逊预先定义了执行是用 Sync 还是 Async.
    - Sync:
        - Elastic Load Balancer
        - Amazon Cognito
        - Amazon Lex
        - Amazon Alexa
        - API Gateway
        - CloudFront
        - Kinesis Data Firehouse
        - Poll-based AWS Service: Kinesis, DynamoDB, SQS.
    - Async:
        - S3
        - Simple Notification Service
        - Simple Email Service
        - CloudFormation
        - Cloudwatch Log
        - Cloudwatch Events
        - Code Commit
        - AWS Config
- Manage Concurrency:
    - Account Level Concurrent Execution Limit (ALCEL): 1000 at same time by region
    - Function Level Concurrent Execution Limit (FLCEL): 函数级别的限制是 Lambda 的一项功能, 默认是关闭的. 要注意的是, 函数级别的限制一旦设置, 会减少全局的 账号级别的限制. 例如默认的的 ALCEL 是 1000, 你给一个函数预留了 100, 那么 ALCEL 就只剩下 900 了.
- Retry Behavior: 可以使用 Dead-Letter-Queue 保存出错的 Invoke
    - Event sources that aren't stream-based:
        - Synchronous invocation: X-Amz-Function-Error, error 200
        - Asynchronous invocation: automatically retry the invocation twice, store failed invokation in dead letter queue
    - Poll-based event sources that are stream-based: 由于对于 Poll-based Event, invokation records 是批量进行处理的, 如果1个 record 发生错误, lambda 会继续执行其他的 record, 直到处理完全部 records, 最长持续 7 天.
    - Poll-based event sources that are not stream-based: 例如 SQS, 由于 SQS 同样也是一次 Batch 发送多个 records 给 lambda 进行处理, 如果 1 个 record 发生错误, lambda 会立刻返回.


Elastic Beanstalk
------------------------------------------------------------------------------

TODO


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

TODO


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




