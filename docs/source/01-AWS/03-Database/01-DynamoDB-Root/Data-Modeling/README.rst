.. _dynamodb-data-modeling:

DynamoDB Data Modeling
==============================================================================

本文档记录了我学习用 DynamoDB 建立数据模型的学习心得. 主要分两个部分:

1. Principal 包括各种经典数据模型, one-to-many, many-to-many, 以及各种 查询模式 的数据模型.
2. system 包括各种互联网产品的后台设计. 比如设计抖音的数据后台.


参考资料:

- DynamoDB 关系建模: https://blog.csdn.net/m0_37263637/article/details/89668891



.. _dynamodb-e-commerce-data-modeling-example:

E-Commerce Data Modeling Example
------------------------------------------------------------------------------

使用场景:

- user_id
- user_major_email
- order_id
- item_id

- 一个 user 只能有一个 major email, 所以 user vs email = 一对一.
- 一个 user 可能有多个 order, 但是一个 order 只有一个 user. 所以 user vs order = 一对多.
- 一个 order 可能有多个 item, 一个 item 也可能被多个 order 所包含. 所以 order vs item = 多对多.


``table_users``::

    user_id (partition_key)     email
    2d4b83                      alice@example.com
    f97c69                      bob@example.com

``index_users_email_to_user``, partition key of GSI can be duplicate::

    email (partition_key)       user_id
    alice@example.com           2d4b83
    bob@example.com             f97c69

``table_users``::







