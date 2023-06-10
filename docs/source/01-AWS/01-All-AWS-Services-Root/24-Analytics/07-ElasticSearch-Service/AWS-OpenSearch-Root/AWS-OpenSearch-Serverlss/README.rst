.. _aws-opensearch-serverless:

AWS OpenSearch Serverless
==============================================================================
AWS OpenSearch 是 ElasticSearch 技术的 AWS 修改版本, 并且 AWS 保证持续开源. 得益于 AWS 的云原生技术支持, OpenSearch 重新设计了整个数据库架构, 并将其分成了三层:

1. 调度层: 用于处理请求, 分发流量, 并管理集群的状态.
2. Indexing 层 (写入层): 用于负责分布式写入和索引.
3. Search 层 (读取层): 用于负责分布式搜索和聚合.

这种设计使得每一层之间都松耦合, 都可以轻松独立的扩容, 从而提高了整个数据库的性能和可用性. 基于这种设计, 最终使得 OpenSearch serverless 变成可能.

Reference:

- `Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html>`_
- `Amazon OpenSearch Serverless General Available <https://aws.amazon.com/about-aws/whats-new/2023/01/amazon-opensearch-serverless-available/>`_: 2023-01-25 OpenSearch Serverless GA Release


1. Concepts
------------------------------------------------------------------------------
传统 OpenSearch 的一个集群叫做一个 Domain, 也就是一堆 index 的集合. 一个 domain 里面有 Master Node 和 Data Node. Master Node 管调度, Data Node 管读写. 而且为了高可用, 这两个的数量必须是大于等于 3 的奇数, 从而能提供冗余.

而 Serverless 中由于没有用户可见的服务器, 所以也就没有集群了, 取而代之的是一个 collection, 也就是一堆 index 的集合. 而且 Serverless 里不再有 Master Node 的概念, 调度已经完全由 AWS 管理并且不再单独收费. 取代 Data node 的是 Indexing compute unit (ICU) 和 Search compute unit (SCU). ICU 负责写入, SCU 负责读取. ICU 和 SCU 合并起来叫做 OpenSearch Compute Unit (OCU), 相当于 2vCPU 和 8GB 内存.

总结来说 Serverless 的核心概念就是:

- collection
- ICU
- SCU
- OCU


2. Why OpenSearch Serverless
------------------------------------------------------------------------------
那么 Serverless 和普通选项有什么优势呢? 主要有以下几点:

- Serverless 可以根据你的业务需求读写比例的多少分配 ICU 和 SCU. 而普通选项的 Data Node 同时负责读写, 那么你分配的 Node 数量必须满足读写中最大的那个需求, 从而造成资源浪费.
- 你的业务流量不平均, 有时高有时低, 你无法提供一个精确的 Node 数量来满足这一需求, 只能按照最大流量来设计.
- 你处于业务逻辑开发阶段, 不希望花时间管理集群, 想用低廉的价格迅速开始实验.


3. Pricing
------------------------------------------------------------------------------
使用 Serverless 的客户中很大一部分是出于价格的考量, 能最大化利用资源和成本. 所以我们很有必要了解一下 Serverless 的价格. 它的价格主要是按照 ICU 和 SCU 的数量来计算, 以及对存储进行额外收费 (这部分很小). 一个 Collection 最小的配置是 2 个 ICU 和 SCU.

- OpenSearch Compute Unit (OCU) - Indexing (ICU), $0.24 per OCU per hour
- OpenSearch Compute Unit (OCU) - Search and Query (SCU), $0.24 per OCU per hour
- Managed Storage, $0.024 per GB per month

.. note::

    OCU comprises 8 GB of RAM and 2vCPU

- (`Amazon OpenSearch Ingestion <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ingestion.html>`_) OpenSearch Compute Unit (OCU) - Ingestion, $0.24 per OCU per hour. 这是一个全托管的 ETL 服务, 用于将数据 ingest 到 OpenSearch 中.

根据上面的数据, 一个最小的集群 (2 ICU + 2 SCU) 一小时的价格是 0.24 * 4 = $1, 一天就是 $24, 一个月大约是 $720. 诚然, 这对于个人用户来说并不便宜.

Reference:

- `AWS OpenSearch Pricing <https://aws.amazon.com/opensearch-service/pricing/>`_


4. Scaling
------------------------------------------------------------------------------
目前 (2023-06-01) OpenSearch 只支持 AWS Account 级别的 OCU Limitation, 而这个值是 50 个 ICU 和 50 个 SCU. 也就是说你 Account 下所有 Region 所有的 Collection 合起来最多有 50 个 ICU 和 50 个 SCU. 而且这个值是不能通过申请调高的. 不过这个值已经是相当的高了, 相当于一个月 $18k, 一年 $216k. 一般的中小企业应该是不会达到这个限制的.

关于自动弹性伸缩的机制目前是不透明的, 可以知道的事如果 CPU 内存占用达到一定程度就会增加新机器, 低于一定程度就会减少机器, 具体触发的边界在哪里 AWS 没有公开.

Reference:

- `Managing capacity limits for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-scaling.html>`_
- `boto3 opensearchserverless client update_account_settings <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_account_settings.html>`_
