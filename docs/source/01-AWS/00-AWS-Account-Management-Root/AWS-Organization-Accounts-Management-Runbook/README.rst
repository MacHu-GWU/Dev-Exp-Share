AWS Organization Accounts Management Runbook
==============================================================================
这篇文档介绍了当你作为一个公司的 AWS Account Admin, 如何配置你公司的 AWS Accounts 的具体操作步骤.


Use AWS Organizations WITHOUT AWS Control Tower
------------------------------------------------------------------------------
如果你不了解 AWS Control Tower 是什么, 请阅读下一章的开头部分.


1. 创建 Root Account 以及为 Root User 配置 MFA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
首先, 用你公司 AWS Account Admin 负责人的 email 注册一个新的 AWS Account, 这个 Account 就作为你的 AWS Organizations 的 root account, 也叫 management account.

这个时候你登陆是用的 Root user 的 email 和 password 登录的. 接下来一定要迅速的为这个 Root user 创建 MFA 登录, 到 IAM 里面 Scan QR code, 在你的手机上设置 MFA. 最好用 Microsoft Authenticator, 能将 MFA 自动备份到云端. 接下来, 除了管理 bill 之类的事情, 不要再用这个 Root user Account 登录了. 这是因为 Root user 的 email 被 hack 了, 这个 email 是超过了 AWS 的管理范围的, AWS 什么都做不了. 正确的管理做法是在 Root Account 上创建一个 IAM User 并授予 Admin 权限. 这个 IAM User 是可以随时被删除, 重新创建的. 在出现问题的时候我们有能力进行修复并减小损失. 所以下一步就是在 Root Account 上创建一个 IAM User.


2. 创建 IAM User on Root Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在这一节我们要为 Root Account 创建一个 IAM User, 用于日常管理 AWS Organization 的活动. 建议也为这个 IAM User 配置 MFA.

默认情况下 IAM User 即使有 Admin 权限, 也是无法看到 billing 相关的信息的, 只有每个 Account 的 Root User 有这个权限. 在企业中用 IAM User 编写程序对 billing 信息进行处理室非常有必要的. 你可以参考下面这篇文章显式地给与 IAM User billing 相关的权限.

Reference:

- How can I troubleshoot access denied errors related to the Billing and Cost Management console?
: https://aws.amazon.com/premiumsupport/knowledge-center/iam-billing-access/


3. 用 AWS Organizations 创建 Member Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们已经有一个 Root Account 了, 接下来就是创建更多的 OU 以及 Member Account. 首先在 Root Account 里创建一个 AWS Organization. 之后你要创建新的 AWS Account, 就不要再像开始那样注册新的了, 而是用 AWS Organization 里的工具创建.

如果不用 Control Tower, 我建议至少创建三个 Account 和 OU::

    root (ROOT)
    |-- infra (OU)
        |-- infra (Account) 用于管理 infrastructure as code, 这个 account 也是 delegated cloudformaiton stackset admin
    |-- sandbox (OU)
        |-- sandbox1 (Account) 用于隔离测试
    |-- app (OU)
        |-- app-dev (Account) 用于运行 app
    |-- root (Account) 这个就是前面创建的 root (management) account

在创建 Account 的时候, 填写 email 的时候建议使用 email alias. 例如你 root user email 是 myname@email.com, 而你创建的 account alias 叫做 app-dev, 那么你创建这个 account 的时候的 email 就应该用 myname+app-dev@email.com. 这样能让 member account 的 email 汇总到 root account 的 email. 不然每个 account 都要一个不同的 email, 你会管理不过来的.

Reference:

- After I use AWS Organizations to create a member account, how do I access that account?: https://aws.amazon.com/premiumsupport/knowledge-center/organizations-member-account-access/
- Accessing and administering the member accounts in your organization: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html


Use AWS Organizations + AWS Control Tower
------------------------------------------------------------------------------
AWS Control Tower 是一个标准化管理 OU 和 Landing Zone 的服务, 简单来说就是不用你手动配置 OU, 而是直接用 AWS best practice 来配置 OU, 并且将 cloud trail log 都汇总到一个 Account 来做 audit. 这个对于每月 AWS 开销在 1w 美元以上的企业当然是有必要的, 但是对于初创企业来说很可能不是必要的.