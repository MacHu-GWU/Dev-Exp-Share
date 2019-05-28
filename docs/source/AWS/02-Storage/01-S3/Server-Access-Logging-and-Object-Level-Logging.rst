Server Access Logging and Object Level Logging
==============================================================================

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