Lambda Layer Sharing
==============================================================================
Keywords: AWS Lambda Function Layer, Share, Sharing


为什么要 Share Lambda Layer?
------------------------------------------------------------------------------
在企业项目中通常有需要将 App 部署到多个 AWS Accounts, DevOps, dev, test, prod 等. 对于 Layer 来说如果在每一个 Accounts 上都部署一套, 这样做非常不推荐. 正确的做法是在你 host code artifacts 的那个 Account 存放 Layer Version, 然后将这个 Layer Version (需要一个个具体的 Version Share, 而不能一次性 Share 一个 Layer 下的所有 Version) 分享给其他需要的 Accounts. 这是因为 AWS Lambda Layer 本质上就是一个 Binary Artifacts, 一个压缩包. 而且作为 Versioned Artifacts 则必须要是 Immutable 的.  因为你在部署 App 的时候肯定是要指定一个准确的 Layer Version, 而你如果说每个 Accounts 上都部署一套 Layer, 这就相当于一个相同的 Layer 发布了许多份, 你就会有额外的工作用来确保不同 Accounts 上的 Layer 本质上是同一个, 这些工作首先容易出错, 而且浪费人力资源.


代码示例
------------------------------------------------------------------------------
请参考下面这个示例代码, 了解如何 Grant 和 Revoke permission, 以及如何跨 Account 部署 Lambda Layer.

.. literalinclude:: ./test.py
   :language: python
   :linenos:

Reference:

- `Creating and sharing Lambda layers <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_
- `Configuring layer permissions <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-permissions>`_
- `Granting layer access to other accounts <https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html#permissions-resource-xaccountlayer>`_
- `add_layer_version_permission <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/add_layer_version_permission.html>`_
- `remove_layer_version_permission <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/remove_layer_version_permission.html>`_
- `CloudFormation Layer Version Permission <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html>`_
- `CDK Layer Version Permission <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/LayerVersionPermission.html>`_
