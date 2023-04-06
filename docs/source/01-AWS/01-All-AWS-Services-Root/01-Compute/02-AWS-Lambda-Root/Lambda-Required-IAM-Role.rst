各种情况下 Lambda 所需要的 IAM Role
==============================================================================


纯 Python 代码计算
------------------------------------------------------------------------------

如果 Lambda 仅仅是调用本地的 Python 代码进行运算, 不访问任何外部的网络服务, 则需要 `AWSLambdaBasicExecutionRole$jsonEditor <https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole$jsonEditor>`_ 这个 Policy 即可.


S3
------------------------------------------------------------------------------

如果 Lambda 仅仅是对 S3 进行 Get Object, Head Object, Put Object, 就需要 `AWSLambdaExecute <https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AWSLambdaExecute$jsonEditor>`_ 这个 Policy. **该 Policy 无法执行 list_objects 操作**.

测试代码:

.. code-block:: python

    """
    Reference:

    - put_object: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    - get_object: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    - head_object: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    - list_objects: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects

    Bucket Dashboard: https://s3.console.aws.amazon.com/s3/buckets/eqtest-sanhe
    """

    import boto3
    from pprint import pprint

    bucket_name = "eqtest-sanhe"
    s3 = boto3.client("s3")

    def put_object():
        response = s3.put_object(
            Bucket=bucket_name,
            Key="hello.txt",
            Body="hello world!".encode("utf-8"),
            Metadata={
                "creator": "Sanhe Hu",
            }
        )
        pprint(response)


    def get_object():
        response = s3.get_object(
            Bucket=bucket_name,
            Key="hello.txt",
        )
        pprint(response)


    def head_object():
        response = s3.head_object(
            Bucket=bucket_name,
            Key="hello.txt",
        )
        pprint(response)


    def list_objects():
        response = s3.list_objects(Bucket=bucket_name)
        pprint(response)


    def lambda_handler(event, context):
        put_object()
        get_object()
        head_object()
        # list_objects() # this operation should not work



VPC
------------------------------------------------------------------------------

许多时候 Lambda 需要与 EC2, RDS, DynamoDB 进行通信, 而数据库服务器通常被放在 VPC 的 Private Subnet 中.

只要 Lambda 被放置于 VPC 中的 Private Subnet 中 (Lambda 要么被放在 VPC 的 Private Subnet 中, 要么不放在 VPC 中), 就需要 `AWSLambdaVPCAccessExecutionRole <https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole$jsonEditor>`_ 这个 Policy 来通过 VPC 访问私网内的服务, 以及通过 NAT Gateway 访问公网.


Secret Manager
------------------------------------------------------------------------------

