Kafka Mirror Maker
==============================================================================


1. Summary
------------------------------------------------------------------------------
Mirror Maker (MM) 是 Kafka 官方提供的跨数据中心的流数据同步方案. 其实现原理就是通过在 Source Cluster 上创建 Consumer Group, 然后将消息发送给 Target Cluster. 相当于这个位于 Source Cluster 上的 Consumer Group 不仅相对于 Source Cluster 上的 Topic 扮演了 Consumer 的角色, 同时相对于 Target Cluster 上的 Topic 扮演了 Producer 的角色.


2. Mirror Maker 1 vs 2
------------------------------------------------------------------------------
2.4 版本以前 MM 的版本叫做 MM1, 从 2.4 以后就叫做 MM2 了. 起先 MM1 就是一个简单的生产者和消费者. 而这存在很多不足:

1. Target Topic 如果不存在, 会使用默认配置创建.
2. Source 端的 ACL 和 Config 发生变动时不会自动同步.
3. Message 会被 ``DefaultPartitioner`` 打散到不同分区. 即对一个 Topic, Source 和 Target 的 Partition 配置不一致.
4. 任何配置修改, 都会使得集群变得不稳定. 比如比较常见的增加 topic 到 whitelist (就是你想要让 MM 同步的 Topic).
5. 无法让源集群的 Producer 或 Consumer 直接使用目标集群的 topic.
6. 不保证 exactly-once, 可能出现重复数据的情况.
7. MM1 支持的数据备份模式较简单, 比如无法支持 active <-> active 互备.
8. Re-balance 会导致延迟.





Ref:

- Kafka跨集群迁移方案MirrorMaker原理、使用以及性能调优实践: https://www.cnblogs.com/felixzh/p/11508192.html