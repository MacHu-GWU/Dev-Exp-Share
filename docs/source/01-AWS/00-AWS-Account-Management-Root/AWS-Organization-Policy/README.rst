AWS Organization Policy
==============================================================================


What is AWS Organization Policy
------------------------------------------------------------------------------
Policies in AWS Organizations enable you to apply additional types of management to the AWS accounts in your organization. 就是说和 IAM Policy 类似, 能提供能细粒度的控制.

- Authorization policies: Authorization policies help you to centrally manage the security of the AWS accounts in your organization.
    - `Service control policies (SCPs) <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html>`_: offer central control over the maximum available permissions for all of the accounts in your organization. 这个最重要, 也最常用. SCP 就像是一个 IAM Policy, 不过它是针对 Account 下所有的 IAM User 和 Role 的, 用来管理这个 Account 下的 User 和 Role 最大的权限范围. 注意, SCP 只是指定最大权限范围, 即使里面包含了允许你访问 XYZ, 但是你还是要用 IAM Policy 给你的 User 和 Role XYZ 的权限才行.. AWS Organization 默认会创建一个 ``FullAWSAccess`` 的 SCP, 而且会自动 attach 给你的所有 Account, 也包括 ROOT 和 OU. 这就意味着默认情况下你下面的所有的 Account 都能用所有的 AWS Services. 而我们如果熟悉 IAM Policy 的话, 它的规则是 "显式Deny > 显式 Allow > 默认 Deny". 也就是说我们一般有两种定义 IAM Policy 的模式, 一种是做加法, 全部默认 Deny, 需要什么加什么. 另一种是做减法, 默认全部 Allow, 不允许用什么减掉什么. 如果我们要做加法, 那么我们就要把这个自动创建的 ``FullAWSAccess`` 从所有的 OU 和 member account 上 Detach 掉, 然后手动创建 SCP 允许一些 AWS Services. 如果我们要做减法, 那么就保留这个 ``FullAWSAccess``, 然后手动创建 SCP 禁止一些 AWS Services.
- Management policies: enable you to centrally configure and manage AWS services and their features.
        - `Artificial Intelligence (AI) services opt-out policies <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html>`_: enable you to control data collection for AWS AI services for all of your organization's accounts. 这个是给 AI 相关的 AWS Services 用的. 因为 AI 相关的 AWS Services 大多都是 AWS Managed, 而且必然要访问你的 business data.
        - `Backup policies <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_backup.html>`_: help you centrally manage and apply backup plans to the AWS resources across your organization's accounts. 这个是给 AWS Backup, 一个用来备份你的 AWS Account 上的数据的全托管服务.
        - `Tag policies <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html>`_: help you standardize the tags attached to the AWS resources in your organization's accounts. 这个是用来管理你的 Accounts 里面的 Resource Tag 的, 比如要求 TagKey 用 Camel Case 还是 all uppercase. 给定的 TagKey, 它的 Value 必须是指定的几个之一. 或者对 Tagging 做出强制要求.

Ref:

- Managing AWS Organizations policies: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies.html?icmpid=docs_orgs_console