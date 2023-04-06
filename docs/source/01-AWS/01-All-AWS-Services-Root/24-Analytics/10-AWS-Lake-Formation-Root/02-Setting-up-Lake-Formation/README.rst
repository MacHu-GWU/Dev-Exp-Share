.. _aws-setting-up-lake-formation:

Setting up Lake Formation
==============================================================================
Keywords: AWS, Lake Formation, LakeFormation, LF

以下用 LF 简写代表 Lake Formation.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 一些前置知识
------------------------------------------------------------------------------
LF 是一个 regional 的服务, 不同的 region 下的 LF 互相独立, **LF 不能跨 region 管理其他 region 上的资源**, 你可以选择在一个 region 上启用 LF, 另一个 region 上不启用. 默认情况下 LF 是没有启用的.

另外, 在启用 LF 之前创建的 Glue Catalog Resource 不受 Data Lake Permission 以及 S3 Location 的限制. 而在启用 LF 之后创建的 Catalog 自动受 LF 的管理. **所以如果你想要启用 LF, 建议在你创建第一个 Glue Catalog 之前就启用 LF**.


2. Define one or more Administrator
------------------------------------------------------------------------------
你第一次来到 LF 的 console, 会看到一个 "Welcome to Lake Formation" 窗口, 让你选择 LF Administrator. 这个 Admin 的全名叫做 Lake Formation Data Admin (下简称 Admin). 关于 Admin, 有这些知识点:

- LF 上可以有一个或多个 Admin, 互相之间完全等价.
- 第一次你登录的 Iam Role (或 User) 只要有 ``LakeFormationDataAdmin`` managed policy, 就可以指定别人或者自己为 Admin.
- 只有 Admin 可以指定别人为 Admin.
- Admin 最好是实际的 IAM User, 而不是 IAM Role.
- Admin 操作 LF 资源比如 LF Tag, attach tag to resource, grant permission 是无需额外权限的.


3. Define Data Catalog Settings
------------------------------------------------------------------------------
在启用 LF 后, 第一件事情就是要到 "Data Catalog Settings" 菜单下 uncheck 两个重要选项:

- [ ] Use only IAM access control for new databases
- [ ] Use only IAM access control for new tables in new databases

**这两个选项一定要 Uncheck! 这两个选项一定要 Uncheck! 这两个选项一定要 Uncheck! 重要的事情说三遍**, 这事因为原先 LF 是没有 Tag based management 选项的, 只有 named resource 这种 O(N^2) 复杂度的数据权限管理模式. 而具体实现是通过让 LF 维护一个对用户不可见, 内部的 ``IAMAllowedPrincipal`` Role, 里面用 IAM Policy 的方式定义了 "谁能对什么资源做什么". 用户或 IAM Role 每次对资源进行操作, 都会自动 assume 这个特殊的 Role. 理解了这点, 上面两个选项的意思就是说, 如果你启用了 LF, 一旦你创建了新的 Data Catalog Database / Table, 你必须用 Iam Role 中的 Glue 相关的 Policy 和 Glue Catalog Resource Policy 来 grant 权限, 而 Lake Formation 的 LF Tag 和 Named Tag 则没用. 这两个选项完全是为了 backwards compatibility 而设置的.

Ref:

- https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-reference.html
- https://docs.aws.amazon.com/lake-formation/latest/dg/change-settings.html


4. S3 Bucket Setup
------------------------------------------------------------------------------
虽然 S3 是一个 Globally 的服务, 但是每个 S3 Bucket 实际上只会被部署到一个 Region 中. 虽然你可以用位于一个 Region 的 EC2 / Lambda 从位于另一个 Region 的 S3 Bucket 读数据, 但是性能上不划算. 由于 LF 是一个 Region 的服务, Glue Catalog 也是一个 Regional 的服务, 所以我推荐对每个 Region 的 Data Lake S3 Bucket, 要保证 Bucket 是在同一个 Region 下.

每一个 Region 的 S3 的 file structure 我推荐使用下面的结构::

    s3://111122223333-us-east-1-data1/datalake/${database_name}/${table_name}/${partition}/${data_filename.parquet}

    # 可能有多个跟 data1 类似的 bucket
    s3://111122223333-us-east-1-data2
    ...
    s3://111122223333-us-east-1-data3
    ...


5. Register Data Lake Locations
------------------------------------------------------------------------------
在 Lake Formation Console -> Register and ingest -> Data lake locations 这个 Menu 下, 你可以将 S3 Folder 注册为 Data Lake Location. 从而让 Lake Formation 提供 Storage Level Permission (来自官方文档, 不是人话).

- 在启用 LF 之前创建的 Glue Catalog Table, 你可以无需任何设置就用 Athena 对其进行查询
- 在你启用了 LF 之后, 所有新创建的 Glue Catalog Table 自动受 Catalog 的保护, 你必须先将数据所在的 S3 location 注册成 Data Lake Location, 并且给 Glue Table 和 IAM Role 加上 LF Tag 之后才能用 Athena 进行 Query.
- 如果你将一个 S3 Location 注册成 Data Lake Location 了之前, 你基于里面的数据创建一个 Glue Catalog Table 或者更改这个 Table 都是没有限制的.
- 如果你将一个 S3 Location 注册成 Data Lake Location 了, 你的 Glue Catalog Table 只要指向那个 S3 Location, 你还额外需要 Data Location Permission.

Ref:

- https://docs.aws.amazon.com/lake-formation/latest/dg/getting-started-setup.html#register-s3-location
