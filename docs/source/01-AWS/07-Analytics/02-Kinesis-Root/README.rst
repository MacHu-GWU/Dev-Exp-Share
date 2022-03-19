Kinesis Root
==============================================================================

.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst


Important Concept
-----------------

Reference: https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html

- Kinesis Stream:
    - Shard
    - Producer
        - PutRecords API: Synchronous, immediately available after captured, need manually implement retry, batch.
        - Kinesis Producer Library (Java): Asynchronous, High Performance (high concurrence), but with larger delay
    - Consumer
- Kinesis Firehose (Delivery Stream):
- Kinesis Analytics: 每隔一段时间, 对近期 Stream 中的数据用 SQL 进行分析, 然后将结果汇总, 传给 Destination, 可以是 Kinesis Stream, Firehose, Lambda.
- Kinesis Video Stream:
- KPL (Kinesis Producer Library):
- KCL (Kinesis Consumer Library):


FAQ
---

Reference: https://aws.amazon.com/kinesis/data-streams/faqs/

- Q: Is the order of what consumer received is same as the order produced?
- A: Yes, It provides ordering of records, as well as the ability to read and/or replay records in the same order to multiple Amazon Kinesis Applications


Note
----

- Firehose 触发的 Lambda, 只专注于数据处理, 并返回处理后的 Binary Output, 并不负责将 Output Load 到 S3 / Redshift 中. Firehouse 自带将 Output 写入 S3 / Redshift / Elasticsearch / Splunk 的功能.
- Kinesis Stream Consumer 将数据按照 X Min / Y KB (取最先达成的那个) 的限制进行打包交给 Lambda 函数处理. 每一个 Shard 会独立于彼此进行运作, 将数据打包. 也就是说, 有多少个 Shard, 就会同时触发多少个 Lambda.
- Difference Between Kinesis Stream vs SQS.
    - Kinesis can scale way larger than SQS by adding sharding.
    - Kinesis usually send batch records to process, but SQS usually consume record one by one.
    - There's no subscription model and topic broker in kinesis.
- Yes, each shard can only have one processor at a given moment (per application).


Data life cycle in Kinesis Stream Pipeline
------------------------------------------------------------------------------

raw -> Data Stream -> Firehose Delivery Stream -> output -> S3 / Redshift / Elastic Search / Splunk


Firehose 触发的 Lambda, 并不直接将 Output Load 到 S3 / Redshift 中, 而是只输出 Binary Output
------------------------------------------------------------------------------

Firehose 需要



Firehouse 的输出可以跟哪些 AWS 服务对接?
------------------------------------------------------------------------------

- AWS S3: 将输出或 原封不动, 或 进行格式转换, 或 用Lambda进行处理后存到 S3 里.
- AWS Redshift: 将输出用 Copy 命令 Load 到 Redshift 上.
- AWS Elasticsearch Service: 将输出 Load 到 Elasticsearch 上.
- AWS Splunk: 将输出 Load 到 Splunk 日志服务器上.



Sharding
--------

Kinesis Stream Consumer 将数据按照 X Min / Y KB (取最先达成的那个) 的限制进行打包交给 Lambda 函数处理. 每一个 Shard 会独立于彼此进行运作, 将数据打包.


Kinesis Producer Library (KPL)
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/streams/latest/dev/developing-producers-with-kpl.html

KPL 是一个 SDK 开发者工具, 相比 AWS SDK 里的 Kinesis PutRecord 命令而言, 额外提供了这些功能:

- Async PutRecord: 异步, 提高性能.
- Collection: 将多个 Record 打入 Buffer.
- Aggregation / Batch: 将多个 Record 进行 Aggregation, 然后一起发送. 将收到的批量 Record 批量 Batch 处理.


Kinesis Data Analytics for SQL Application
------------------------------------------------------------------------------

Docs: https://docs.aws.amazon.com/kinesisanalytics/latest/dev/what-is.html

Kinesis Data Analytics 是一个将 Stream 中的数据直接对接给 SQL Application 的服务, 用实时数据处理数据, 然后返回结果.

