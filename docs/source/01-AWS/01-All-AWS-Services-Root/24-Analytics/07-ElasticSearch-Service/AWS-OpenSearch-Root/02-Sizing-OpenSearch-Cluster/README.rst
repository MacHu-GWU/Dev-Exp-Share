.. _aws-opensearch-sizing-cluster:

Sizing OpenSearch Cluster
==============================================================================
有几个要考量的因素:

从硬件的角度, 要考虑如下因素:

1. CPU: 每个 Shard 会占用 CPU, 不仅 Primary Shard 会占用 CPU, Replica Shard 也会占用 CPU. 这取决于你的 Replica Factor
2. 内存: 查询用的 index 是在 JVM 内存中维护的, JVM 内存如果超过 70% 就要报警了, 维持在 50% - 70% 是一个比较好的利用率
3. 磁盘: Replica 也是要占用磁盘的, 并且根据 `官方文档 <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html>`_ 系统, 过期数据等都会占用额外磁盘空间, 通常你测量出的大小要乘以一个 1.45 的系数.

简化版流程图:

1. **计算需要多少磁盘**: 启动一个 1 个 data node, 0 replica 的集群, 根据你的 Mapping, 计算 benchmark, 每 1M 个 Document 在磁盘上占据多少 GB. 在 OpenSearch 中的统计数据是指的磁盘占用大小, 而不是指的对应的 index 的内存占用. 假设为 1G. 而你目前有 1B 个文档, 也就是要 1000G 磁盘. 并且你记录一下你的内存占用 1M 个 Document 需要占用多少 JVM 内存. 这里我们假设占用了 50M 的内存.
2. **计算需要多少 Shard**: 根据 ElasticSearch `最佳实践 <https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html>`_, 一个 Shard 处理的数据大小保持在 10G ~ 50G 较好. 最好不要超过 30G. 所以你可以用 1000G / 30G 得到约 34 个 Shard.
3. **计划你的 Replica Factor (RF)**: 默认是 replica factor = 1, 也就是 1 个副本. 1 个副本保底, 2 个副本才能保证高可用. 我们这里使用保底策略, 也就是 1 个副本.
4. **计算实际需要的 Shard**: 由于 RF = 1, 也就是你实际需要 34 * 2 = 68 个 Shard.
5. **选择你的 EC2 Type**, 每个 EC2 Type 有三个因素: vCPU, Memory, EBS Bandwidth (磁盘 IO 速度). 我们以 ``r6g.xlarge`` 为例, 有 4 个 vCPU, 32GB 内存, 4750 Mbps.
6. **选择 Shard CPU Ratio**, 也就是为每个 Shard 分配多少个 CPU. 这取决于你的业务逻辑. 如果 Read 并发很高, 那么每个 Shard 都会被利用到也就是说每个 Shard 都需要至少一个单独的 CPU. 最好需要 1.5 个, 因为 replica shard 也会承担查询的任务, 如果刚刚好是一个, 则很容易出现多个 shard 竞争一个 CPU 的情况. 官方推荐是 1.5 个, 根据你的业务可以将这个比例定为 0.5 ~ 2. 而在写入都是 Batch 且不频繁, 且 Read 的频率不高, 但是对响应时间很高的情况, 我们可以使用 Ratio = 0.5. 由于有 Replica 的存在, Primary Shard 是能单独占用一个 CPU 的.
7. **计算需要多少个 Data Node**, 这取决于 CPU, Memory, EBS 最短的那个短板. 通常 CPU 是最大的短板会比较合适. 因为如果 CPU 是短板意味着内存和磁盘有冗余. 内存和磁盘如果达到上限了很可能导致系统直接不可用, 而 CPU 达到上限则是会造成延迟.
    - CPU: 我们有 68 个 Shard, 需要 68 * 1.5 = 102 个 CPU, 也就是一共需要 102 / 4 ~= **26** 个 ``r6g.xlarge``.
    - Memory: 一共有 26 个 node * 32 GB 每台 ~= 832 GB, 而我们需要占用 50M * 1000 ~= 50 GB JVM 内存, 远远没有达到上限. 所以内存有很多冗余.
    - EBS:
        - Disk: 一共有 1000G * 2 个副本 * 1.45 的其他系统占用系数, 大约需要 2900G 磁盘, 每个 Node 则需要 2900 / 26 ~= 115 GB 磁盘.
        - IO: 一共有 26 * 4750 Mbps ~= 123 Gbps, 你一共才 1000G 的磁盘占用, 不可能需要这么高的 Gps, 所以磁盘也有很多冗余.
8. **继续调优**, 我们可以看出内存有很多的冗余, 而 CPU 比较吃紧. 这对于查询远远大于数据集的业务来说这事没办法的事情. 但是我们还有很多优化可以做:
    - 我们可以用 batch 以及异步提高写入的效率, 在写入之前进行一些 aggregate, 提高写入性能.
    - 对于查询多多利用缓存
    - 对于查询输入进行预处理, 很多不同的查询经过预处理后其实是同一个查询, 这样可以更多的利用缓存.

Ref:

- Sizing Amazon OpenSearch Service domains: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html
- Size your shards: https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html
