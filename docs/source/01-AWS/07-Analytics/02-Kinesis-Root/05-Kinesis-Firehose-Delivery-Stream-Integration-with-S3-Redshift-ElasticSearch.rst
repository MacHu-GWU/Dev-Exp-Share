Kinesis Firehose Delivery Stream Integration with S3 Redshift ElasticSearch
==============================================================================

Ref:

- Select destination: https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html


To Redshift
------------------------------------------------------------------------------

Ref:

- https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html?shortFooter=true#create-destination-redshift

- 实现方式上, Kinesis Firehose **首先将数据写入 (可以不处理, 也可以处理) S3 (我们称之为  Intermediate Bucket), 然后调用 Redshift Copy 命令将数据读取到 Redshift 中. 读取后并不会删除 S3 上的数据**. 此时, S3 上的数据就是 Source Record.
- 如果你配置了 **Transform Lambda Function, 那么你可以选择打开 Source Record backup**, 将处理前的数据存入另一个 S3 Bucket. 此时 Intermediate Bucket 上的数据是处理好的数据.
- 如果担心 Redshift Copy Command 失败, 你可以使用 Retry Duration 设置进行重试. Firehose 每 5 分钟重试一次. 假设你设置 Retry Duration = 60 Min, 则总共会尝试 12 次.


To Elastic Search
------------------------------------------------------------------------------

Ref:

- https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html?shortFooter=true#create-destination-elasticsearch

- Backup Mode: 你可以选择只备份出错的数据, 或是备份全部数据.



Failure Handling
------------------------------------------------------------------------------

一共有两个环节可能出错:

- Delivery Failure Handling: https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html?shortFooter=true#retry
- Transform Failure Handling: https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html?shortFooter=true#data-transformation-failure-handling

**Delivery Failure Handling**:

- Destination = S3: 会尝试 24 小时, 如果由于你的 IAM Role, 或是 S3 配置错误导致失败, 超过 24 小时如果你没有修复, 那么期间的数据将会丢失.
- Destination = Amazon Redshift: 你可以设置 retry duration 不断尝试, 超过时间仍然失败的话, 由于使用 S3 作为中间媒介, 原始数据将会被保存在 S3 上.
- Destionation = Amazon Elasticsearch Service: 同 Redshift

**Transform Failure Handling**:

- 默认 Kinesis 会重试 3 次 Lambda Function, 如果失败, 则失败的数据会被存入 s3://bucket-name/processed-failed 中.
- 你可以启用 Source Record Backup.

Delivery Failed 和 Transform Failed 并称为 Processed Failed.
