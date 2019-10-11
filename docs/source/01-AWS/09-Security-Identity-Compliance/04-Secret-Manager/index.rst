.. _aws-secret-manager:

Secret Manager
==============================================================================

Secret Manager 通常跟 :ref:`KMS <aws-kms>` 结合使用. KMS 储存的是加密用的密钥, 而 Secret Manager 储存的是使用 KMS 加密过后的数据. 并随时准备为可信的 App 提供简单的解密方案.

另一个便利是, Secret Manager 可以和 AWS 提供的数据库服务无缝连接, 例如 RDS, Redshift, DocumentDB. 使得 RDS 的密码能自动定期修改, 同时自动更新 Secret Manager 内加密后的用户名和密码. 这才是 Secret Manager 的杀手功能.

如果你要读取加密信息, 你可以这样做:

.. code-block:: python

    import boto3
    import json
    import base64

    client = boto3.client(service_name="secretsmanager")

    response = client.get_secret_value(SecretId="secret-name")
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        secret = decoded_binary_secret

    # your code here
    data = json.loads(secret)
    username = data["username"]
    password = data["password"]
    ...


Required IAM Policy to Access Secret
------------------------------------------------------------------------------

当你使用 IAM User 或是 IAM Role 访问特定的 Secret 的时候, 你最少需要多少 Policy 呢?

虽然 AWS 提供了 官方的 arn:aws:iam::aws:policy/SecretsManagerReadWrite Policy, 但是这个权限太大了. 我推荐自定义创建一个 IAM Policy, 并且明确指定 Secret Arn. 这样能保证这个 Policy 能且只能访问我们指定的 Secret. 虽然 Secret Manager 使用了 KMS 进行加密, 但是从用户角度来说, 不需要 KMS 的权限.

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": [
                    "arn:aws:secretsmanager:us-east-1:111122223333:secret:my-example-secret-0f4dFe"
                ]
            }
        ]
    }
