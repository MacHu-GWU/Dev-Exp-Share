Big Data Specialist Kinesis 考点
==============================================================================

https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-it-works-kinesis-video-api-producer-sdk.html






读取 - Shared Fan Out
------------------------------------------------------------------------------




Shared Fan-out vs Enhanced-Fan-Out
------------------------------------------------------------------------------

- 1个 Shard 能提供 2MB/s 的读取速度. 如果有多个 Consumer 同时读取这个 Stream, 这个带宽由所有 Consumer 分享.
- 如果启用了 Enhanced Fan-Out 功能, 则允许一个 Consumer 独享一个 Stream 2MB/s 的读取速度.
- 如果用 API Consumer, 则可以 Subscribe individual shard.
- 如果用 KCL Consumer, 则自动 Subscribe all shard of the stream.


如何让多个 Consumer 同时读取一个 Stream, 并且数据一 available 就立刻读取?
------------------------------------------------------------------------------

首先, 要注意 Stream 的读取数据有限制, 每秒, 每个 Shard 最多同时执行 5 个 GetRecords. 为了避免触发这个限制, Amazon 推荐每一个 Application 每秒钟 polling 一个 Shard. 尽量使用 Batch 获得更高的吞吐量.


Behavior before and after Reshard
------------------------------------------------------------------------------

无论是你 将一个 Shard 再分片, 还是合并多个 Shard. **这个过程都不是瞬间完成的. 那么在这个过程中, Producer 和 Consumer 会受到什么影响? 以及相关的 Shard 上的数据又会被怎样移来移去呢?**

在你执行 Resharding 的过程中, Stream 是 Inactive 的. 你需要在你的代码中加入异常处理的部分, 当捕获到 Stream Inactive 的错误时, 要进行等待重试, 直到 Stream 恢复 Active.

定义 Parent Shard

- 在 Split Shard 中, 则那个被 Split 的 Shard 就是 Parent Shard
- 在 Merge Shard 中, 则两个被 Merge 的 Shard 都是 Parent Shard

开始执行 Resharding 时候, Parent 处于 Open State, 执行完了之后 Parent 处于 Close State, 当 Parent 过了 Retention Period 之后, 里面的数据已经无法 Accessible 了, 此时处于 Expire State.

执行 Resharding 之后, PutReocrd 到 Parent Shard 的数据会被 Route 到 Child Shard, 而 GetRecord 则会从 Parent 和 Child Shard 上读取数据.


Reshard Strategy
------------------------------------------------------------------------------



Security and Encryption
------------------------------------------------------------------------------

- Kinesis doesn't support client side encryption.
- Kinesis support all kinds of serverside encryption.