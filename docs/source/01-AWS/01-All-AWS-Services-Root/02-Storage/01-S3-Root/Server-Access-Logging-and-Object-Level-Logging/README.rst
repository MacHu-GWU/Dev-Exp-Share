Server Access Logging and Object Level Logging
==============================================================================
Keywords: AWS, S3, Access, Log, Logging,


Summary
------------------------------------------------------------------------------
Server Access Logging (SAL) 是 S3 的一个 Feature, 能自动收集对 S3 中的 object 的访问的日志.
 该功能主要用于 security 和 access auditing.

这个功能的工作方式是, 每当有人对 S3 进行读写操作, 就会生成一个 Event, 这个 Event 会被根据 S3 prefix 和 Time period aggregate 到一起变成一个或多个文件. 然后写入到一个另外的 S3 bucket 中. 被监控的 S3 bucket 叫 Source bucket, 用于存储数据的 S3 bucket 叫 Target bucket.


Log Delivery
------------------------------------------------------------------------------
- SAL 在新创建的 S3 bucket 上是默认关闭的. 而开启 SAL 需要一段时间来生效, 通常在 1 小时左右.
- 你可以让多个 Source Bucket 共享一个 Target Bucket.
- 对于 Target Bucket 的写入权限管理的方式推荐使用 bucket policy. AWS 有一个内部的 Account 专门用来收集 SAL 数据, 然后从这个 Account 中将数据写入到 Target Bucket. 这个 Principal 是 ``logging.s3.amazonaws.com``, 你在 Target Bucket policy 中指定允许它写入即可.
- log 被生成之后通常需要几个小时才能被写入到 Target Bucket 中, 这是基于性能考虑, 将日志按照小时聚合能够减少写入的次数.
- log 并不保证 exact once delivery, 它可能被 deliver 多次, 也可能一次都没被 deliver.

Reference:

- `Best effort server log delivery <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html#LogDeliveryBestEffort>`_: 说明了 SAL 不能保证 exact once delivery. 可能有重复数据, 也可能会丢数据 (可能性很低).
- `Bucket logging status changes take effect over time <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html#BucketLoggingStatusChanges>`_: 说明了你启用 SAL 后需要一定时间才能生效.


Log Format
------------------------------------------------------------------------------
S3.

::

    79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes
    79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 891CE47D2EXAMPLE REST.GET.LOGGING_STATUS - "GET /DOC-EXAMPLE-BUCKET1?logging HTTP/1.1" 200 - 242 - 11 - "-" "S3Console/0.4" - 9vKBE6vMhrNiWHZmb2L0mXOcqPGzQOI5XLnCtZNPxev+Hf+7tpT6sxDwDty4LHBUOZJG96N1234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 - -
    79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be A1206F460EXAMPLE REST.GET.BUCKETPOLICY - "GET /DOC-EXAMPLE-BUCKET1?policy HTTP/1.1" 404 NoSuchBucketPolicy 297 - 38 - "-" "S3Console/0.4" - BNaBsXZQQDbssi6xMBdBU2sLt+Yf5kZDmeBUP35sFoKa3sLLeMC78iwEIWxs99CRUrbS4n11234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 - Yes
    79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:01:00 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 7B4A0FABBEXAMPLE REST.GET.VERSIONING - "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 113 - 33 - "-" "S3Console/0.4" - Ke1bUcazaN1jWuUlPJaxF64cQVpUEhoZKEG/hmy/gijN/I1DeWqDfFvnpybfEseEME/u7ME1234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 - -
    79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:01:57 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DD6CC733AEXAMPLE REST.PUT.OBJECT s3-dg.pdf "PUT /DOC-EXAMPLE-BUCKET1/s3-dg.pdf HTTP/1.1" 200 - - 4406583 41754 28 "-" "S3Console/0.4" - 10S62Zv81kBW7BB6SX4XJ48o6kpcl6LPwEoizZQQxJd5qDSCTLX0TgS37kYUBKQW3+bPdrg1234= SigV4 ECDHE-RSA-AES128-SHA AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 - Yes

Reference:

- `Amazon S3 server access log format <https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html>`_: 说明了 SAL 的 log format.


Server Access Logging:

- Provides detailed records for requests that are made to a bucket (source bucket).
- Useful for security and access auditing.
- Source and target buckets should be in the same region.
- Need to grant Amazon S3 log Delivery group write permissing on the target bucket.

Object Level Logging:

- Logging happens at the object level.
- Leverage CloudTrail trail.
- Useful for security and access auditing.

Reference:

- Amazon S3 Server Access Logging: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html
- How Do I Enable Object-Level Logging for an S3 Bucket with AWS CloudTrail Data Events?: https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-cloudtrail-events.html