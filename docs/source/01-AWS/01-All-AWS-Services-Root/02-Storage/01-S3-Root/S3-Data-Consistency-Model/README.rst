S3 Data Consistency Model
==============================================================================
Keywords: Amazon AWS S3 Data Consistency Model


Summary
------------------------------------------------------------------------------
- Strong read-after-write consistency: 早期的 S3 是 eventual consistency, 也就是说你 put 了一个 object 返回成功之后立刻读, 有可能读到的是旧数据. 从 2020-12 起 AWS S3 提供了 Strong Read-after-Write Consistency, 也就是你返回成功后立刻读, 读到的都是正确的数据.
- Atomic S3 的 PUT 是原子操作, 只有操作完全成功或是完全不成功, 你不可能读到 partial 或是 corrupt 数据.
- S3不提供锁的机制, 如果两个写操作并发, 结果最终会以后成功的一个为准.

Reference:

- `Amazon S3 now delivers strong read-after-write consistency automatically for all applications <https://aws.amazon.com/about-aws/whats-new/2020/12/amazon-s3-now-delivers-strong-read-after-write-consistency-automatically-for-all-applications/>`_: 这是 Strong read-after-write consistency 作为新功能发布的公告
- `Amazon S3 data consistency model <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel>`_: 这是对 data consistency model 的详细说明
