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
