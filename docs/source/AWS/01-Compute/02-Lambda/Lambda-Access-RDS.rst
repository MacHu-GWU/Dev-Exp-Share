Lambda Access RDS
==============================================================================

**如何配置 RDS 以及 RDS 所在的 VPC 网络, 请参考** :ref:`configure-network-for-rds` 一文.

**需要的 IAM Role Policy**:

1. Lambda 并不需要 ``AmazonRDSxxxAccess`` 这一类的 Policy, 这一类的 Policy 是为 RDS 的 API 提供权限的, 比如创建数据库, 备份, 删除数据库. Lambda 实际上是用 SQL Client 与数据库通信.
2. IAM Role 中必须要包含 ``AWSLambdaVPCAccessExecutionRole`` 这一 Policy. 这一 Policy 已包含了 ``AWSLambdaBasicExecutionRole``, 并提供了访问 VPC 网络的权限. 之所以使用这一权限是因为, 大部分的 RDS 和 Redshift 都是部署在 VPC 内的 Private Subnet 下的. **而创建 Lambda 时本身就设定了 VPC, Subnet, Security Group. 所以 Lambda 本身已经就是在 Private Subnet 下了, 只要 Security Group 开启了数据库相应的 TCP/IP 端口, 那么 Lambda 就可以与 RDS 用 SQL Client 通信了. 而 VPC 通常为 Private Subnet 配置了 NAT Gateway 用于和外网通信, 所以 Lambda 也依然可以访问外网**

**Lambda Code**:

`sqlalchemy_mate <https://github.com/MacHu-GWU/sqlalchemy_mate-project>`_ 是一个 Python 库, 能用最少的代码连接数据库.

.. code-block:: python

    def lambda_handler(event, context):
        from sqlalchemy_mate import EngineCreator

        # connect to postgres RDS
        engine = EngineCreator(
            host="xxx",
            port="xxx",
            database="xxx",
            username="xxx",
            password="xxx",
        ).create_postgresql_psycopg2()

        # execute some random sql
        stmt = sa.text("SELECT 999;")
        result = engine.execute(stmt).fetchone()[0]
        return {
            'statusCode': 200,
            'result': result
        }
