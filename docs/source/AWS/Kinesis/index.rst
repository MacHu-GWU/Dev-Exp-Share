

Kinesis 中的重要概念


Data Stream
Firehose Delivery Stream

raw -> Data Stream -> Firehose Delivery Stream -> output -> S3 / Redshift / Elastic Search / Splunk



Firehose 触发的 Lambda, 并不直接将 Output Load 到 S3 / Redshift 中, 而是只输出 Binary Output
------------------------------------------------------------------------------

Firehose 需要
