Resharding a Stream
==============================================================================

Ref:

- Resharding a Stream: https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding.html?shortFooter=true

你可以执行两种操作:

- Split Shard:
- Merge Shard:


After Resharding
------------------------------------------------------------------------------

无论是你 将一个 Shard 再分片, 还是合并多个 Shard. **这个过程都不是瞬间完成的. 那么在这个过程中, Producer 和 Consumer 会受到什么影响? 以及相关的 Shard 上的数据又会被怎样移来移去呢?**

在你执行 Resharding 的过程中, Stream 是 Inactive 的. 你需要在你的代码中加入异常处理的部分, 当捕获到 Stream Inactive 的错误时, 要进行等待重试, 直到 Stream 恢复 Active.

定义 Parent Shard

- 在 Split Shard 中, 则那个被 Split 的 Shard 就是 Parent Shard
- 在 Merge Shard 中, 则两个被 Merge 的 Shard 都是 Parent Shard

开始执行 Resharding 时候, Parent 处于 Open State, 执行完了之后 Parent 处于 Close State, 当 Parent 过了 Retention Period 之后, 里面的数据已经无法 Accessible 了, 此时出于 Expire State.

执行 Resharding 之后, PutReocrd 到 Parent Shard 的数据会被 Route 到 Child Shard, 而 GetRecord 则会从 Parent 和 Child Shard 上读取数据.

