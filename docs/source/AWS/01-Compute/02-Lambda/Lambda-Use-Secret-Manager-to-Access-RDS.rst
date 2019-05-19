Lambda Use Secret Manager to Access RDS
==============================================================================

**需要的 IAM Role Policy**:

1. Lambda 并不需要 ``AWSKeyManagementServicePowerUser``, 即使 SecretManager 本身需要使用 KMS. **正确的做法是在 Secret 所使用的 KMS Key 的控制台中, 将 Lambda 所使用的 IAM Role, 添加到 Key users 中**.
2. 为了访问 SecretManager 中的数据, **我们需要 SecretManager 的 Read 权限. 但是 AWS Managed 自带的 Policy 中的 SecretsManagerReadWrite 中有对 SecretManager 的写权限. 我们并不希望 Lambda 有这个写权限. 所以我们需要自己创建一个 Policy**. 点击 Create Policy, 选择 Service 为 Secrets Manager, 选择 Actions 为 Read, 选择 Resources 为 All Resoures, 不对 Request Conditions 进行设置.

**Lambda Code**:

`pysecret <https://github.com/MacHu-GWU/pysecret-project>`_ 是一个 Python 库, 可以用最少的代码从 AWS Secret Manager 中读取数据.

.. code-block:: python

    from pysecret import AWSSecret

    secret_id = "db_credential"
    aws = AWSSecret() # AWS IAM role implied
    password = aws.get_secret_value(secret_id=secret_id, key="password")
    ...


**Lambda Code Example from AWS**:

.. code-block:: python

    # Use this code snippet in your app.
    # If you need more information about configurations or implementing the sample code, visit the AWS docs:
    # https://aws.amazon.com/developers/getting-started/python/

    import boto3
    import base64
    from botocore.exceptions import ClientError


    def get_secret():

        secret_name = "db_credential"
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        # Your code goes here.

