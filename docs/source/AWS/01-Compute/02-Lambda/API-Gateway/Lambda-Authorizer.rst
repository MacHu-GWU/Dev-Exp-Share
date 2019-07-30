API Gateway Lambda Authorizer
==============================================================================

.. contents::
    :local:

Reference:

- The Complete Guide to Custom Authorizers with AWS Lambda and API Gateway: https://www.alexdebrie.com/posts/lambda-custom-authorizers/
- Use API Gateway Lambda Authorizers: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html


Lambda Authorizer
------------------------------------------------------------------------------


Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

简单来说, 该方法是在你每次发送 API Http Request 的时候, 在 Header 中附带一个 Token 信息, 然后有一个专用的 Lambda Function 会接受到这个 Token, 以及被请求的资源的信息. 然后你使用自定义的逻辑处理这个 Token, 返回一个 JSON Policy Document, 里面定义了能对哪些资源进行访问, 哪些资源不允许访问. 然后 AWS 会根据这个 Policy Document 来检查你要访问的资源是否允许你访问.

由于是使用 Lambda Function, 你基本上可以使用任意的自定义验证逻辑. 比如跟 DynamoDB 中的 Token 进行比较.

在 Serverless 应用中, 一个比较常见的方法是, 当用于成功登陆时, 根据用户的 ID, 在 DynamoDB 中生成一条数据, 包括 ID 和 Token, 并设置 TTL, 比如 15 分钟后过期. 然后在每次的请求中带上这个 Token, 并在 API Gateway 设置 Authentication Cache, 比如 5 分钟. 然后再验证的 Lambda Function 中实现每次验证刷新 Token. 这样就可以实现无状态登陆了.

1. **创建 Authorizer**:

在 API Console 界面, 选择你的 API, 选择 Authorizer, 选择 Create New Authorizer, Name 填写 ``MyAuthorizer`` (注意 ``my-authorizer`` 不行, 必须使用驼峰命名法), Type 选择 Lambda, 然后选择你的 Function Name (可以提前创建一个空的 Lambda 函数, 代码等下再补全). Lambda Invoke Role 不填, 让它自动决定, Lambda Event Payload 选择 Token, Token Source 填写 ``auth``, 这将会是你用于验证的 Http Headers 的 key name. Token Validation 可以不填, 它是用来使用 Regex 验证用的, 可以提前免费帮你筛选掉不合法的 Token, 省下 Authorizer Lambda Function 的运行. Authorization Caching 勾上, TTL 设置为 300 秒.

2. **在 Lambda Function 中自定义验证逻辑**:

在 Lambda Function 中的 Event 对象是这个样子的, 其中 ``authorizationToken`` 是你在 ``auth`` header 的值. 而 ``methodArn`` 则是你的 endpoint 所对应的 API Method 的 Arn.

.. code-block:: python

    {
        "type": "TOKEN",
        "authorizationToken": "allow",
        "methodArn": "arn:aws:execute-api:us-west-2:123456789012:abcdef/*/GET/"
    }

Lambda Function 逻辑中, 推荐使用 DynamoDB 作为数据库用来通过 Token 反查请求者 email 或 user_id, 以及维护 token.

经过处理后, 你的函数需要返回形如这样的 JSON 对象. 其中 ``principalId`` 是从 Token 反查获得的请求者的 ID, 用于追踪是谁调用了此 API, 通常是用户名或邮箱. ``PolicyDocument`` 则是定义了访问权限的说明. 你可以使用通配符 ``*`` 统一匹配多个 Resource 的多个 Method. ``context`` 则可以用于储存任意自定义数据.

.. code-block:: python

    {
        "principalId": "my-username",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": "arn:aws:execute-api:us-east-1:123456789012:abcdef/test/GET/my-resource"
                }
            ]
        },
        "context": {
            "org": "my-org",
            "role": "admin",
            "createdAt": "2019-01-01T12:00:00"
        }
    }

AWS Lambda 创建函数的界面有一个 blue print, 里面的代码很值得一读, 可以动态创建 PolicyDocument.

值得一提的是, 在这篇文档中 (最下面) https://docs.aws.amazon.com/apigateway/latest/developerguide/configure-api-gateway-lambda-authorization-with-console.html 说了, 你可以将 Authorizer 的输入和输出信息在验证成功后转发到 API Method 真正的 Lambda Function 的 event 中. 有些业务场景中会有用.

在设置好之后, 你就可以在 Authorizer 界面使用 Test 进行测试了.

3. **将 Authorizer 应用到 API Method**

在 Resource 中选定你的 Method, 然后选择 Method Request, 在 Authorization 中选择你刚才用 驼峰命名法 命名的 Authorizer, 确定即可. 最后将整个 API Deploy 即可.

以上的所有过程都可以使用 Cloudformation 进行自动化.

参考资料:

- Use API Gateway Lambda Authorizers: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html


REQUEST
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REQUEST 本质上跟 TOKEN 一致, 都是通过 Header 传入信息, 由 Lambda Function 进行处理, 返回 PolicyDocument, 不过输入信息更丰富. 而且你需要手动指定 Cache Key, 也就是在 Header 中选择一个或多个 Key 作为 Cache 的 Key.

