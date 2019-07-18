Kinesis Analytics
==============================================================================

Ref:

- Amazon Kinesis Data Analytics for SQL Applications: How It Works: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works.html

简单来说 Kinesis Analytics 就是在你普通的 Stream 的 Input Output 的中间环节加了一个 Kinesis Application Stream. 而在这个中间的操作只能是一个或多个 SQL 语句.

Kinesis Analytics 适用于以下几种问题:

1. 时间序列分析. 根据 Time Window, 每隔一段时间对一段时间内的数据做处理.
2. 实时监控面板上的数据统计.
3. 实时统计数据.