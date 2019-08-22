Per Account S3 Bucket
==============================================================================

在许多 AWS 服务的使用过程中, 需要一个地方储存临时过渡文件, S3 Bucket 无疑是最好的选择. 例如, CloudFormation 需要将 Template 上传后再执行; AWS Lambda 需要将 代码上传后再部署; AWS Athena 将 Query 结果临时放在 S3 Bucket 中再显示; CloudTrail 将 API 操作日志储存在 S3 Bucket 中.

所以我建议, 为你的每个 AWS Account 手动创建一个 S3 Bucket, 1 个就好, 在里面划分不同的文件夹, 用于保存不同的文件.

命名规则:

- Bucket Name: ``<aws-account-id>-everything``
- CloudFormation: ``/cloudformation/...``
- Lambda: ``/lambda/...``
- Athena: ``/athena/...``
- CloudTrail: ``/cloudtrail/...``
- ...
