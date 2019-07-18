KPL (Kinesis Producer Library)
===============================================================================

Reference:

- https://docs.aws.amazon.com/streams/latest/dev/developing-producers-with-kpl.html

KPL 本质上是编程语言实现的客户端SDK程序 (目前只有 Java), 能让用户更容易的编写 Producer 程序.


Advantages of Using KPL over AWS SDK (Put Record)
-------------------------------------------------------------------------------

1. 性能更好, 单台机器 1K + Record /s 的写入性能.
2. 自带 Retry 机制.
3. 使用了 Batch, 先将 Record 写入 Buffer, 再一次性发给 Stream, 从而提高写入性能.
4. 允许方便地自定义 Monitor Event, 并将其发送到 CloudWatch.
5. 异步架构, 由于使用了 Buffer, 当你使用 KPL 执行 Put Record 时, 并不会堵塞 Producer Client 程序.


When to Use KPL When to use AWS SDK (Put Record)
-------------------------------------------------------------------------------

When to NOT USE KPL:

1. 如果不允许 Consumer 接受 Record 的时候有 Delay. 因为 KPL 使用了异步架构, 而且 Record 先打入 Buffer 再 Batch 发送, 所以不能用 KPL


Installing the KPL
-------------------------------------------------------------------------------

KPL 是用 C++ 实现的, 启动KPL后会在后台运行一个子进程. 然后你可以使用 KPL SDK (Java) 调用API.


KPL Key Concepts
-------------------------------------------------------------------------------

Records:

- KPL Records: 一条 Blob 数据
- Kinesis Data Stream Records: 一个特殊的 Record 数据结构, 包括了 Partition Key, Sequence Number, Blob of Data

Batching:

Batching 指对多个 Items (Records) 执行同一个 Action. KPL 支持两种不同的 Batching 模式:

- Aggregation: 将多个 KPL Records 合并, 保存在一个 Kinesis Data Stream Records 中.
- Collection: 将多个 KPL Records 用异步的方式延迟调用 AWS SDK PutRecord API, 提交到一个 Shard 或是多个 Shard 上.

Aggregation: 见上
Collection: 见上
