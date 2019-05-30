CloudFormation
==============================================================================

和 Terraform 类似, CloudFormation 用一个配置文件定义了一个项目或是一个APP所要用到的全部 AWS Resource.

Template 相关的概念:

- AWS Resource: AWS 上的各种服务就叫做 AWS Resource, 例如 S3, EC2. 一个具体的实体, 比如 S3 Bucket, 叫做 "a resource".
- Property: AWS Resource 的属性, 比如 S3 Bucket 的属性有 bucket_name.
- Stack: 一系列组合在一起的 AWS Resource, 相互之间可能有依赖关系.


- AWS Resource and Property Types Reference: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html
- AWS Properties S3 Bucket: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html


创建一个 Template, 并创建 Stack


修改一个 Template 并应用更改到 Stack


移除整个 Stack


CloudFormation Template
------------------------------------------------------------------------------



怎样找到你在 Console 中的设置在 Template 中对应的脚本?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

新手写 Template 时有一个很难克服的问题就是: **在 Console 里都会设置, 系统也能正常运行, 一旦使用 Template, 要设置哪些 Property, 设定值是什么? Console 里的某些设置对应在 Template 里又是什么?**. 这里我发现了一个诀窍可以解决这个问题:

1. 在 Console 中对设置好所有的 Resource, 让系统跑起来.
2. 重新设置一套环境, 目的是用 CloudFormation 重现刚才所有的设置, 注意, 不要删除掉之前设置好的 Resource, 之后要随时作为参考.
3. 使用 AWS CLI 或是 Boto3 API 调用各种函数, 查看各个 Resource 的 Config Data. 例如: 对于 EC2 可以用 `ec2_client.describe_instance_attribute <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instance_attribute>`_, 对于 S3 可以用 `s3_client.get_bucket_policy <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy>`_, 对于 Lambda 可以用 `lambda_client.get_function <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function>`_, 对于 API Gateway 可以用 `apigateway.get_method <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_method>`_. **总之就是调用查看你配置好的 Resource 的详细数据**, 再和 `AWS Resource and Property Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ 这篇 CloudFormation 的 Template 文档相互比对. 你就知道有哪些 Resource 需要设置了.


怎样编辑一个非常大的 Json 文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Terraform 中, 你可以将你的整个系统, 分为多个子模块, 放在 .tf 文件 中. 然后使用 terraform 命令行扫描一个目录下的所有 .tf 文件, 自动将其合并.
CloudFormation 并没有这个功能.

一个改良的做法是, **将一个大的 .json 文件分成多个子模块, 然后每次用 Python 脚本将这些文件全部合并成一个 Json**. 然后再 Git 中 ignore 生成的最终 json 文件. 通过这样做, 我们 **可以在子模块的 json 文件中加注释**, CloudFormation 不允许上传非标准格式的 json.

编辑 CloudFormation 的工具:

- Sublime:
    - JsonComma: 自动修正多余和缺少的逗号
    - Pretty Json: 将 Json 格式化
- PyCharm:
    - AWS CloudFormation: 自动补全 Resource 的 Type, Property, Reference. 点击 Reference 自动跳转. File Structure 导航栏. 自动 Validate 模板, 给予错误提示, 自动修正多余和缺失的逗号, 自动格式化 Json.


application/json

{
   "mpl_id": "$input.params('mpl_id')"
}