What is Dynamodb
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Reference:

- 谈谈Amazon DynamoDB的增删改查（CRUD）操作: https://zhuanlan.zhihu.com/p/40828013
- 深度解析 DynamoDB: https://www.infoq.cn/article/aws-dynamodb-dive-in
- Learn DynamoDB: https://www.dynamodbguide.com


Key Value NoSQL database
------------------------------------------------------------------------------

- Key Value: Dynamodb 是一个 Key Value 数据库. 这并不是说 Dynamodb 不能批量读写, 只是说按照 Key 来读写是最有效率的方式.
- NoSQL: 在 Dynamodb 中没有 Schema 的概念. 只有 Hash key 和 Range key 是必须要有的以及需要预先定义, 其他的 field 都不需要定义就可以使用.
- Data Model: 由于是 NoSQL, 为你的 Application 进行数据建模的方式跟传统的 RDBMS 有很大的不同. 这里先不展开讲.

Table "Tweets"::

    {
        hash_key_id: "t-001",
        range_key: "details",
        create_time: "2021-01-07 08:54:59",
        author_id: "u-001",
        content: "Hello World",
    },
    {
        hash_key_id: "t-001",
        range_key: "thread_000_000_001",
        create_time: "2021-01-07 09:02:41",
        author_id: "u-002",
        content: "Welcome to the world",
    },
    {
        hash_key_id: "t-001",
        range_key: "thread_000_000_002",
        create_time: "2021-01-07 09:02:59",
        author_id: "u-003",
        content: "what is this?",
    },


Dynamodb API (Connect to Dynamodb)
------------------------------------------------------------------------------

传统的关系数据库通常都是通过 http 协议, 数据用 TSL 加密, 通过一个像 URL 的 Endpoint, 用 host, port, database, username, password 来连接到数据库. 这个连接会长期存在直到数据库杀死它, 或是客户端主动选择关闭. 而为了提高性能, 数据库和客户端都会在内存中维护一个连接池, 以便复用, 减少创建连接的开销.

而 Dynamodb 作为云原生服务, 不存在数据库连接的概念. 整个 API 都是 Stateless 的. 完全是通过 Https Request 与 Dynamodb 进行通信. 这个 HTTPS 的 API 也就是俗称的 Low Level API, 详细的语法文档可以参考这里 https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html.

而 AWS SDK 提供了封装更好的 API. 在 Python 中你可以用 boto3 来对 Dynamodb 进行 读/写/更新/删除 等操作. 主要使用 JSON 作为数据传递的接口.

在 Python 社区还有个封装的更好的 API, 由开源 Python 库 `Pynamodb <https://pynamodb.readthedocs.io/en/latest/>`_ 提供. 这个库相当于 SQL 世界中的 ORM, 允许用 Class 来定义数据模型, 使得代码量更少, 人类更好理解.

**关于鉴权**, Dynamodb 没有 Username Password 的概念, 完全适用 IAM Role 来验证你是否有权限. 由于使用了 IAM Role, 你可以对客户端可进行的操作做更精细的控制.


Dynamodb Write
------------------------------------------------------------------------------

在 Dynamodb 中的 Write 包括: Create, Update, Delete. 只要是对数据发生了变更, 就是 Write 操作.

这三种操作都有 单个 Item 和 Batch 两种模式. 单个 Item 的模式很好理解, 这里重点说一下 Batch 模式.

Batch 的本质是将多个 Action Push 到一个 Buffer 中, 然后以 25 个 Action 为一批批量执行. (25 是 Batch 的上限) 要注意的是 **一个 Batch 中的多个 Actions 的执行顺序是无法保证的, 完全可能生效的顺序和你请求的顺序不一致. 如果你要严格保证一致, 请使用 Transaction**


Dynamodb Read
------------------------------------------------------------------------------

DynamoDB 有三种查询模式:

1. get item: 直接定位到某一条记录, 只支持 hash key 列的查询.
2. query: 利用 hash key, range key, 或是用 secondary index 索引进行查询. **这是 Dynamodb 推荐的查询方式, 比较有效率, 可以利用索引, 避免全表扫描**.
3. scan: 对全表进行扫描, 支持任意列的条件判断. 性能差, 如果非必要不推荐.


Dynamodb Data Modeling
------------------------------------------------------------------------------

请特别注意, 设计表时, 列名称不要和 Reserved Keyword 冲突, 这里是所有 DynamoDB 保留关键字的列表: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html


Dynamodb Ops
------------------------------------------------------------------------------

Dynamodb 是云原生数据库. 创建一个表只需要 3-5 秒. 备份和恢复也都是秒级的.


Dynamodb Pricing
------------------------------------------------------------------------------

Dynamodb 的收费有 On-Demand (Pay as you go) 和 Provisioned 两种模式.
