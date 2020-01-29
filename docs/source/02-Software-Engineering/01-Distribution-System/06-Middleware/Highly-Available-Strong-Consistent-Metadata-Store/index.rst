Highly Available Strong Consistent Metadata Store
==============================================================================

对于分布式系统而言, 多个节点对整个系统的 外部状态 [1]_ 要有一个一致的了解才能协作. 例如在分布式 Map Reduce 集群中, 每个做 Map 的节点要知道处理后的数据发送到哪个 Reduce 的节点上, 那这些节点的 Metadata 就需要有一个一致的中心化的模块进行管理. 而我们知道任何 **单机系统都不可避免的会出现单点故障**, 所以这个 **中心化的模块本身就需要是一个高可用, 强一致, 分布式的服务**.

目前业内比较流行的两个解决方案是 2013 年 CoreOS 开源发布的 ETCD (K8S 的核心组件之一) 和 2008 年 Apache Software Foundation 开源发布的 Zookeeper (Hadoop 的核心组件之一).

高可用, 强一致的 Metadata Store 在以下领域也起到非常重要的作用:

- 微服务架构中的服务发现
- 负载均衡中的资源管理


ETCD 介绍
------------------------------------------------------------------------------

参考资料:

- 从零开始入门 K8s：手把手带你理解 etcd: https://www.infoq.cn/article/ZQZelYY57Xgvb6ECXcfb


Zookeeper 介绍
------------------------------------------------------------------------------

参考资料:

- 可能是全网把 ZooKeeper 概念讲的最清楚的一篇文章: https://segmentfault.com/a/1190000016349824


ETCD vs Zookeeper
------------------------------------------------------------------------------

一致性协议和算法:

- ETCD: Raft 算法
- Zookeeper: Zab 协议 和 Paxos 算法


社区成熟度:

- ETCD: 比较年轻
- Zookeeper: 比较成熟

可靠度:

- ETCD: 非常可靠
- Zookeeper: 非常可靠

实现语言:

- ETCD: Go
- Zookeeper: Java

客户端软件:

- ETCD: Go 的 client 比较成熟, 也有 Python 其他的还不够.
- Zookeeper: 主流语言都有.

节点存活判断:

- ETCD: Lease (可以将多个 Key 绑定到一个 Lease 上, Lease 需要定期刷新 调用 KeepAlice() 方法

分布式同步实现:

- ETCD: Master / Slave
- Zookeeper: Leader / Follower / Observer







.. [1] 外部状态是指一个系统以系统的外部使用者的视角来看, 处于的状态.