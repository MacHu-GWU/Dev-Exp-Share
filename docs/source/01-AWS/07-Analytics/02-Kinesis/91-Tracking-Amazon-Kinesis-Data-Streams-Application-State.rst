Tracking Amazon Kinesis Data Streams Application State
==============================================================================

Source: https://docs.aws.amazon.com/streams/latest/dev/kinesis-record-processor-ddb.html

在 Consumer 端, 如果你使用的是 Kinesis Client Library, 则会使用一个 Application Name 为 Table Name 的 Dynamodb Table 来 Track Application State

Throughput:

如果你看到 Kinesis Throughout Exception 时, 大概率是 Dynamodb 读写速度达到上限了 (默认情况下是 10 write read per seconds).

Application State Data:

- checkpoint: The most recent checkpoint sequence number for the shard. This value is unique across all shards in the stream.
- checkpointSubSequenceNumber: When using the Kinesis Producer Library's aggregation feature, this is an extension to checkpoint that tracks individual user records within the Kinesis record.
- leaseCounter: Used for lease versioning so that workers can detect that their lease has been taken by another worker.
- leaseKey: A unique identifier for a lease. Each lease is particular to a shard in the stream and is held by one worker at a time.
- leaseOwner: The worker that is holding this lease.
- ownerSwitchesSinceCheckpoint: How many times this lease has changed workers since the last time a checkpoint was written.
- parentShardId: Used to ensure that the parent shard is fully processed before processing starts on the child shards. This ensures that records are processed in the same order they were put into the stream.