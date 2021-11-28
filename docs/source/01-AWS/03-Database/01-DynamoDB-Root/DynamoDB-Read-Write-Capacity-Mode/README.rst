DynamoDB Read Write Capacity Mode
==============================================================================

.. contents::
    :local:


两个重要术语 RRU 和 WRU
------------------------------------------------------------------------------

- Read Request Unit (RRU):
    - 1 个 strong consistence read, 或 2 个 eventually consistence read 对于一个 4KB 的 item, 如果 item 不超过 4KB, 按照 4KB 计算. 大于 4KB 的 item 会除以 4KB 然后向上取整.
    - transaction read request 需要两个 RRU.
- Write Request Unit (WRU):
    - 1 个 write request 对于 1KB 的 item (超过的话计算和 read 同理). Transaction write request 需要 2 个 WRU

注意: Global Secondary Index 也占用额外的 R/W RU.

参考资料:

- Read Request Units and Write Request Units: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html#HowItWorks.requests


On Demand Mode vs Provisioned Mode
------------------------------------------------------------------------------

主要有两种收费模式, 在创建表的时候可以指定, 创建完表之后还可以修改:

1. On Demand 模式, 根据你所使用的 R/W Unit 收费. 如果你有下列情况, 请用 On Demand 模式
    - You create new tables with unknown workloads. 不知道新表的 Workflow.
    - You have unpredictable application traffic. 你的 App Traffic 不规律, 无法预测.
    - You prefer the ease of paying for only what you use. 你想偷懒, 不想被多收钱.
2. Provisioned 模式, R/W 固定, 或是通过 Auto Scale 自动


Dynamodb Pricing
------------------------------------------------------------------------------

Dynamodb

