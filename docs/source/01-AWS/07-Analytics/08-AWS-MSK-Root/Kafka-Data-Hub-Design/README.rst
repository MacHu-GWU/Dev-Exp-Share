Kafka Data Hub Design
==============================================================================




1. 中心化的 Data Hub 要解决什么问题?
------------------------------------------------------------------------------
1. 首先, 没有银弹.

    基于 Kafka 的 Data Hub 要解决的问题都是基于流数据处理. Kafka 不是一个计算引擎, 也不是一个 ETL 引擎. Kafka 是一个中间件, 能让基于不同技术的 计算引擎 和 ETL 引擎 配合起来.

2. 一次生产, 多次消费.

    当出现一个新的源数据流的时候, 我们就可以将数据打入 Kafka Topic. 先不管我们要怎样消费它.

    当想到一个能消费这个数据并带来价值的的方式, 我们就可以启用 1 个 Consumer Group.

    以后能想到新的消费方式, 可以很快的启用新的 Consumer Group.

    这和 DataLake 的功能很相似, 先不管三七二十一把数据存入 DataLake. 想到以后如何使用这些数据的时候再处理这些数据.

3. 基础设施复用.



2. 中心化的 Data Hub 的关键技术挑战是什么?
------------------------------------------------------------------------------
1. Multi-Tenant with-in Topic.

    有两种解决方案:

    1. 用一个 Consumer 作为 Distributor, 按照 Tenant 将数据分流到不同的 Topic 上. 每个 Tenant 变成一个新的 Topic.
        - 优点:
            - 数据完完全全被分离开, 不可能出现一个 Tenant 的 Consumer 不小心消费到了别的 Tenant 的数据
            - 很容易增加和减少 Tenant. 增加一个新的 Topic 即可, 不影响已有的系统.
        - 缺点:
            - 为每个 Tenant 所属的 Topic 配置合适的 Partition 非常难. 由于 Kafka 本身只允许增加 Partition, 但不能减少 Partition.
        - 应用场景:
            - 每个 Tenant 的 Topic 的流量都很小, 数量不多的 Partition 足以搞定.
    2. 为每个 Tenant 创建一个 Consumer Group, 每个 Consumer Group filter 出只属于自己的数据并进行消费.
        - 优点:
            - 实现简单
            - 很容易增加和减少 Tenant. 增加一个新的 Consumer Group 即可, 不影响已有的系统.
        - 缺点:
            - 每个 Tenant 的 Consumer Group 都收到了全量数据.
    3. 只创建一个 Consumer Group. 为

2. 权限管理.

    作为一个 Hub, 生产者无脑的将数据打入 Kafka. 消费者来选择感兴趣的 Topic.

    1. 消费者如何在没有权限的情况下 Explore 来自不同 Topic 的数据?
    2. 如何高效管理庞大数量的访问权限? (Principal / Resource / Action)
    3. 如何

