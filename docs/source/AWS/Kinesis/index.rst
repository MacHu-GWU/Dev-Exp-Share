Kinesis
==============================================================================


Difference betwee Kinesis vs SQS
------------------------------------------------------------------------------

- Kinesis can scale way larger than SQS by adding sharding.
- Kinesis usually send batch records to process, but SQS usually consume record one by one.
- There's no subscription model and topic broker in kinesis.





Kinesis 中的重要概念


Data Stream
Firehose Delivery Stream

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
