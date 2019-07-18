Big Data Specialist Redshift 考点
==============================================================================


选择 Distribution Style
------------------------------------------------------------------------------

Distribution Style 指的是数据是如何储存在各个实体 Node 上的. 比如是每个 Note 保存一份副本 (All)? 还是按照某个 Column 的 Hash Key 分配? 还是每个 Note 平均分配?

- Auto: 当表很小时, 使用 ALL, 当表变大后, 使用 Even, 然后就再也不变了.
- Even: 用轮询的方式, 将数据平均的分配到 Node 上. 当使用 Key 和 All 的好处不是很明显时使用这一模式.
- Key: 使用一个 Column 作为 Partition Key. 当该表比较大, 而有一列经常是 Primary Key 并且变化非常大, 还经常需要做 Join 时, 使用这一模式.
- All: 每个 Node 的第一个 Slice 上都有该 Table 的一个副本. 常用于很小的表, 并且频繁被 Join 的表. 比如 Tag(tag_id, tag_name). 总共也不过 1000 个 Tag, 而 TagName 很长, 在其他表中你只储存 Id, 而你的查询结果中要使用 TagName.


Redshift Spectrum
------------------------------------------------------------------------------

Ref:

- Using Amazon Redshift Spectrum to Query External Data: https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html?shortFooter=true

- 什么是 Spectrum: 使用 Redshift 底层的查询引擎, 查询 Redshift 外的数据 (比如 S3)的一个工具. 你依然是在 Redshift 中创建表, 不过是创建的 External Table, 查询依旧在 Redshift 上进行. 比如你想将 Redshift 中的表和 Athena 中定义的位于 S3 中的表做 Join, 那么 Spectrum 就是你需要额工具.
- External Schema (Database), External Table: 指定 Athena 中的 Database, 或是 AWS Glue 中的 catalog, 或是 Hive Metastore.


使得 Redshift 和 S3 之间通过 VPC 传数据, 而不通过公网
------------------------------------------------------------------------------

Ref:

- Working with VPC Endpoints: https://docs.aws.amazon.com/redshift/latest/mgmt/enhanced-vpc-working-with-endpoints.html

1. 创建一个 VPC Endpoint, Redshift 在这个 VPC 里, S3 和该 VPC 需要在同一个 Region.
2. Attach Endpoint Policy to your endpoint to more closely manage access to your data.
3. Enable Enhanced VPC Route when you create a cluster.
4. Enable Domain Name Service (DNS) resolution in your VPC.
