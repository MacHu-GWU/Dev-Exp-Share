.. _aws-cloudformation-stacksets:

AWS CloudFormation StackSets
==============================================================================
Keywords: AWS, CloudFormation, CF, CFT, Stack, StackSet, StackSets, Organization, Organizations.


Summary
------------------------------------------------------------------------------
如果这是你第一次接触 AWS CloudFormation StackSets, 请先确保你了解清楚了 AWS CloudFormation Stack 的概念之后再来阅读本文.

- Q: StackSets 是什么?
- A: StackSets 是 AWS CloudFormation 中的一个功能, 用于在多个 AWS Account 和多个 AWS Region 中同时部署 CloudFormation Stack.

- Q: 什么时候需要用 StackSets?
- A: 企业上 AWS 的最佳实践是用 `AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html>`_ 管理多个 AWS Accounts. 通常 Cloud Engineer 拿到一个新的 Account 之后, 需要用 CloudFormation 对其进行一些配置. 但 CloudFormation Stack 只能用于一个 AWS Account 和一个 Region. 按照部门批量配置 CloudFormation Stack 的时候, 一个个手动操作就显得很麻烦. 这时候就需要用到 StackSets. 并且很多企业的生意是全球化的, 他们将跨区域构建他们的应用. 为依据国家和地区的法规处理敏感数据以及选择存储位置. 另外, 多区域一主一备灾难恢复对于大型企业也是必须的.

Ref:

- Working with AWS CloudFormation StackSets: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html
- 使用 AWS CloudFormation StackSets 跨多个 AWS 账户和区域配置资源: https://aws.amazon.com/cn/blogs/china/use-cloudformation-stacksets-to-provision-resources-across-multiple-aws-accounts-and-regions/


Core Concept
------------------------------------------------------------------------------
- Administrator and target accounts: StackSets 是从哪个 Account 上发起的 (Admin)? 要部署到哪些 Account 上 (Target)?
- AWS CloudFormation StackSets
- Permission models for stack sets: 有 Self-Managed 和 Service-Managed 两种模式. Self-Managed 是说你需要自己配置这些 Cross Accounts IAM Permission. 而 Service-Managed 则是 AWS 会帮你配置好这些 Cross Accounts IAM Permission, 前提是你要配置 AWS Organizations. 我的看法是对于整个企业进行管理, 凡是能以 Organizational Unit (OU) 为单位批量部署到左右的子 Account 中去的 StackSets 都用 Service-Managed. 而当 Admin Account 和 Target Accounts 这种一对多的关系无法用 OU 来描述的时候, 你彩用 Self-Managed 模式.
- Stack instances: 每一个 Account 和一个 Region 下具体的哪个 Stack 就是一个 Stack instance.
- Stack set operations: 有四种 operation, Create stack set, Update stack set, Delete stacks, Delete stack set. 这里需要注意的是 Delete 相关的两个 operation, 如果 stackset 里面有 stacks, 你是无法删除 stackset 的, 你必须先删除 stackset 里面的 stacks, 然后才能删除 stackset.
- Stack set operation options: 而在增删改 stackset 的时候, 你可以通过 operation options 来控制 stackset 的行为. 一共有这些选项:
    - Maximum concurrent accounts: 一次最多同时操作多少个 Account.
    - Failure tolerance: 允许百分之多少的 stack instances 失败, 如果低于这个值, 我们依然当做这个 operation 成功了.
    - Retain stacks: 在执行 Delete stacks 的时候, 是否要保留位于 account 和 region 上的 stack.
    - Region concurrency: 是 sequential 还是 parallel.
- Tags
- StackSet status codes
- Stack instance status codes

Ref:

- StackSets concepts: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html


Grant Self Managed Permission
------------------------------------------------------------------------------
如果你选择 Self-Managed 模式, 那么你需要自己配置 Cross Accounts IAM Permission. 官方文档推荐了两种配置模式, 简单模式和高级模式.

Ref:

- Grant self-managed permissions: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Set up basic permissions for stack set operations (简单模式)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
简单模式下的原理是 Admin Account 上有一个特殊的叫做 ``AWSCloudFormationStackSetAdministrationRole`` 的 IAM Role. 而所有的 Target Account 上有一个特殊的叫做 ``AWSCloudFormationStackSetExecutionRole`` 的 IAM Role (名字不能错). 这个 Admin Role 要能 assume Execution Role, 执行 StackSet 的时候就是由 Admin Role 发起, 然后 assume Execution Role 执行.

