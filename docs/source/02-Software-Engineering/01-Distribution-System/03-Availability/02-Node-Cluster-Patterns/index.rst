.. _dist-sys-node-cluster-patterns:

Node Cluster Patterns (节点集群模式)
==============================================================================

.. contents:: Table of Content
    :depth: 1
    :local:


什么是 Node Cluster Patterns
------------------------------------------------------------------------------

在分布式系统中, 一定有许多的节点组成了一个集群, 来向外部提供服务. 分布式系统通过让节点之间互相协作, 实现负载分流, 冗余容错, 而最终实现分布式系统中的 一致性 和 高可用性.


Master-Slave 或 Leader-Follower Pattern
------------------------------------------------------------------------------

指有一个 master 用于特别重要的工作, 例如 write, 有时候也可以提供 read. 而 slave 则用于提高整体系统的可用性, 例如提供 read 服务. 当 master 宕机的时候, 通过选举机制的算法, 一个 slave 可以接管成为 master, **多用于数据库的设计中**.

- 比如 mongodb 中 master 节点提供 write, 然后写入的数据转发到 slave 上同步, 从而实现 eventual consistent. 而 read preference 设置为 slave, 用于保证高负载下的高并发读数据的性能.
- 又比如 Hadoop 中 Master 提供任务分发, 而 Slave 则真正执行 Map 和 Reduce 工作.
- 再比如 Zookeeper 中的 Leader 提供写, 而 Follower 提供读. Leader 收到写请求后会将消息转发到 Follower, 只有超过半数的 Follower 都成功写入了, 该写入才算是成功.


Active / Active Pattern
------------------------------------------------------------------------------

指所有节点的地位是等价的, 都同时工作, 由负载均衡请求发送给不同的节点处理. 例如 web app 多采用这一模式部署服务器.


Active / Standby Pattern
------------------------------------------------------------------------------

指只有 Active 的节点在运行提供服务, 而 Standby 只是备用, 当 Active 节点挂掉后 Standby 立刻接管.
