AWS Glue
==============================================================================



AWS Glue 是一个什么样的服务?
------------------------------------------------------------------------------

AWS Glue 的招牌是 Serverless ETL 服务. 本质上 AWS Glue 的后台是 Spark. 你只要定义了 Source, Transformation, Target, AWS Glue 就会为你分配所需要的计算资源, 并帮你进行 ETL.

AWS Glue 的子模块:

- AWS Glue Catelog: 一个 Data Catalog 的服务, 相当于 Hadoop Metadata Store. 定义了 Source, Schema, Ownership.
- AWS Glue Crawler: 能自动扫描 Source, Detect Schema, 并生成对应的 Data Catalog. 然后能自动的发现数据增量, 不断从数据库中抓取数据.
- AWS Glue Studio: 是一个方便用户编写 Glue ETL Script 的模块, 用可视化的方式.