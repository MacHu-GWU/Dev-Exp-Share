Managing Throughput Settings on Provisioned Tables
==============================================================================

Ref:

- Managing Throughput Settings on Provisioned Tables: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html

管理 ``预分配的`` 表的流量.

- Burst Capacity: Dyanamodb 将你 5 分钟内没有使用的 RCU WCU 保留起来, 如果你突然需要多于你的设定的读写速度, 则可以利用这期间保存的读写带宽.
- Adaptive Capacity: 由于 Dynamodb 有 Partition, 所以你的总 RCU WCU 的带宽在每个 Partion 上是要均分的. 但如果你使用了 Adaptive Capacity, 那么某个特别 Hot 的 Partition (比如超级明星用户在这个 Partition 上) 的带宽允许超过平均值, 只要总数没有超过你的设定. 而且单个 Partition 是有 3000 RCU 1000 WCU 的限制的, 但是假设你的总数是 6000 RCU 2000 WCU, 而有 3 个 Partition, 那么其中的 Hot Partition 可以超过 3000 RCU 1000 WCU 的限制.
