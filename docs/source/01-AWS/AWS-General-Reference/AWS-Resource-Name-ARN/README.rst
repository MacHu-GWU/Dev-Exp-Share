AWS Resource Name ARN
==============================================================================
ARN 是 URI (Unique Resource Identifier) 的一种, 是 Amazon 专用的资源标识符, 用于标识 AWS 上的资源, 例如 S3 Bucket, SQS Queue, DynamoDB Table 等等. 它的格式如下.

ARN Format::

    arn:partition:service:region:account-id:resource-id
    arn:partition:service:region:account-id:resource-type/resource-id
    arn:partition:service:region:account-id:resource-type:resource-id

我自己写了个 Python 库 `aws_arns <https://github.com/MacHu-GWU/aws_arns-project>`_ 用来解析 ARN, 在我的很多项目中我常用它.

Reference:

- Amazon Resource Names (ARNs): https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
