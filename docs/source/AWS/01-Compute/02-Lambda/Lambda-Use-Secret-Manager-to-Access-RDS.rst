Lambda Use Secret Manager to Access RDS
==============================================================================

**需要的 IAM Role Policy**:

1. Lambda 并不需要 ``AWSKeyManagementServicePowerUser``, 即使 SecretManager 本身需要使用 KMS. **正确的做法是在 Secret 所使用的 KMS Key 的控制台中, 将 Lambda 所使用的 IAM Role, 添加到 Key users 中**.
2. 为了访问 SecretManager 中的数据, **我们需要 SecretManager 的 Read 权限. 但是 AWS Managed 自带的 Policy 中的 SecretsManagerReadWrite 中有对 SecretManager 的写权限. 我们并不希望 Lambda 有这个写权限. 所以我们需要自己创建一个 Policy**. 点击 Create Policy, 选择 Service 为 Secrets Manager, 选择 Actions 为 Read, 选择 Resources 为 All Resoures, 不对 Request Conditions 进行设置.

**Lambda Code**:

`pysecret <https://github.com/MacHu-GWU/pysecret-project>`_ 是一个 Python 库, 可以用最少的代码从 AWS Secret Manager 中读取数据.

.. code-block:: python

    from pysecret import AWSSecret

    aws_profile = "my_aws_profile"
    secret_id = "db_credential"
    aws = AWSSecret(profile_name=aws_profile)
    password = aws.get_secret_value(secret_id=secret_id, key="password")
    ...
