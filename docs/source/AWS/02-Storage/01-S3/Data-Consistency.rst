Data Consistency in S3
==============================================================================

- S3 是一个分布式的 Key Value Object 系统, 实现的是 Eventually Consistency. 也就是你 Overwrite Put, 或是 Delete 了一个 Object, 如果你立刻读, 有可能读到的是之前的版本.
- S3 的 PUT 是原子操作, 只有操作完全成功, 才会返回成功.
- S3 只对创建新的 Object 的 Put 操作提供 read-after-write consistency, 也就是说, 只有在对象成功写入所有的设备, 返回成功的返回值后, 对象才能被读取. 对 Overwrite Put 不提供 read-after-write consistency.
- S3不提供锁的机制, 如果两个写操作并发, 结果最终会以最后一个为准.