- 有一个叫做 ``AWSCloudFormationStackSetAdministrationRole`` 的 IAM Role. 这个 Role 要能够 Assume 位于 Target Account 上的 ``AWSCloudFormationStackSetExecutionRole`` IAM Role. 这个被 Assume 的 Execution Role 就是用来真正执行 CloudFormation Stack Create / Update / Delete
Admin Account 需要满足的条件:

- 有一个叫做 ``AWSCloudFormationStackSetAdministrationRole`` 的 IAM Role. 这个 Role 要能够 Assume 位于 Target Account 上的 ``AWSCloudFormationStackSetExecutionRole`` IAM Role. 这个被 Assume 的 Execution Role 就是用来真正执行 CloudFormation Stack Create / Update / Delete 的.
- ``AWSCloudFormationStackSetAdministrationRole`` 的 trusted identity policy 如下::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudformation.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

- 对于有的 region 有的 service principal 默认是 disabled, 这时候你就需要显式允许. 例如下面这个香港地区 Asia Pacific (Hong Kong), 默认就是 disable 的::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "cloudformation.amazonaws.com",
                        "cloudformation.ap-east-1.amazonaws.com"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

- ``AWSCloudFormationStackSetAdministrationRole`` 的 iam policy 如下. 你可以适当降低这个权限::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "sts:AssumeRole"
                ],
                "Resource": [
                    "arn:aws:iam::*:role/AWSCloudFormationStackSetExecutionRole"
                ],
                "Effect": "Allow"
            }
        ]
    }

Target Account 需要满足的条件:

- 有一个叫做 ``AWSCloudFormationStackSetExecutionRole`` 的 IAM Role. 这个 Role 就是用来真正执行 CloudFormation Stack Create / Update / Delete 的.
- trusted identity policy 如下, 把 ``${admin_account_id}`` 替换成 Admin Account 的 ID 即可::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::${admin_account_id}:root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

- iam policy 如下. 你可以适当降低这个权限::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }


Set up advanced permissions options for stack set operations (高级模式)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
高级模式的原理是在 Admin Account 上不再设置 ``AWSCloudFormationStackSetAdministrationRole`` IAM Role, 而 Target Account 上也不再设置 ``AWSCloudFormationStackSetExecutionRole``. 你自己在 Admin Account 上参考之前的 Admin Role, 配置很多个类似的 Admin Role, 不过不叫那个名字了. 然后在 Target Account 参考之前的 Execution Role 上配置很多个类似的 Execution Role, 不过不叫那个名字了. 然后自己在 Policy 中对它们进行排列组合.


Enable Trusted Access with AWS Organization
------------------------------------------------------------------------------
本节非常重要, 你要想用 StackSets 无外乎 Self-Managed 和 Service-Managed 两种模式. 这是 Service-Managed 模式的前提条件.

首先, 你需要在 Management Account (也就是被视为 Root 的 Account) 上开启 AWS Organizations.
 你先要登录到 Management Account 并且以 administrator 的身份登录 Management Account 才能继续, 后面的操作都需要 administrator 权限.

1. 开启 AWS Organizations 后你要确保 "All Feature" 模式是开启的. 还有一种模式是 "Consolidated Billing features" 这个模式只能将你的账单汇总, 没有我们需要的功能.
2. 到 AWS CloudFormation 的 StackSets 页面, 如果你是 Management Account, 那么你会看到一个 "Enable trusted access" 的按钮. 点这个按钮能开启 trusted access 功能. 它会自动在 Management Account 创建一个 ``AWSServiceRoleForCloudFormationStackSetsOrgAdmin`` 的 IAM Role, 它的 Policy 如下. 文档说要先在 Management Account 创建一个 Stack Set 才能给所有的 Member Account 创建 ``AWSServiceRoleForCloudFormationStackSetsOrgMember`` IAM Role, 但我不记得我做过这件事但 Member Account 都有这个 Role 了, 它的 Policy 如下. 我分析后觉得, 底层的机制可能是这样的, 每次你从 administrator Account deploy stackset 的时候, 这个 admin account 首先是一个 member account::

    # AWSServiceRoleForCloudFormationStackSetsOrgAdmin
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowsAWSOrganizationsReadAPIs",
                "Effect": "Allow",
                "Action": [
                    "organizations:List*",
                    "organizations:Describe*"
                ],
                "Resource": "*"
            },
            {
                "Sid": "AllowAssumeRoleInMemberAccounts",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": "arn:aws:iam::*:role/stacksets-exec-*"
            }
        ]
    }

    # AWSServiceRoleForCloudFormationStackSetsOrgMember
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "iam:CreateRole",
                    "iam:DeleteRole",
                    "iam:GetRole"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:iam::*:role/stacksets-exec-*"
                ]
            },
            {
                "Action": [
                    "iam:DetachRolePolicy",
                    "iam:AttachRolePolicy"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:iam::*:role/stacksets-exec-*"
                ],
                "Condition": {
                    "StringEquals": {
                        "iam:PolicyARN": "arn:aws:iam::aws:policy/AdministratorAccess"
                    }
                }
            }
        ]
    }

