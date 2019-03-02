.. _Read-Credentials-in-Lambda-CN:

在 Lambda 中使用密码信息
==============================================================================

Keywords: Lambda, Password, Credential, KMS, Key Management Serice, 密码

考虑一个常用的场景, Lambda 需要连接 Database, 进行读写数据. 那么这个密码要放在哪里呢?


常用的做法
------------------------------------------------------------------------------

为 Lambda 赋予 S3 的读写权限, 那么可以将密码以文件的形式存放在同一个账号下的 S3 上. 然后在 Lambda 中从 S3 的文件中读取密码.

这种做法本身安全, 但是在开发者的本地电脑上编辑这个 S3 和传输的过程中, 如果被入侵了, 就会有危险.


使用 KMS (Key Management Service)
------------------------------------------------------------------------------

KMS 是一套非对称加密的服务, 用于加密 较短的敏感信息.

简单来说, 我们可以创建一个 Key, 这个 Key 可以用来 **在 Lambda Console 界面将用户输入的敏感信息加密, 加密后的信息以环境变量的形式存储在 Lambda 的运行环境中. 然后告诉 Lambda 这个用于加密的 Key 的 ARN. 同时我们也在 Key 中设定, 允许你的 AWS IAM 登录账户, 以及 Lambda 的 Role 使用这个 Key (分别对应于, 你在 Console 加密信息的行为, 和 Lambda 运行时解密的行为). 那么我们就可以在 Lambda 中解密环境变量, 得到密码了**.

这里有几个容易出错的点:

- Lambda 的 Role 要有 KMS 权限
- Lambda 要指定使用这个 Key 的 ARN
- Key 要指定运行运行 Lambda 的 Role 访问自己
- Key 要指定实际操作用户的 IAM 访问自己


代码实例
------------------------------------------------------------------------------

Lambda Handler 中的代码

.. code-block:: python

    import os
    import boto3

    def handler(event, context):
        kms = boto3.client("kms")
        password = kms.decrypt(
            CiphertextBlob=b64decode(os.environ["DB_PASSWORD"])
        )["Plaintext"]
