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


Stack Set vs Stack Instances
------------------------------------------------------------------------------
在第一次接触 StackSets 的时候, 有一个误区是认为 StackSets 是 Stack 的等效概念. Stack 是在具体的 Account 和 Region 上被部署的实体, 里面包含了很多 Resources. 而 StackSet 只是 Stack 的 Metadata, 本身不包含任何 Resources. StackSet 只是负责根据 Metadata 来在各个 Account 和 Region 上创建 Stack Instances. 你可以把它理解为一个 Stack 的模板. 你可以在 StackSets 上部署多个 Stack Instances. 而 Stack Instance 才是在具体的 Account 和 Region 上 StackSet 的实例, 每一个 Stack Instance 一般会对应一个具体的 Stack. 它们的差别是 Stack Instance 有可能会创建 Stack 失败, 此时 Stack Instance 没有 Stack 与之对应.

我们在用 StackSet 管理 管理 IAC 的时候, 一般有以下四种情况:

1. 第一次将 AWS Resources 通过 StackSet 部署到多个 Accounts / Regions 上.
2. 保持 Accounts 和 Regions 不变, 改变 Template.
3. 保持 Accounts 和 Regions 不变, Template 也不变, 但改变 Parameter.
4. 保持 Template 不变, 新增或删除 Accounts 和 Regions.

如果我们既要改变 Template, 又要改变 Accounts 和 Regions. 那么我建议先改变 Template, 然后再改变 Accounts 和 Regions. 因为如果你先改变 Accounts 和 Reginos, 那么可能会将旧的 Template 部署到新的 Accounts 和 Regions 上, 然后你之后又要更新 Template. 而如果你先改变 Template, 那么当你增加新的 Accounts 和 Regions 上的时候, 就可以直接部署最新的 Template 了.

下面我简要的描述一下这四种情况需要怎么做.

1. 第一次将 AWS Resources 通过 StackSet 部署到多个 Accounts / Regions 上.
    - 先调用 `create_stack_set <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/create_stack_set.html>`_ API, 用你定义的 Template 创建一个 StackSet
    - 然后用 `create_stack_instances <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/create_stack_instances.html>`_ API, 在指定的 Accounts 和 Regions 上创建 Stack Instances. 这个 API 会在每个 Account 和 Region 上创建一个 Stack.
    - 等待所有的 Stack instances 的状态都变为 ``CURRENT``.
2. 保持 Accounts 和 Regions 不变, 改变 Template.
    - 调用 `update_stack_set <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/update_stack_set.html>`_ API, 更新 StackSet 的 Template, 然后改变就会被自动的 propagate 到已经成功部署的所有的 Stack Instances 上.
    - 等待所有的 Stack instances 的状态都变为 ``CURRENT``.
3. 保持 Accounts 和 Regions 不变, Template 也不变, 但改变 Parameter.
    - 调用 `update_stack_instances <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/update_stack_instances.html>`_ API, 更新 Stack Instances 的 Parameter.
    - 等待所有的 Stack instances 的状态都变为 ``CURRENT``.
4. 保持 Template 不变, 新增或删除 Accounts 和 Regions.
    - 如果你既有增加又有删除, 则你需要分两次分别调用 `create_stack_instances <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/create_stack_instances.html>`_ 和 `delete_stack_instances <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/delete_stack_instances.html>`_ API.
    - 增加的时候要等待所有的 Stack instances 的状态都变为 ``CURRENT``.
    - 减少的时候要等待所有的 Stack instances 都被成功删除.

当然, 以上的操作都是有可能出错或者失败的. 为了学会如何处理部署失败的情况, 我们需要了解 Stack Instance 的状态码含义. 以下的解释来自于 `官方文档 <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/list_stack_instances.html>`_:

Status: 对一个 Stack Instance 的操作已经停止后的状态码. 操作进行中的其他状态码请参考 Detailed Status.

- ``INOPERABLE``: 说明 ``DeleteStackInstances`` 的操作失败了, 导致目前的状态不稳定. 你对这个 StackSet 执行的任何修改都会 ignore 这个 stack instance. 修复这个问题的方法是先 delete 这个 stack instance, 然后手动到 Account 上 delete 这个 stack 并清理掉所有的 resources.
- ``OUTDATED``: Stack Instance 的状态跟 StackSet definition 里的不一致. 有两种情况会导致这种状态:
    - create / update stack set 的时候会自动把 change apply 到已经部署的 stack instance, 但没有成功. 一般是因为你的 Template 有问题. 解决这个问题的方法是修复你的 Template 然后运行 update stack set.
- ``CURRENT``: Stack Instances 的状态跟 StackSet definition 的一致. 也就是通俗理解的 Succeeded.

Detailed Status: 这是操作正在进行中的详细状态码, 你需要用 polling 的方式隔一段时间查询一下每个 Stack instances 的状态到哪里了.

- ``CANCELLED`` : The operation in the specified account and Region has been canceled. This is either because a user has stopped the stack set operation, or because the failure tolerance of the stack set operation has been exceeded.
- ``FAILED`` : The operation in the specified account and Region failed. If the stack set operation fails in enough accounts within a Region, the failure tolerance for the stack set operation as a whole might be exceeded.
- ``INOPERABLE`` : A DeleteStackInstances operation has failed and left the stack in an unstable state. Stacks in this state are excluded from further UpdateStackSet operations. You might need to perform a DeleteStackInstances operation, with RetainStacks set to true , to delete the stack instance, and then delete the stack manually.
- ``PENDING`` : The operation in the specified account and Region has yet to start.
- ``RUNNING`` : The operation in the specified account and Region is currently in progress.
- ``SUCCEEDED`` : The operation in the specified account and Region completed successfully.


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


IAM Role on Delegated Administrator Account
------------------------------------------------------------------------------
这里我有一个疑问, 设置 delegated admin 的时候指定了 account id, 并没有说具体的 Role. 那么是不是说只要在这个 account 上的 IAM Role, 只要它有 AWS CloudFormation 的权限, 都可以对整个 org 上的 CFT 进行操作? 经过我的验证, 答案是 YES.

Trusted Entity::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::393783141457:root"
                    ]
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    }
