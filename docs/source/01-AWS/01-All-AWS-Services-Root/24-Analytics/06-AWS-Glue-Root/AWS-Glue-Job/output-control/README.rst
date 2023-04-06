控制 Glue 在 S3 的输出
==============================================================================



控制 Partition
------------------------------------------------------------------------------

如果你的 DataFrame 有一个 Low Cardinality 的 Column, 那么这个 Column 是可以被用作 Partition 的. 也就是 ``s3://{bucket}/datalake/year={year}/month={month}/day={day}/abc.json`` 中的这些 partition 部分. 而数据被吸入文件的时候, 这些用作 Partition 的 Column 会被自动移除.

要注意的点:

1. partition 的 value 需要是字符串, 而且如果在 query 的时候你如果想要用于 >=, <= 比较, 那么字符串要注意 Zero Padding
2. 有的 row 这个 partition key Column 会不存在, 所以在 dynamic dataframe 中记得 fill default value for NA, 确保这个有值, 以便能查询到

Ref:

- https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-partitions.html


控制 Output 的文件数量
------------------------------------------------------------------------------
由于 Spark 的实现机制是一个 Partition 是一个独立的读写单元, 也就是一个 Partition 要生成一个文件. 你要减少生成的文件数量只有用减少 Partition 的数量. 这有三个方法:

1. 用 groupFiles 选项, 限制每个 Partition 最小的数据量, 也就是每个 Partition 最后获得的数据一定大于这个值, 从而生成大文件.
2. 用 pyspark 的 coalesce() API, 将多个 Partition 上的数据合并成较少的 Partition 上, 并且利用已有信息尽量减少数据移动. 问题是只能减少 Partition 不能增加. 设置为 1 则会生成 1 个大文件. 但是小心磁盘空间可能会爆.
3. 用 pyspark 的 repartition() API, 重新分配 Parition, 旧数据不删除, 重新生成新数据, 这里会有全量的数据移动. 所以性能差于 coalesce() API. 不推荐使用.

Glue 以外的方案你可以用 Lambda 对文件夹进行触发扫描, 然后手动将其合并.


Ref:

- https://aws.amazon.com/premiumsupport/knowledge-center/glue-job-output-large-files/


控制 Output 的文件名
------------------------------------------------------------------------------
简单来说你无法控制. 因为 Spark 是以 Partition 为写入单位根据内部的 run id 作为 naming convention 的以避免覆盖已有文件. 不过你可以在 Glue ETL Script 最后用 boto3 API 扫描并重命名.
