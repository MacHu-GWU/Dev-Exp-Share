AWS Organization Accounts Management
==============================================================================

对于个人用户, 你的 Amazon 购物网站的账户, 就是你的 AWS Root 账户, 这个非常简单. 我们重点讨论一下企业用户如何管理 AWS 账户.

首先我们要知道的是, 一个 Amazon 账户下的资源是有限制的, 比如默认状态下最多能创建 5 个 EIP IPV4 地址, 最多能创建 100 个 S3 Bucket, 最多创建 200 个 CloudFormation Stack, 等等, 如果要提高这些限制, 你需要联系 AWS 提高这些限制. 所以对于企业用户, 一个企业不可能只有 1 个 AWS 账户.

其次一个企业有不同的部门, 你不希望一个部门或是一个项目的管理员能够有权限更改其他部门或是项目的云资源. 最简单的隔离方法就是使用不同的 AWS 账户.


AWS Account 和 Organization 相关的术 语 和 概念
------------------------------------------------------------------------------

在进入企业用户的 AWS 账号管理之前, **首先, 我们来了解一下 AWS Account 和 AWS Organization 的一些基本概念**.

- Ref: https://aws.amazon.com/cn/blogs/china/aws-organizations-multi-account-management/

- Organization - 组织: 一系列的 AWS 账户.
- AWS account – 账户: 单个 AWS 账户.
- Master account – 主账户: 在组织中为所有账户付款的账户, 管理你的组织的中心节点.
- Organizational unit (OU) – 组织单元: 逻辑上的 子 Organization, 由多个 AWS 账户组成, 跟 AWS 账户是 多对多 的关系.
- Administrative root – 管理根: 管理根是整理AWS账户的起始点, 也是整个组织层次架构中的最顶层的容器.
- Organization control policy (OCP) – 组织控制策略: 定义您要应用于某个 Organization 或 OU 的 AWS账户的控制策略. 而具体的 Poilicy 叫做 Service Control Policies (SCP), OCP 是一个概念, SCP 是 OCP 的一个实例.

.. image:: ./OU-OCP-SCP.png
    :width: 800 px

所以, 假设你是一个初创企业, 你的 AWS 账户管理应该是这样的:

.. image:: ./AWS-Account-Management-in-Enterprise.png
    :width: 800 px

简单来说, **OU 的结构最好跟行政组织结构一致. 这里我推荐 首先基于行政结构 像树一样管理各个部门的 OU 主账号. 而在 OU 下则按照项目给每个需要互相隔离的 Project 分配独立的 AWS 账户. 而相互之间需要通过内网通讯的项目, 最好放在同一个 AWS 账户下**. 而相互之间需要通过公网通讯的项目, 可以不放在不同的 AWS 账户下.

**权限控制**:

子 OU 会从母 OU 继承 Policy. 而在某个 OU 下的 AWS 账户中的 IAM User 和 Role 的最终权限, 由 OU 的 SCP 以及 IAM User / Role 的 Policy 共同决定.

例如: OU 允许你控制 A, B 服务, 而 IAM 允许你控制 B, C 服务, 那么你只能控制 B 服务.


禁止普通 IAM User 创建其他 IAM User, 并使用 Assume Role
------------------------------------------------------------------------------

- Q: 为什么要禁止 IAM User 创建其他 IAM User?
- A: 因为作为公司, 公司需要管理用户创建 IAM User 的行为, 并使用 IAM User 来追踪用户的使用行为. 如果允许用户自行创建其他的 IAM User, 那么公司就很难追踪这些新创建的 IAM User. 这叫做 preventing cascade creation.

- Q: 如果我需要使用其他的 IAM User 进行测试该怎么做? 我可能需要同时使用 Console 和 Cli. 比如我需要使用一个 Machine User 进行项目的 Deploy, 我需要知道这个 Machine User 所需要的最小权限是什么, 所以我需要一个 IAM User 进行测试.
- A: 你可以使用 Assume Role 的方式, 创建一个 IAM Role, 用来模拟 IAM User 的权限, 然后在 Console 和 Cli 中 Assume 这个 Role 进行测试.

- Q: 使用 Assume Role 的好处?
- A: 不用频繁的登录切换 IAM User, 减少管理 ACCESS KEY 的麻烦.

1. 创建一个 IAM Role, 在 Select type of trusted entity 中选择 Another AWS Account, 并填入你当前的 AWS Account Id (12位数字)
2. Attach 对应的 Policy, 这些 Policy 会成为你想模拟的 IAM User 的 Policy.
3. 给这个 IAM Role 一个名字, 里面最好包含 Assume Role, 以表示其功能.
4. 在 Console 的右上角点击自己的 Account, 选择 Switch Role, 填入你的 AWS Account Id 和 Policy Name (你刚才起的名字). 此时你在 Console 中的权限就跟 Assume Role 中的一样了.
5. 如果要切换回来, 在 Console 右上角点击自己的 Account, 选择 back to xxx 即可.
6. 如果要使用 CLI, 请参考官方文档 https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html, 简单来说就是将你的 ``$HOME/.aws/credentials`` 文件修改成如下样子, 然后在你的 Cli 中加上 ``--profile my_iam_user_assume_role`` 选项, 或是在 SDK 中加上 ``boto3.Session(profile_name="my_iam_user_assume_role")`` 即可::

    [original_iam_user_profile]
    aws_access_key_id = AAAAAAAAAAAAAAAAAAAA
    aws_secret_access_key = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    [my_iam_user_assume_role]
    role_arn = arn:aws:iam::123456789012:role/my-assume-role
    source_profile = original_iam_user_profile
