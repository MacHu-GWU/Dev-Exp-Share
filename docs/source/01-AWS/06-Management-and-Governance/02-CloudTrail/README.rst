AWS CloudTrail Docs
==============================================================================

简单来说, CloudTrail 是用于记录 AWS API 的使用. 无论 API Call 的来源是 网页界面, 还是 Command Line, 还是 SDK. 用于记录, 谁, 在什么时候, 做了什么.

Reference: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html

- Cloudtrail is an API logging service that logs API calls made by AWS
- It does not matter if API calls from the CMD, SDK or Console
- All created logs are placed in to a designated S3 bucket, with these features:
    - Cross Account bucket for multiple accounts
    - Limit access to logs
    - Encrypted
