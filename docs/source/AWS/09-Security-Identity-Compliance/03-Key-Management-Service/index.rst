.. _aws-kms:

AWs Key Management Service
==============================================================================

简单来说, KMS 提供的是全托管 非对称加密 服务 (通常是 RSA 加密算法). 让你用简单的几行代码, 就能在你的 App 中使用非对称加密, 从而安全地读取敏感信息. 由于是 RSA, 一次性加密的数据不能太大. 如果你要加密大量数据, 通常是使用对称加密对数据进行加密, 而仅仅是用 RSA 来对 对称加密 算法中的密钥进行加密即可.

KMS 托管的是你的 RSA 密钥. **KMS 并不托管你的想要加密的敏感信息, 比如数据库连接信息, 数据库密码**.


How to Use
------------------------------------------------------------------------------

KMS 通常要结合 :ref:`Secret Manager <aws-secret-manager>` 使用. Secret Manager 使用你在 KMS 中托管的 Key, 对你的敏感信息进行加密, 并储存在 Secret Manager 中.

虽然你可以直接用下面的方式, 用 KMS 加密, 解密信息. 但是并不推荐手动这么做.

.. code-block:: python

    import boto3
    import base64

    client = boto3.client("kms")

    secret = "..."

    encrypted_text = base64.b64encode(client.encrypt(
        KeyId="...",
        Plaintext=base64.b64encode(secret.encode("utf-8")),
    )["CiphertextBlob"])

    decrypted_text = client.decrypt(
        CiphertextBlob=base64.b64decode(encrypted_text.encode("utf-8"))
    )["Plaintext"].decode("utf-8")

    assert secret == decrypted_text # True

Reference:

- encrypt: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.encrypt
- decrypt: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.decrypt

正确做法是结合 Secret Manager 一起使用. 具体做法请参考


What Type of Key should Use?
------------------------------------------------------------------------------
很多 KMS 的用户第一次看到 Console 里的 ``AWS managed keys``, ``Customer managed keys``, ``Custom key stores`` 都会感到困惑.

简单来说:

1. Customer managed CMK, 自己创建, 自己管理 (保管在自己账户下), 自己使用.
2. AWS managed CMK, AWS 自动随着服务一起创建的, 归属于你的账户, 但是自己无法删除和管理, 跟随服务一起被删除, 存储在 AWS 自己的密码服务器上, 在自己的账户下使用.
3. AWS owned CMK, AWS 在亚马逊自己的账户下创建的, 供第三方使用, 自己无法删除和管理, 有很多用户共同使用. 这种 Key 对用户通常不可见.

.. list-table:: Title of the table
    :widths: 10 10 10 10
    :header-rows: 1

    * - Type of CMK
      - Can view
      - Can manage
      - Used only for my AWS account
    * - Customer managed CMK
      - Yes
      - Yes
      - Yes
    * - AWS managed CMK
      - Yes
      - No
      - Yes
    * - AWS owned CMK
      - No
      - No
      - No

结论, 自己的 App 就用 Customer managed keys.

Reference: https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys
