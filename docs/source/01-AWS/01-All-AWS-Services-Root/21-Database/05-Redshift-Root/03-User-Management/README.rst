.. _aws-redshift-user-management:

AWS Redshift User Management
==============================================================================
Keywords: AWS Redshift User Management, Group, Grant, Revoke, Permission.


Overview
------------------------------------------------------------------------------
Redshift 的应用层是基于 Postgres 修改而来, 也有着丰富的 User / User Group 的权限管理功能.

Redshift 的权限管理模型和 IAM 很类似, 都分为 Principal, Resource, Action. 简单来说就是 谁, 能对什么东西, 做什么. 而 `User <https://docs.aws.amazon.com/redshift/latest/dg/r_Users.html>`_ 则是一个具体的账号密码 (如果用 IAM Role 权限管理则不需要密码). `Group <https://docs.aws.amazon.com/redshift/latest/dg/r_Groups.html>`_ 则是一个包含多个 User 的集合, group 本身可以被授予权限, 所有被加入到 group 中的用户都会自动获得 group 所有的权限. 这个和 IAM User Group 是类似的. 也是推荐的管理方式.

.. note::

    AWS 推荐的用户管理方式:

    1. 所有的 User 被创建后不要直接用 ``GRANT`` 给任何权限.
    2. 创建几个 User Group, 给 User Group 一些权限. 例如 Power User, Developer, Analyst, Business
    3. 用把 User 放入到 Group 中的形式给 User 权限.


User Management 有什么用?
------------------------------------------------------------------------------
- 当你的用户


Important Concepts
------------------------------------------------------------------------------
- `User <https://docs.aws.amazon.com/redshift/latest/dg/r_Users.html>`_: Single User
- `Group <https://docs.aws.amazon.com/redshift/latest/dg/r_Groups.html>`_: Group of Users
- `Schema <https://docs.aws.amazon.com/redshift/latest/dg/r_Schemas_and_tables.html>`_: Group of Tables
- Privileges: list of operation allowed to operate, such as SELECT, INSERT, UPDATE, DELETE

**Important SQL Commands**:

- `CREATE USER <https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html>`_: Create or Disable user (``CREATE USER username WITH PASSWORD DISABLE``)
- `CREATE GROUP <https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_GROUP.html>`_:
- `ALTER USER <https://docs.aws.amazon.com/redshift/latest/dg/r_ALTER_USER.html>`_: update password, session timeout, etc.
- `ALTER GROUP <https://docs.aws.amazon.com/redshift/latest/dg/r_ALTER_GROUP.html>`_: add user, drop user, rename group
- `DROP USER <https://docs.aws.amazon.com/redshift/latest/dg/r_DROP_USER.html>`_: delete user
- `DROP GROUP <https://docs.aws.amazon.com/redshift/latest/dg/r_DROP_GROUP.html>`_: delete group
- `GRANT <https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html>`_ command: Grant specific user one or set of privilege
- `REVOKE <https://docs.aws.amazon.com/redshift/latest/dg/r_REVOKE.html>`_ command: inverse of GRANT


Redshift 中的 User 和 IAM Role 如何配合使用
------------------------------------------------------------------------------
如果你启用了 IAM Access. 那么你可以用 IAM User / Role 来调用 ``boto3.redshift_client.get_credentials`` 来获取一个用户名和密码. 这个用户名一般是 ``IamUser:your_name`` 或是 ``IamRole:role_name`` 的格式. 实际上 Redshift 会临时创建/更新一个 User, 并且设定一个 session timeout 的时间. 所以本质上如果你要用数据库内的 User / Group Access management 的功能对 IAM User / Role, 只需要对 IAM User 和 Role 相对应的 User 进行管理即可.