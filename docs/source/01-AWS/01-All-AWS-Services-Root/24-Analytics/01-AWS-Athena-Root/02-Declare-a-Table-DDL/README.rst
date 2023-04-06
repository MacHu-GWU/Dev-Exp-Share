.. _aws-athena-ddl:

AWS Athena Declare a Table - DDL
==============================================================================
Keywords: AWS, Athena, Glue, Table, DDL, Define, Declare


AWS Glue Catalog 是 AWS 上的通用 Data Metadata Store. 对应于 Hadoop 生态中的 Hive Data Catalog.

AWS Athena 的 DDL (data declaration language) 是一种用来定义 Table Schema 的语法. 由于 Athena 底层使用了在 Hadoop Hive 基础上修改来的系统, 所以 Athena DDL 的语法和 Hive 相似度高达 99%.

为了创建一个 Table, 定义 Schema, 以及定义 Seder (就是序列化库, 决定了如何从文件中读取数据), 这些步骤其实是很繁琐的. 即使是受过良好训练的开发者也很难一次性写出准确的 DDL. AWS 提供了几种创建 Table 的方式:

1. 用 AWS Glue Crawler, 自动分析 S3 文件夹下的所有文件, 生成 DDL, 并创建 Table
2. 用 AWS Glue Console, Manually create Table
3. 在 Athena 中手写 DDL, 并执行 SQL 语句进行创建

方法 1 很方便, 但要求你的数据比较规整, 不然你很难控制 crawler 的行为, 生成的 schema 很可能不满足你的需求.

方法 2 比较推荐, 创建过程很 user friendly, 创建之后还能修改, 对 sede property 以及各种参数在 UI 中做进一步的调整, 避免了手写 DDL 频繁出现的语法错误

方法 3, 如果你是大神, 请自便.

参考资料:

- Serde, 数据读取参数, 比如设置 CSV 的 delimiter, 是否有 header 等: https://docs.aws.amazon.com/athena/latest/ug/supported-serdes.html
- 对于 JSON 中的 array, struct 等数据结构的处理: https://docs.aws.amazon.com/athena/latest/ug/json-serde.html
