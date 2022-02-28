.. _aws-redshift-spectrum-root:

AWS Redshift Spectrum Root
==============================================================================

Ref:

- Using Amazon Redshift Spectrum to Query External Data: https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html

.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst


What is AWS Redshift Spectrum
------------------------------------------------------------------------------
AWS Redshift Spectrum 允许你不把数据 Load 到 Redshift Cluster 中, 直接对 AWS S3 上的数据进行查询的工具. 实际的查询和计算都是由 AWS Redshift Spectrum Layer 完成的.





For queries that are closely tied to a Redshift data warehouse, you should lean towards Redshift Spectrum. Spectrum makes it easier to join data on S3 with data in Redshift, and to load those results into a Redshift table.

If all your data is on S3, lean towards Athena. If you’re not looking to analyze Redshift data, you probably don’t want to add the effort and cost of spinning up a Redshift cluster just to use Spectrum. Athena should be your go-to for reading from S3.

If you are willing to pay more for better performance, lean towards Redshift Spectrum. As we’ve covered in the previous sections, Spectrum doesn’t rely on pooled resources, so it can provide more consistent performance. However, this might increase your Redshift compute usage and require you to pay more for a larger cluster.


- 什么是 Spectrum: 使用 Redshift 底层的查询引擎, 查询 Redshift 外的数据 (比如 S3)的一个工具. 你依然是在 Redshift 中创建表, 不过是创建的 External Table, 查询依旧在 Redshift 上进行. 比如你想将 Redshift 中的表和 Athena 中定义的位于 S3 中的表做 Join, 那么 Spectrum 就是你需要额工具.
- External Schema (Database), External Table: 指定 Athena 中的 Database, 或是 AWS Glue 中的 catalog, 或是 Hive Metastore.