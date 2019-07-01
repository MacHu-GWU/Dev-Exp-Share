Reading Data From Kinesis Data Stream
==============================================================================

- 1个 Shard 能提供 2MB/s 的读取速度. 如果有多个 Consumer 同时读取这个 Stream, 这个带宽由所有 Consumer 分享.

Enhanced Fan Out

- 