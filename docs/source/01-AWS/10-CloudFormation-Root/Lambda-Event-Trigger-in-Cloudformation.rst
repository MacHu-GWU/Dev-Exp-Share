Lambda Event Trigger in Cloudformation
==============================================================================

Reference:

- Event Source Mapping: https://docs.aws.amazon.com/lambda/latest/dg/intro-invocation-modes.html?shortFooter=true

在 Lambda Console 设置根据 S3 Put Object 或是 SQS 触发 Lambda 很容易, 通过 AWS CLI 设置 event 就麻烦一点, 通过 Cloudformation 设置最一劳永逸, 复用程度最高, 但是也最难学. 本文就主要来讲讲怎么用 CloudFormation 来设置:

对于异步根据服务触发的情况, 比如 S3 Put Object, Cloudwatch Event, Cloudformation Resource 的定义通常在 Lambda 下面:

- S3 Event: ``AWS::S3::Bucket LambdaConfiguration`` https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html?shortFooter=true
- CloudWatch Event: ``AWS::Events::Rule`` https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html?shortFooter=true

对于基于轮询的服务, Cloudformation Resource 的定义通常在 Lambda 下面:

- Kinesis, DynamoDB, SQS: ``AWS::Lambda::EventSourceMapping`` https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html