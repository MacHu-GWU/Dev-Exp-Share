Bucket
==============================================================================

Bucket Properties:

1. Versioning
2. Server access logging
3. Static Website Hosting
4. Object-level logging
5. Tags
6. Transfer Acceleration
7. Events


Bucket Url Pattern
------------------------------------------------------------------------------

1. https://mybucket.s3-us-east-1.amazonaws.com
2. https://s3-us-east1.amazonaws.com/mybucket


Bucket Feature
------------------------------------------------------------------------------

- Properties:
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
    - Bucket Policy: in-line policy provides detailed controls.
    - CORS (Cross-Origin Resource Sharing) configuration: 用于允许 AWS 以外的环境, 比如 Mobile App 上的用户, Web App 上的用户, 访问 S3.
- Management:
    - **Life Cycle Policy (超级重要)**: 为不同的 /Prefix 设定 Life Cycle Policy, 过一定时间自动从 Standard 降级为 Infrequent Access, 继而降级为 Glacier
    - **Replication**: 将 Bucket 内的数据同步到位于另一个 Region 的 Bucket, 作为备份. 该设置需要让两个 Bucket 都开启 Versioning 才能生效. 注意, Bucket 本身是全 Region 可访问, 一个 Region 内的 Bucket 名字, 在另一个 Region 内也不能用. 但是 Bucket 还是有物理意义上的 Region 的, 取决于你在哪里创建的.
    - Analytics: 分析里面的 Object 的占比之类的
    - Metrics: 监控 Storage, Requests, Data Transfer
    - Inventory: 设定一个 Object 清单列表, 每隔一段时间生成报告


Object Feature
------------------------------------------------------------------------------
