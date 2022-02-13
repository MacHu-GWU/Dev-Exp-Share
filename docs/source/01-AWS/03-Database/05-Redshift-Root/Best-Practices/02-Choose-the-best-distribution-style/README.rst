.. _aws-redshift-best-practice-choose-the-best-distribution-style:

Choose the best distribution style
==============================================================================
Keywords: AWS Redshift, Best practice

首先要知道的是 Redshift 是一个分布式系统. 数据需要根据 distribution key 来决定由哪个节点来处理这个数据.


官方文档推荐用以下几个原则来决定哪个 Column 成为 Distribution Key

- Distribute the fact table and one dimension table on their common columns.
    - 比如你有个大的 fact table, event
