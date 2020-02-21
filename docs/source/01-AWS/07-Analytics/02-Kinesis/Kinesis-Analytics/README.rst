

Kinesis Analytics 是一个流数据分析的工具. 整个 Kinesis 对标的开源工具是 Kafka.

我们来看一个具体的例子, 股票市场自动化交易平台.

Kinesis Analytics 解决问题的模型是这样的:


举例来说

首先你要有一个数据源, ``Source Stream``, 这里面的数据是流式的 record. 每一条有 field. 你可以将其想象为一个二维的数据表.

Kinesis Analytics 可以定义一个虚拟的二维表, 这个二维表里的数据是我们分析的结果. 这个表叫做 ``Destination Stream``.

而从 ``Source Stream`` 到 ``Destination Stream`` 的转换是通过 ``Pump`` 来进行的, 而这个 ``Pump`` 就是一个具体的 SQL 语句.

而 Kinesis Analytics 是


- INTERVAL: INTERVAL '1' DAY


Kinesis Analytics vs Redshift Pricing Compare
------------------------------------------------------------------------------

- Kinesis: https://aws.amazon.com/kinesis/data-analytics/pricing/
- Redshift: https://aws.amazon.com/redshift/pricing/

- Kinesis: 1 KPU = 1 vCPU, 4GB Memory $0.11 per Hour
- Redshift: dc2.large = 2 vCPU, 15 GiB, 0.16TB SSD, 0.6 GB/sec, $0.25 per Hour
