.. _aws-redshift-user-management:

AWS Redshift User Management
==============================================================================
Redshift 的应用层是基于 Postgres 修改而来, 也有着丰富的 User / User Group 的权限管理功能.

Redshift 的权限管理模型和 IAM 很类似, 都分为 Principal, Resource, Action. 简单来说就是 谁, 能对什么东西, 做什么. 而 `User <https://docs.aws.amazon.com/redshift/latest/dg/r_Users.html>`_ 则是一个具体的账号密码 (如果用 IAM Role 权限管理则不需要密码). `Group <https://docs.aws.amazon.com/redshift/latest/dg/r_Groups.html>`_ 则是一个包含多个 User 的集合, group 本身可以被授予权限, 所有被加入到 group 中的用户都会自动获得 group 所有的权限. 这个和 IAM User Group 是类似的. 也是推荐的管理方式.

.. note::

    AWS 推荐的用户管理方式:

    1. 所有的 User 被创建后不要直接用 ``GRANT`` 给任何权限.
    2. 创建几个 User Group, 给 User Group 一些权限. 例如 Power User, Developer, Analyst, Business
    3. 用把 User 放入到 Group 中的形式给 User 权限.

这里有一些示例代码.

.. literalinclude:: ./example.py
   :language: python
   :linenos:

**Important Concept**:

- `User <https://docs.aws.amazon.com/redshift/latest/dg/r_Users.html>`_: Single User
- `Group <https://docs.aws.amazon.com/redshift/latest/dg/r_Groups.html>`_: Group of Users
- `Schema <https://docs.aws.amazon.com/redshift/latest/dg/r_Schemas_and_tables.html>`_: Group of Tables

**Important Command**:

- `CREATE USER <https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html>`_ command: Create or Disable user (``CREATE USER username WITH PASSWORD DISABLE``)
- Privileges: list of operation allowed to operate
- `GRANT <https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html>`_ command: Grant specific user one or set of privilege
- `REVOKE <https://docs.aws.amazon.com/redshift/latest/dg/r_REVOKE.html>`_ command: inverse of GRANT
