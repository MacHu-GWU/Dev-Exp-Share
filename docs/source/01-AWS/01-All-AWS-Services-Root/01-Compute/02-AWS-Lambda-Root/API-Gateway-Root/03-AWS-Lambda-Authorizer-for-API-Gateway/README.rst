API Gateway Lambda Authorizer
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Reference:

- The Complete Guide to Custom Authorizers with AWS Lambda and API Gateway: https://www.alexdebrie.com/posts/lambda-custom-authorizers/
- Use API Gateway Lambda Authorizers: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html


What is AWS Lambda Authorizer
------------------------------------------------------------------------------
API Gateway 支持三种鉴权方式:

1. AWS Cognito
2. SAML (Third Party Single Sign On)
3. Custom Authorizer

AWS Lambda Authorizer 就是 Custom Authorizer 的实现.

简单来说根据 `这篇文档 <https://docs.aws.amazon.com/apigateway/latest/developerguide/call-api-with-api-gateway-lambda-authorization.html>`_  Client 在发送 Request 的时候需要附带一个 HTTP Headers ``{"Authorization": "${TOKEN}"}``. 然后根据 `这篇文档 <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-input.html>`_ AWS Lambda Authorizer 收到的 event 是这样子的:

.. code-block:: javascript

    {
      "type": "TOKEN",
      "authorizationToken": "{caller-supplied-token}", # 就是 header 里的 TOKEN
      "methodArn": "arn:aws:execute-api:{regionId}:{accountId}:{apiId}/{stage}/{httpVerb}/[{resource}/[{child-resources}]]"
    }

根据 `这篇文档 <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html>`_ 这个 AWS Lambda 需要返回一个长这样的 Policy Document, 其中 Action, Effect, Resource 定义了这次 Authentication 的结果, 能否访问? 能访问什么权限? 能使用什么 HTTP Method?:

.. code-block:: javascript

    {
      "principalId": "yyyyyyyy", // The principal user identification associated with the token sent by the client.
      "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Action": "execute-api:Invoke",
            "Effect": "Allow|Deny",
            "Resource": "arn:aws:execute-api:{regionId}:{accountId}:{apiId}/{stage}/{httpVerb}/[{resource}/[{child-resources}]]"
          }
        ]
      },
      "context": {
        "stringKey": "value",
        "numberKey": "1",
        "booleanKey": "true"
      },
      "usageIdentifierKey": "{api-key}"
    }

请注意这里的 ``context``, 你可以把 Authorization 的结果信息放入 context, 然后这个 context 会被一同 pass 给实际调用的 backend service. 这个机制可以用作鉴权缓存. 相当于提供 Service 的 backend 本身也做了一些鉴权的判断逻辑.

值得一提的是, 根据 `这篇文档 <https://aws.amazon.com/blogs/security/use-aws-lambda-authorizers-with-a-third-party-identity-provider-to-secure-amazon-api-gateway-rest-apis/>`_, Authorizer 是支持缓存的, 也就是一定时间内你对 API 发起的请求不需要再经过 Authorizer 的 Lambda Function 了, 这样可以提高响应速度.



一个具体的例子
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


使用 Lambda Authorizer 时的 API 鉴权的流程
------------------------------------------------------------------------------
我们以 GitHub 网站为例:

1. 用户输入账号密码登录, 这个登录服务器本身也是一个对公网开放的 API, 这个 API 是无需权限的, 但是有限流限速等机制以防暴力破戒. 一旦登录成功, 服务器端就会生成一个有效期 24 小时的 token, 并将 token 存在 Dynamodb 中 (Redis 也可以, 类似, 我们就按 Dynamodb 算吧) 并设置 TTL. 然后浏览器会收到这个 token.
2. 用户进入 GitHub 点击各个网页元素或者菜单, 有些按钮是不是 public 的, 比如列出你的所有 Private Repo. 那么这些网页元素本身背后就是一个需要 Authentication 的 API. 你第一次点击的时候浏览器就会自动带上这个 token.
3. 后端的 Lambda Authorizer 的实现逻辑可能仅仅是检查这个 Key 在 Dynamodb 中是否存在, 如果存在则 Allow.
4. 于是 Github 网站成功返回一些需要登录才能获得的资源.
5. 当你再次刷新这个页面时, 如果是 Get, 可能不仅仅 Authorization 被缓存, 而实际返回的数据 API Gateway 都直接缓存了, 所以 Lambda Authorizer 以及 Backend Service 都没有被 Invoke.
6. 如果是 Post, 比如你要 commit, 那么 API Gateway 则会在短时间内, 比如 60 秒内不经过 Authorizer, 而是直接在 Authorization 缓存里找到你已经登录的记录, 直接 commit. 如果超过 60 秒, 就再 call 一次 Lambda Authorizer 即可.
