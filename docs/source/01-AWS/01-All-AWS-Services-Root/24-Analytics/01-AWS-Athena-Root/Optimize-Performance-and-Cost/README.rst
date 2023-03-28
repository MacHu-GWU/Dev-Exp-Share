Optimize Performance and Cost
==============================================================================

The content of this tutorial are experience from hands-on experiment based on this blog post: https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/

.. contents::
    :depth: 1
    :local:


Partition (分区) 和 Bucketing (分桶)
------------------------------------------------------------------------------

Partition (分区) 和 Bucketing (分桶) 是两种将数据分区的技术. 两者都是为了在分布式的查询引擎中提高性能, 减少被扫描的数据, 提高查询的速度.

.. note::

    这里的 bucketing 指的并不是 S3 Bucket 中的 Bucket, 而是一种逻辑概念.

首先我们要明白一个概念 Cardinality (Number of element in a set). 它指的是一个字段中, 不同的值的个数. 比如你有 10 年的 1 亿条电商购买数据. year 字段可能只有 10 种可能, month 只有 12 种, day 只有 31 种. 那么这几个字段都是 ``Low Cardinality`` 的. 而对于 OrderId, 可能有千万个购买行为, 那么就有几千万个不同的 OrderId, 那么这个字段就是 高 ``High Cardinality`` 的.

.. note::

    字段是指二维表数据中的 Column, 或者 Json 中的 Key.

Partition 常用于 ``Low Cardinality`` 的字段. 常用于年月日时间这一类查询中常用 Range ( ``start <= time <= end``) 进行过滤的字段. 在 S3 Bucket 中的实现表现为使用不同的 S3 Key prefix. 在文件系统中表现为使用不同的文件夹. 这样使得查询时能少扫描一些数据.

Bucketing 常用于 ``High Cardinality`` 的字段. 常用于 OrderId 这一类人类不可读, 但是机器可读的 Id 类型的字段. 常用于我们指定具体的值 或者进行 Join 的查询 (``OrderId = "f90a9d8fb3671f8f4a488585461b6144"``). 在 S3 Bucket 中的实现表现为使用不同的 S3 Key prefix. 在文件系统中表现为使用不同的文件夹. 其原理是指定比如 256 个桶, 然后将 ``OrderId`` 进行 hash 后除以 256 取余然后放在不同的桶中. 这样在查询具体订单的相关信息时时能够快速的定位到具体的桶中, 使得只扫描很少的数据. 并且在做 Join 的时候, 所有的相关数据都会被放到桶一个桶中, 所以 JOIN 的效率会高.

在同时使用 Partition 和 Bucketing 时, S3 Key 的 pattern 长这样: ``s3://my-bucket/order-dataset/year=2010/month=01/day=15/001`` ... ``s3://my-bucket/order-dataset/year=2010/month=01/day=15/256``. ...



Compress and Split file
------------------------------------------------------------------------------


Optimize file sizes
------------------------------------------------------------------------------


Use Columnar data store generation
------------------------------------------------------------------------------


Use ``Limit`` clause with ``Order By``
------------------------------------------------------------------------------


Join Large table on the Left Small table on the right
------------------------------------------------------------------------------


``GROUP BY`` highest cardinality column first, low cardinality column last
------------------------------------------------------------------------------


Use regexp_like instead of ``LIKE`` if multiple token used
------------------------------------------------------------------------------


Use approx_distinct(my_column) instead of COUNT(DISTINCT my_column) if the exact number doesn't matter
------------------------------------------------------------------------------


Only include the columns that you need
------------------------------------------------------------------------------

