.. _aws-lakeformation-cross-account-access-control:

Cross Account Access Control Using Lake Formation
==============================================================================
Keywords: AWS, Lake Formation, LakeFormation, LF

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

术语缩写:

- LF: AWS Lake Formation
- LF Tag: Lake Formation tag based access control, LF 权限管理的模式之一
- Named Res: Named data catalog resource, LF 权限管理的模式之一


要解决的问题
------------------------------------------------------------------------------
LF 可以很好的满足管理一个 AWS Account 内的数据访问权限的需求. 但是作为大企业, 可能有很多部门, 他们各自有各自的 AWS Account, 并 Own 自己的 data. 如何将这些数据打通, 安全的分享对于大型企业来说非常重要. 这也是 Data Infrastructure 的趋势, 也就是 decentralized data mesh 架构, 企业有通用的解决方案解决 Ingestion, Storage, Processing, Analytics, Data Security 的问题. 而各个 Business Owner 用通用的方案构建自己小范围内数据架构, 保证每个组的人数精简有助于提高业务推进速度. 而 Data Mesh 则是解决了这些分布式的 Team 之间如何高效协作的问题. 这也是 Data Infrastructure 在大型企业中的终极形态.

下面我们来介绍如果使用 LF 安全高效地在不同的 AWS Account 之间分享数据.

附录, `Infoq tech talk <https://www.youtube.com/watch?v=ZZr9oE4Oa5U&t=15s>`_ 上的 Data Pipeline Maturity:

1. None
2. Batch
3. Realtime
4. Integration
5. Automation
6. Decentralization


在 LF 中跨账号管理 Data Access 是怎么实现的?
------------------------------------------------------------------------------
1. 我们知道在一个 AWS Account 内, LF Data Admin 可以方便滴构建 Resource / Principal / Permission 之间的权限.
2. 每个 AWS Account 都会有 LF Data Admin.
3. 你无法把 Acc A 中的 Resource grant 给 Acc B 中的 principal. LF Tag 和 Named Res 两种方式都不行.
4. 但是你可以把 Acc A 中的 Resource grant 给 Acc B 账号本身, 因为 AWS Account 本身就是一个特殊的 Principal.
5. 如果两个账号在同一个 Organization 下, 一旦 Grant, Acc B 的 Admin 立刻就能在 LF 中看到. (Glue Catalog 中不行)
6. 如果两个账号不再同一个 Organization 下, Acc B 需要在 `Resource Access Manager Console <https://console.aws.amazon.com/ram/home?#SharedResourceShares:>`_ 下 (这是一个 AWS Service) 点击接受, 然后就能在 LF 中看到了
7. Grant 后 External Account 下的资源就变成了本地资源. Acc B 的 Admin 就可以像管理本地 Resource 一样的管理权限了.
8. #7 不完全正确, 如果你只是想用 API list, describe 这些共享资源, #7 就够了. 如果你要用 Athena 查询这些资源, 那么你需要创建一个 Resource Link (一种虚拟 Database / Table, 作为真实的 Database / Table 的引用) 作为桥梁, 然后把 Resource Link 作为一种特殊的 ``Resource`` grant 给 Principal 即可.


考虑一个具体案例
------------------------------------------------------------------------------
- 我们有两个 Account: acc_A, acc_B, 其中 acc_A 下面有 db_A, tb_A
- 我们想要将 db_A, tb_A 分享给 acc_B 中的非 LF data admin 用户, 让他们能用 Athena 进行查询.

简单来说就是:

1. 每个 Account 的 Data Admin 管理自己 Account 下的 Resource
2. 想要共享资源, 例如 ResOnAccA 想要给 UserOnAccB, 那么 AccA 的 Admin 直接给对方 AccB 这个资源的权限, 其中 Principal 是 AccB 的 AWS Account ID, 而且用的是 named data catalog resource 的模式 (你无法用 LF Tag 的模式因为你无法给外部的 AWS Account 或是位于外部 AWS Account 的资源 attach 一个 LF Tag), AccB 的 Admin 就会获得 Resource 的权限, 然后 AccB 的 Admin 再把权限给 UserOnAccB, 就像操作位于 AccB 上的资源一样.
3. 当 AccA 把资源 Share 给 AccB 时, AccB 需要在 `Resource Access Manager Console <https://console.aws.amazon.com/ram/home?#SharedResourceShares:>`_ 下 (这是一个 AWS Service) 接受邀请, 之后你才能在自己的 LF console 处看到这个资源.
4. 被 AccA 的 LF Share 出去的资源只能在 AccB 的 LF Console 中看到. 在 Glue Console 中 你是无法看到的.


具体案例的实现步骤
------------------------------------------------------------------------------
**在 acc_A 上 LF Data Admin 的工作**

    1. 进入 acc_A LF Console, 找到 Data Lake Permission 菜单里, 点击 Grant 的按钮.
    2. 把 Principal 设为 External Account, 填入 acc_B 的 12 位 ID, **记得按回车输入**.
    3. 选择 Named Data Catalog Resource, 选择 Database, (不要选择 Table) 选择 Describe 和 Describe Grantable Permission. 为什么要勾选 Grantable 是因为你分享给了 acc_B 的 Data Admin, 而 acc_B 的 Data Admin 需要将这个权限 grant 给 acc_B 下的 principal.
    4. 上一步你只是把 Database 分享给了 acc_B. 此时你只能 describe database, 并不能看到下面的 table. 所以现在我们要重复 1 ~ 3, 这次选择 Database 并选择 All Table, 选择 Describe, Select, DescribeGrantable, SelectGrantable Permission.

    至此, acc_A 上的 database, table 都被 share 给 acc_B 了, acc_A 的工作已经完成, 接下来就是 acc_B 的 admin 的工作了.

**在 acc_B 上 LF Data Admin 的工作**

    1. acc_B admin 需要到 `Resource Access Manager Console <https://console.aws.amazon.com/ram/home?#SharedResourceShares:>`_ 找到邀请, 并且点击接受邀请.
    2. 此时已经可以在 LF Console 中看到 acc_A 上的 database 和 table 了.
    3. 点击 Database 菜单, 点击 Create Database, 选择 Resource Link, 选择 acc_A 上的那个 database, 创建一个 resource link. 这里的 resource link 的名字我建议使用 ``rlink_`` 作为 prefix, 这样比较方便分辨哪个是实体 database, 哪个是 resource link. 你无需为 table 创建 resource link, 只需要为 database 创建即可.
    4. 进入 Data Lake Permission 菜单, 点击 Grant 按钮, 这一步是给 acc_B 上的 user 授权.
    5. 选择 Named Data Catalog Resource, 选择 Database (不要选择 Table), 选中 resource link 选择 Describe. 这一步之后 user 就可以在 Athena 中看到 database 了, 但看不到 table.
    6. 重复 #5, 这次选择 Database 后, 在 Table 的 drop down 里手动选择每一个 table (不要选择 all table, 你可以看到底下灰色的字显示的 catalog id, 是 acc_A 的 account id 才是对的), 然后选择 Describe, Select permission.

    至此, acc_B 上的 user 就可以看到所有的 database 和 table, 并进行查询了.

Ref:

- Cross Account How it Works: https://docs.aws.amazon.com/lake-formation/latest/dg/crosss-account-how-works.html
- Resource Access Manager Console: https://console.aws.amazon.com/ram/home?#SharedResourceShares:


FAQ
------------------------------------------------------------------------------

- 对于别的 Account Share 过来的资源, 你无法用 LF Tag 来管理,

