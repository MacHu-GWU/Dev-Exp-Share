AWS OpenSearch Security
==============================================================================


Reference:

- `Security in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/data-protection.html>`_


Data protection in Amazon OpenSearch Service
------------------------------------------------------------------------------
OpenSearch 使用了以下机制保证你的数据安全:

- Encryption at Rest: 所有落盘的数据, 包括 Index, Logs, Swap files, Snapshot, 都会被 KMS 所加密.
- Encryption in Transit: 所有的网络通信都会使用 TLS 加密.
- Node to Node Encryption: 所有节点之间的通信都会使用 TLS 加密.
- 对于 OpenSearch 的 API 调用在 CloudTrail 都有记录.


Identity and Access Management in Amazon OpenSearch Service
------------------------------------------------------------------------------
和其他的 AWS Service 一样, 最为推荐的身份验证的方法是使用 IAM. 和大部分跟 Data 有关的 Policy 一样, OpenSearch 也支持三种鉴权机制, 你可以选择性的启用其中的一到多种, 只有所有条件都满足的访问才会被允许. 这三种机制分别是:

- 基于 Identity 的 Policy, 也就是在 Principal, 请求发起方上附加的 Policy, 定义了请求方可以访问什么.
- 基于 Resource 的 Policy, 也就是在 OpenSearch 资源上附加的 Policy, 定义了谁可以访问自己.
- 基于 IP 地址的 Policy, 这个由 IAM Policy 里的 Condition 实现. 定义了请求方必须位于某个 IP 区间才能访问.


Cross-service confused deputy prevention
------------------------------------------------------------------------------
这个术语是用来解决 Coerce Access 的问题. 意思是, 有的时候 A 没有访问 B 的权限, 但是 C 有. 而 A 又有操纵 C 的权限, 这就导致 A 可以操纵 C 访问 B.

为了解决这个问题, OpenSearch 允许你在 Resource Policy 中定义 ``aws:SourceArn``, 来限制具体的 "谁" 可以访问自己. 如果通过 A assume C 来访问 B, 那么这里的 SourceArn 会显式 A 的 ARN, 从而能拦截下这种非法访问.


Fine-grained access control in Amazon OpenSearch Service
------------------------------------------------------------------------------
这是 OpenSearch domain 上的一个功能.


Resilience in Amazon OpenSearch Service
------------------------------------------------------------------------------
OpenSearch 支持 Multi-AZ domain 和 replica shards, 以及和 RDS 类似的 automate / manual snapshot. 和数据库服务类似, 也不支持跨 region 的 replica. 目前只有 Aurora 一个服务支持 global, 跨 region 的数据库.