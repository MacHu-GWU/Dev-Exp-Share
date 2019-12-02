MongoDB Replication
==============================================================================

**背景**

凡是涉及到高可用性 (Availability), 我们都必须要引入冗余 (Replication). 我们来看看 MongoDB 中的 Replication 是怎么做的.

参考资料: https://docs.mongodb.com/manual/replication/


Primary Secondary Replication
------------------------------------------------------------------------------

- 首先, 每一个节点都需要有 3 个副本, 因为我们要保证在任何情况下数据都没有丢失的风险, 如果只有 2 个副本, 一个副本挂掉, 在更换新盘时, 唯一健在的副本挂掉的风险太大了.
- 这 3 个副本时有主次的, 同一时间只能有一个 Primary, 而所有的 write 操作都先在 Primary 上进行, 然后 Primary 将 ops log 转发到 secondary 上进行更新. 这意味着如果你的如果 read 操作在 secondary 上进行, 那么数据会有延迟的风险. 根据 CAP 理论, P 对于 Scale 来说是必须要有的, 而我们在 MongoDB 的应用场景下, 我们牺牲了 Consistence, 换来了 Availability.
- Primary 和 Secondary 之间会通过 Heartbeat 机制进行通信, 定期检测对方的存在. 如果有一个副本挂掉, 则立刻启动投票机制, 将一个 replicate 选举为 primary. 选举机制通常为所有的副本都会选择从自己的视角出发, 性能最好的副本.
- MongoDB 中可以使用 Arbiter 仲裁机制, 因为如果两个 secondary 都想要当 primary, 而票数相等则无法选出 Primary, 那么此时启用仲裁机制, 选出一个 primary.
