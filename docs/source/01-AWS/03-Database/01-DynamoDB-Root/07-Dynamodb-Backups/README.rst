.. _dynamodb-backups:

Dynamodb Backups
==============================================================================
为了数据库容灾, Dynamodb 提供了两种备份方式: On-demand backup 和 Point-in-time Recovery.

Reference:

- DynamoDB Backups: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backups.html

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


On-Demand Backup And Restore
------------------------------------------------------------------------------
Dynamodb 使用 Snapshot 技术, 使得备份和恢复对性能几乎没有影响. Dynamodb 支持两种备份方式:

1. AWS Backup Service: AWS Backup 是一个单独的 AWS 服务, 支持对多种 AWS Resource 的备份. 其中就包括 Dynamodb.
2. Dynamodb Backup: 是一个 Dynamodb 内置的功能, 你可以在 Console 上点击, 或是用一个 API Call 就对 Table 的全部数据做一个备份.


Point in Time Recovery for Dynamodb
------------------------------------------------------------------------------
简单来说 Point-in-time (PIT) 就是一种持续备份的机制. 你无需像 Dynamodb Backup 机制一样定期调用 API 进行备份. 不过 PIT 备份最多能恢复到 35 天前的状态.

要特别注意几点:

1. 如果你禁止了 PIT 又启用了 PIT, 那么你的恢复时间将被重置, 你最多恢复到你最新一次启用 PIT 时刻的状态.
2. 你选择恢复到之前时刻, 该操作只恢复数据, 不恢复 Settings. 你的 Settings 还是跟你进行恢复操作前一样.
