.. _kinesis-consumer-handle-slow-consumer:

Kinesis Consumer - Handle Slow Consumer
==============================================================================
Keywords:


Summary
------------------------------------------------------------------------------
假设对于每个 Shard, 每秒会产生 100 条 Record. 虽然一个每秒 Consumer 可以拉取 100 条 Record, 但每秒只能消费 10 条 Record. 这样 Shard 中未被处理的数据则会越来越多, 该怎么办呢? 简单来说就是: "单个 Consumer 实体的消费能力跟不上了一个 Shard 上数据产生的速度".

简单来说办法只有一个, 为每个 Shard 分配更多的 Consumer, 以加快消费速度. 但是由于 Kinesis 一个 Shard 有 5 TPS Get API Call 的限制, 也就是 1 秒最多调用 5 次 ``GetRecord`` 或是 ``GetRecords`` 的限制, 所以针对上面的问题, 让 10 个 Consumer 每 1 秒去 pull 一次 shard 显然是不行的, 因为超过了 5 TPS的限制, 并且每个 Consumer 都要维护各自的 Shard Iterator, 很难保证不重复消费也不漏消息. **所以唯一的办法就是让一个 Consumer Coordinator 专注于 1 秒 Pull 一次 10 条 Record, 然后将 Record 分发给 10 个 Consumer Worker 去处理**.

接下来要讨论的问题是, **把 Record 分发出去以后, 是 异步 (Async) 直接拉下一个 Batch, 还是 同步 (Sync) 等待响应再拉下一个 Batch**.

还有一个需要考虑的因素是, **Ordering 是否重要**, 如果重要, 意味着消费消息的速度必须按照产生消息的顺序. 如果 Consumer 处理一个消息结果失败了, 意味着这个 Consumer 就要停止从对应的 Shard 拉取数据.

这里我们先考虑 Ordering 不重要的情况, 这个比较简单. 因为如果 Ordering 不重要, 那么可以果断使用 Async 模式. 如果 Consumer Worker fail 了, 可以重试, 或者可以把数据打到 Dead-letter Stream 等待后续 Debug 处理即可, 反正以后再消费也没关系.

而如果是 Ordering 重要的情况, 这个就比较麻烦,


这里有个问题是, 假设 GetRecords API 返回了 10 条数据.


并且你把 Shard Iterator 和 Next Shard Iterator 都保存在 Dynamodb 中了.
