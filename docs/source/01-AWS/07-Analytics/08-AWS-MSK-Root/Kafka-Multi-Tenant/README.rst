.. _aws-kafka-multi-tenant:

Kafka Multi Tenant (多租户)
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Summary
------------------------------------------------------------------------------
什么是多租户?

    多租户就是指在一个数据系统中包含有属于不同的租户的数据. 例如一个 Database Table 中有属于不同租户的数据, 用一个 Column Tenant = A, B, C, ... 做区分. 又例如一个 Kafka Topic 中的 Message 有属于不同租户的数据.

为什么要有多租户?

    1. 为每个租户维护一套基础设施, 例如数据库, 成本是很高的. 在不同的租户的业务逻辑类似的情况下, 分享一套基础设施能有助于节约成本, 方便管理, 易于扩容.
    2. 有时候不同的租户的总数会很多, 万级甚至百万级, 那么为每一个租户准备一个独立的基础设施例如数据库几乎是不可能的. 所以就需要用一个超高吞吐量的数据库来管理.

在 Kafka 语境下的多租户?

    通常是指一个 Topic 中的 Message 可能来自于不同的租户. 也有的语境下指的是不同的租户使用同一个 Cluster. 但这种情况没有什么挑战.

多租户的挑战?

    1. 不同的租户使用同一个 Cluster的情况.

    - 只要做好 Topic 级别的权限管理即可, 让属于不同租户的 Consumer 只能访问他们自己的 Topic
    - 为了防止某个 Topic 的流量过大影响其他集群性能, 可以用 `Quota <https://docs.confluent.io/platform/current/kafka/design.html#quotas>`_ 进行限流. 限流的粒度有三种. "user + client_id", "user", "client_id".

    2. 同一个 Topic 中的 Message 来自于不同的租户的情况.

    - 要避免属于 A 的 Consumer **看到** 属于 B 的 Message. 常见于每个租户自己维护 Consumer 的情况.
    - 要避免属于 A 的 Consumer 不小心误对 B 的 Message 进行处理. 这种要求更宽松一些, 可以 **看到, 只要不处理** 即可. 常见于由第三方统一维护 Consumer 的情况.
    - 对于不同的租户的消费逻辑虽然比较相近但可能有所不同. 由于如果消费时间过长 Partition 和 Consumer 之间的 Heartbeat 可能 Timeout. 这就意味着这个 Timeout 要以消费最慢的 Tenant 为准.


2. Single Topic, Multi Tenant Solution
------------------------------------------------------------------------------
有两种解决方案:

1. 为每个 Tenant 新创建一个 Topic. 用一个 Consumer 作为 Distributor, 按照 Tenant 将数据分流到属于不同 Tenant 的 Topic 上.

    优点:

    - 数据完完全全被分离开, 不可能出现一个 Tenant 的 Consumer 不小心消费到了别的 Tenant 的数据.
    - 很容易增加和减少 Tenant. 增加一个新的 Topic 即可, 不影响已有的系统.
    - 每个 Tenant 的消费逻辑可以独立更新和部署, 更新一个 Tenant 不会影响其他 Tenant 的消费. 挂掉也不会影响他人.

    缺点:

    - 为每个 Tenant 所属的 Topic 配置合适数量的 Partition 非常难. 如果 Tenant 自己的吞吐量波动很大, 那么你就要给它很多 Partition. 但由于 Kafka 本身只允许增加 Partition, 但不能减少 Partition. 这还只是一个 Tenant 的情况, 很多 Tenant 的时候很难 Scale, 也容易造成浪费.
    - 如果不同的 Tenant 的数量很多, 你就需要创建很多 Topic. 如果超过 100 个就比较难管理了.

    应用场景:

    - 每个 Tenant 的 Topic 的流量要么比较小数量不多的 Partition 足以搞定. 要么虽然流量比较大, 但是 Traffic 比较稳定.
    - 不同的 Tenant 的数量不能很多. 超过 100 个就比较不合适了.

2. 为每个 Tenant 创建一个 Consumer Group, 每个 Consumer Group 在 Application Code 逻辑中 filter 出属于自己的数据并进行消费.

    优点:

    - 实现简单
    - 由于 Kafka 采用了 0 拷贝技术, 增加 Consumer Group 对 CPU 资源的消耗并不大, 只要网络能抗住就行.
    - 很容易增加和减少 Tenant. 增加一个新的 Consumer Group 即可, 不影响已有的系统.
    - 每个 Tenant 的消费逻辑可以独立更新和部署, 更新一个 Tenant 不会影响其他 Tenant 的消费. 挂掉也不会影响他人.

    缺点:

    - 每个 Tenant 的 Consumer Group 都收到了全量数据. 大大浪费了计算资源. 假设有 10 个 Tenant, 对于 Consumer 来说, 为了处理 10% 的数据就要付出 100% 的计算资源. 而对于 Kafka 来说, 为了处理 100% 的数据就要将将数据分发 10 份, 也就是分发出去了 1000% 的数据量. 性能的浪费在 2N 这个级别.
    - 往往 Consumer 会用 Batch 以减少 IO, 在这种方案下, 一次 Batch 获得的数据很可能只有非常少的 Message 是需要处理的, 这样就没法充分利用 Batch 带来的性能优势.

3. 只创建一个 Consumer Group. Consumer 的逻辑根据 Tenant 的不同调用不同的消费逻辑.

    优点:

    - 扩容容易
    - Kafka 端和 Consumer 端都不存在资源的浪费. 性能最佳.

    缺点:

    - 不同的 Tenant 的逻辑在一个 Consumer 中, 增加和减少 Tenant 意味着重新部署代码, 增加了重部署时破坏其他 Tenant 的正常消费的奉献.
    - 代码功能耦合会比较严重.
    - 跟 #2 一样, 在一个 Consumer Batch Poll 中, 属于同一个 Tenant 能够用 Batch 处理 Message 并不多, 没法充分利用 Batch 带来的性能优势.

4. 来自于 Gong 的解决方案:

    1. 不同租户的 Message 以 Round Robin 的方式到达 Topic. 这些 Message 会被随机分布在不同的 Partition 上.
    2. Consumer1 把这些数据按照 Tenant Id 为 Key, 发送到一个 Topic1 上. 在这个 Topic1 中, 属于同一个 Tenant Id 的 Message 会抵达同一个 Partition. 诚然, Traffic 很大的 Tenant 的数据会到达同一个 Partition. 但是由于是服务器, 这还行. 毕竟一个 Cluster 上可能有多个类似的 Topic, 不同的 Topic 有不同的 hot partition, 总的来说问题不大.
    3. Consumer2 把这些数据按照很大的 Batch 读进来, 然后按照 Tenant Id 打包成 Batch, 用 Round Robin 发送到 Topic2 上, 这个 Batch 中的所有数据都会被发到同一个 Partition 上. 也就是 Consumer2 本质上即是 Consumer, 也是 Producer. 虽然负责处理 Hot Partition 的 Consumer 压力会比较大, 但是由于逻辑简单, 只是简单的分发, 所以性能瓶颈问题不大.
    4. 最终有着实际业务逻辑的 Consumer 订阅 Topic2, 每次 Batch 收到的都是来一批来自同一个 Tenant 的 Message. 并且 Topic2 上每个 Consumer 处理的流量是均衡的.

- How We Maintain Tenant Data Isolation with Kafka at Scale: https://medium.com/gong-tech-blog/how-we-use-kafka-to-maintain-tenant-data-isolation-at-scale-ad501f2dc572
- https://kafkawize.com/2021/04/09/managing-multi-tenancy-in-kafka/