3. 然后就是 Register a delegated administrator. 意思是从 Management Account 给底下的一个 Account 授权, 让其当你的 Organization 里的 StackSets 的 administrator. 之所以这么设计是因为 Management Account 本身不应该用来做任何开发之类的工作, 只是专门用来管理 Organization 的以及 billing 的. 开发 StackSets 应该在专门的 Account (一般是叫 Infra) 上进行. 这个 administrator account 来负责管理所有针对整个 Organization 或是 OU 的 StackSets.
4. 现在你可以不用登录 Management Account 而是登录 administrator account 来 deploy StackSet 了.

Ref:

- Enable trusted access with AWS Organizations: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-enable-trusted-access.html
- AWS CloudFormation StackSets and AWS Organizations: https://docs.aws.amazon.com/organizations/latest/userguide/services-that-can-integrate-cloudformation.html
- Enable trusted access: https://docs.aws.amazon.com/organizations/latest/userguide/services-that-can-integrate-cloudformation.html#integrate-enable-ta-cloudformation
- Disable trusted access: https://docs.aws.amazon.com/organizations/latest/userguide/services-that-can-integrate-cloudformation.html#integrate-disable-ta-cloudformation


Create / Update a Stack Set
------------------------------------------------------------------------------
在开始之前, 我们很有必要搞清楚 StackSets 是如何一步步将 Infra 的改变部署到多个 Accounts 和 Region 的.

1. 首先, 你得 ``create_stack_set``, 给绑定一个 Template. 这只是 Metadata, 我们还没决定部署到哪些 AWS Account 和 Region 上去呢.
2. 然后要 ``create_stack_instances``, 这一步就要指定 OU, Accounts, Regions 了.
3. 如果你要部署到更多的 Accounts, Regions 上, 那么你还是要用 ``create_stack_instances``.
4. 如果你要更新 Template, 那么你要用 ``update_stack_set``, 一旦 Template 更改, 已经存在的 Stack Instances 就都会自动使用最新的 Template 部署更新.
5. 如果 Template 没有更新, 你只是用最新的 Parameter Value 将更新应用到部分 Accounts, Regions 上, 那么你要用 ``update_stack_instances``. 这个 API 要求这些 Stack Instances 必须是已经存在的, 而且只能更新 Parameter Value. 如果你要更新 Template, 那么你得用 ``update_stack_set``.

这里有几个 API, 我们一定要区分清楚:

- create_stack_set:
- update_stack_set:
- delete_stack_set:
- create_stack_instances:
- update_stack_instances:
- delete_stack_instances:


Example 1 - Use Self Managed Option
------------------------------------------------------------------------------
下面这个脚本为 Admin Account 和 Target Account 批量配置所需的 IAM Role.

.. literalinclude:: ./self_managed_advanced_setup.py
   :language: python

下面这个脚本使用了前一步创建的 IAM Role, 部署, 更新了一个 StackSet.

.. literalinclude:: ./test_self_managed_advanced_setup.py
   :language: python


Example 2 - Use Service Managed Option
------------------------------------------------------------------------------
下面这个脚本部署, 更新了一个 StackSet. 可以看出来用 Organization 来管理 StackSets 的效率要高得多.

.. literalinclude:: ./test_service_managed.py
   :language: python

