API Gateway Lambda Integration Guide
==============================================================================

.. contents::
    :depth: 1
    :local:

在 Serverless 应用中, 我们常常会使用 API Gateway 来间接调用 Lambda 函数. 这样做的好处是工程师只专注于数据接口, 而调用 Lambda 的语言和 Lambda 实现所用的语言完全相互独立. 是一种很典型的解耦合的设计. 当然直接在 App 里面使用 AWS SDK 调用 invoke function 也是可以的. 不过就无法利用 API Gateway 自带的安全, 统计等功能了.


**本文主要讨论各种常用的 API Gateway 和 Lambda 相结合使用的方式**


几种常用的 Integration 风格
------------------------------------------------------------------------------

.. contents::
    :local:


Rest API 风格
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**使用 HTTP 作为接口, 实现的基于 Resource 的 Rest 风格的 API**.

**在 Application 中, Rest API 主要用于获取数据**.

以 GitHub API 为例. User 是一种资源.

- ``GET api.github.com/v1/users`` 是获得所有用户的列表, ``GET api.github.com/v1/users?page=3`` 由于 Get All 往往返回大量数据, 所以用 parameters 来指定分页是一个不错的选择.
- ``GET api.github.com/v1/users/1`` 是获得 user_id 为 1 的用户的数据.
- ``POST api.github.com/v1/users {user_id: 1, email: alice@email.com}`` 是创建一个新的 User.
- ``PUT api.github.com/v1/users {user_id:1, email: bob@email.com}`` 是修改 User 的数据.
- ``DELETE api.github.com/v1/users/1`` 是删除 user_id 为 1 的用户的数据.

响应数据协议使用 ``application/json``


Function 风格
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Lambda 本质上是一个函数, 函数就是一个无状态的输入和输出. 所以在 API 上就是一个 HTTP POST, 而用 Payload 来传递参数**.

**在 Application 中, Function API 主要用于调用某些功能, 当然也可以用于获取数据**.

- ``POST api.github.com/v1/func/get-last-n-days-new-users {n_days: 7}``

响应数据协议使用 ``application/json``


HTML 风格
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**在 Serverless Web App 的架构下, 前端的 HTML 都是使用 Lambda 对请求数据进行处理, 然后从 S3 获取 HTML Template, 然后使用 Template Language 进行 Render, 最后返回 HTML 给客户端**. 而在不离开页面的情况下的互动, 则通过 Ajax 获取额外的数据, 动态加载数据到前端.

此时我们同样是将 GET URL, POST URL 通通转化为 POST URL + Payload 传递给 Lambda, 然后返回数据. 和 Function 风格不同之处在于, Function 中只会对 URL 使用 POST 方法, 而 HTML 风格中可能需要对 URL 使用 GET 方法, 此时则需要将 GET 风格中的参数转化为 Payload, 然后调用 Lambda.

响应数据协议使用 ``text/html``


Binary 风格
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

主要用于实现 图片, 文件 服务器.





API Gateway 中的设置
------------------------------------------------------------------------------

.. contents::
    :local:


Rest API 风格的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

我们实现 ``GET api.example.com/v1/rest/user?page=3&sort_by=create_time``, **返回所有用户列表, 假设每页允许返回 10 条数据, 则列出第 3 页, 按照 create_time 排序假设**.

请参考 `<HTML风格设置_>`_, 跳过 Method Response 和 Integration Response 中的内容即可.


我们实现 ``GET api.example.com/v1/rest/user/<user_id>``, **假设 user_id = 3, 那么则通过** ``GET api.example.com/v1/rest/user/3`` **返回 user_id = 3 的用户的数据**.

Method Request:

- Request Paths: Name = ``user_id``

Integration Request:

- Integration type = Lambda Function
- Use Lambda Proxy integration 不选择
- URL Path Parameters: 无需设置
- URL Query String Parameters: 无需设置
- HTTP Headers: 无需设置
- Mapping Templates: 将 HTTP GET 的 URL 和参数转化为 Lambda 的 event
    - Content-Type: ``application/json``
    - Mapping Template: ``{"user_id": "$input.params('user_id')"}``

Method Response:

- 全部无需设置

Integration Response:

- 全部无需设置, 响应数据协议默认使用 ``application/json``

**而对于 Post, Put. 由于本质上和 Function 风格一致, 所以请参考** `<Function风格的设置_>`_ 即可.

**而对于 Delete, 取决于你想用 GET 实现还是 POST 实现**.


.. _Function风格的设置:

Function 风格的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

例如我们的 Function 里有一个这样的函数:

.. code-block:: python

    def sum_all(number_list):
        return sum(number_list)

    def lambda_handler(event, context):
        return sum_all(event["number_list"])

那么在 API Gateway 中, 我们则是实现 ``POST api.example.com/v1/func/sum-all {"number_list": [1, 2, 3]}``.

Method Request:

- URL Query String Parameters: 无需设置
- HTTP Request Headers: 无需设置
- Request Body: 无需设置
- SDK Settings: 无需设置

Integration Request:

- Integration type = Lambda Function
- Use Lambda Proxy integration 不选择
- 其他全部无需设置, 默认情况下 API Gateway 自动将 Payload 中的 Json 转化为 data 传递给 Python Handler 中的 event 变量.

Method Response:

- 全部无需设置

Integration Response:

- 全部无需设置, 响应数据协议默认使用 ``application/json``


.. _HTML风格设置:

HTML 的设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

例如, 实现 ``GET api.github.com/v1/<USERNAME>/repositories?page=1`` 返回一个 HTML 页面, 列出了用户的前 10 个 repo (每页 10 个)

Method Request:

- URL Query String Parameters 中设置 Name = page, Required = 不需要, 在 Lambda 函数中对其进行处理, 如果没有则默认设为 1.
- HTTP Request Headers: 无需设置

Integration Request:

- Integration type = Lambda Function
- Use Lambda Proxy integration 不选择
- URL Path Parameters: 无需设置
- URL Query String Parameters: 无需设置
- HTTP Headers: 无需设置
- Mapping Templates: 将 HTTP GET 的 URL 和参数转化为 Lambda 的 event
    - Content-Type: ``application/json``
    - Mapping Template: ``{"page": "$input.params('page')"}``, 如果 page 参数不存在, 则会返回一个空字符串. ``{"page": ""}``, 所以 Lambda 中需要对其进行异常处理.

Method Response:

- Response Headers for 200: 加上这么两条 ``Access-Control-Allow-Origin``, ``Content-Type``

Integration Response:

- Header Mappings:
    - ``Access-Control-Allow-Origin`` = ``'*'`` 注意单引号. 由于 API Gateway 后端是 Lambda, 这是一个跨域 (CORS) 请求, 所以告诉客户端的浏览器, 来源是合法的. 为什么这么做的原理请看 http://www.ruanyifeng.com/blog/2016/04/cors.html.
    - ``Content-Type`` = ``'text/html'`` 注意单引号. 告诉客户端浏览器, 返回的数据请当做 text/html 来处理
- Mapping Templates:
    - Content-Type: ``text/html``
    - Mapping Template: ``$input.path('$')``. 对返回的 HTML 进行一些处理, 在这里我们使用 $ 表示原封不动的返回.


参考资料
------------------------------------------------------------------------------

Mapping Template Reference: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html

