
Connect to DynamoDB
------------------------------------------------------------------------------

- DynamoDB 不像 Relational Database 那样, 使用 Host, Port, Database, Username, Password 连接到数据库,
- DynamoDB 是 Stateless 的, 不存在连接的概念, 完全使用 Https Request.
- DynamoDB 使用 IAM Role, 然后创建 DynamoDB Boto3 Client 用于 API Call.
    - 如果你想从本地机器上连接 DynamoDB: AWS User Profile
    - 从 EC2 上: IAM role, ``boto3.client("dynamodb")``
    - 从 Lambda 上: IAM role, ``boto3.client("dynamodb")``


DynamoDB CRUD
------------------------------------------------------------------------------

- DynamoDB 使用 boto3 client 通过 API 进行 CRUD
- API



DynamoDB 有三种查询模式:

1. get item: 直接定位到某一条记录, 只支持 primary key 列的查询.
2. query: 利用 primary key 和 secondary index 列的查询.
3. scan: 对全表进行扫描, 支持任意列的条件判断. 性能差, 官方不推荐.

请特别注意, 设计表时, 列名称不要和 Reserved Keyword 冲突, 这里是所有 DynamoDB 保留关键字的列表: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html


Reference:

- 谈谈Amazon DynamoDB的增删改查（CRUD）操作: https://zhuanlan.zhihu.com/p/40828013
- 深度解析 DynamoDB: https://www.infoq.cn/article/aws-dynamodb-dive-in
- Learn DynamoDB: https://www.dynamodbguide.com

经典数据库中

- given email, find user_id
- given user_id, find all order_id he have placed
- given order_id, find detail and total price

users
    user_id
    email
    password

items
    item_id
    name
    price

orders
    order_id
    user_id

order_and_item
    order_id
    item_id
    quantity


DynamoDB中

users
    user_id, primary_key partition_key
    email, primary_key sort_key
    password

session_id = user_id



简单的微信消息应用

message
    sender_id, primary key, partition key
    time, primary key, sort key
    message_id
    receiver_id
    type
    body

用户登录微信, 点开和某个朋友的对话框. 此时获得 query(sender_id=<user_id>, )





积分榜应用
------------------------------------------------------------------------------



重要概念
-------
