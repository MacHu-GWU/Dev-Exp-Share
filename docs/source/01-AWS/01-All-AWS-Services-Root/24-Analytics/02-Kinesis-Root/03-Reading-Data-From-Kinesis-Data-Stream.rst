Reading Data From Kinesis Data Stream
==============================================================================

有下列事实:

- 1个 Shard 能提供 2MB/s 的读取速度. 如果有多个 Consumer 同时读取这个 Stream, 这个带宽由所有 Consumer 分享.
- 如果启用了 Enhanced Fan-Out 功能, 则允许一个 Consumer 独享一个 Stream 2MB/s 的读取速度.
- 如果用 API Consumer, 则可以 Subscribe individual shard.
- 如果用 KCL Consumer, 则自动 Subscribe all shard of the stream.


如何让多个 Consumer 同时读取一个 Stream, 并且数据一 available 就立刻读取?
------------------------------------------------------------------------------

首先, 要注意 Stream 的读取数据有限制, 每秒, 每个 Shard 最多同时执行 5 个 GetRecords. 为了避免触发这个限制, Amazon 推荐每一个 Application 每秒钟 polling 一个 Shard. 尽量使用 Batch 获得更高的吞吐量.



