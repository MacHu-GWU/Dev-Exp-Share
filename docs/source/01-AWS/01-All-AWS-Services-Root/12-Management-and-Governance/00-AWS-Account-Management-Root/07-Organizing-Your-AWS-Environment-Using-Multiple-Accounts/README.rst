.. _organizing-your-aws-environment-using-multiple-accounts:

Organizing Your AWS Environment Using Multiple Accounts
==============================================================================


Summary
------------------------------------------------------------------------------
这篇博文是阅读这篇 `同名 AWS Whitepaper <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html>`_ 的笔记. 介绍了在企业中如何正确地管理多个 AWS Accounts.


为什么要用多个 AWS Accounts
------------------------------------------------------------------------------
如果别人有这个疑惑, 要能跟人用人话解释的清楚. 主要有这么几点:

1. Group workloads based on business purpose and ownership: 将云资源按照 business purpose 和 ownership 分组, 以便于管理和审计.
2. Apply distinct security controls by environment: 对于不同的 workload security 的级别是不同的. 例如 prod 和 non prod 的安全级别肯定是不一样的.
3. Constrain access to sensitive data: 对于 data 的安全级别也是不一样的.
4. Promote innovation and agility: 允许开发者在隔离的环境中不受限制的实验一些东西有助于创新. 这里有 sandbox account 和 dev account 两个概念. sandbox account 指的是跟你的业务, data 完全 disconnected 的 account, 通常是可以不受限制的做实验. dev 则是能在受管制的情况下访问一些业务和 data, 同时又有比较大的 freedom 来做实验.
5. Limit scope of impact from adverse events: 隔离风险
6. Support multiple IT operating models: 不同公司有不同的 IT operating model (IT 管理模型), 显然如果只有一个 account 是无法适应复杂多变的需求. 而用多个 accounts 就能灵活的排列组合出你想要的需求了.
7. Manage costs: 管理开支
8. Distribute AWS Service Quotas and API request rate limits: 每个 account 是有 service quotas 的, 对其进行分流可以有效的避免 quota limit 的问题.

Ref:

- https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/benefits-of-using-multiple-aws-accounts.html


一些核心概念
------------------------------------------------------------------------------
这节是了解在企业中如何管理 AWS Accounts 的重点. 要仔细阅读.

有这么一些关键概念啊:

- AWS Organizations: 一个能 administer 很多 accounts 的 entity. 通常一个法律和财务上注册的公司就是一个 organization, 底下会有很多部门. 而如果这是一个集团公司, 那么集团下面的公司都可以视为一个个独立的 organization. 而如果这个公司还有子公司, 但是母公司和子公司的关系又没有大到集团公司那种关系, 那么子公司既可以被视为独立的 organization, 也可以归属于母公司的 organization.
- Organizations management account: 一个 org 只有一个 management account, 相当于 root account, 里面不跑业务, 而是专门用来管理其他 accounts.
- Organizations member accounts: 用来跑具体业务, 同时自己下面没有别的 member 归属自己, 那这就是一个 member account
- Organizational Units (OU): 将多个 member accounts group 到一起的逻辑概念, 每一个 OU 可以按照部门, 项目, 业务等来分组. OU 是 Org tree 上面的一个父节点, 它是 AWS Organizations 里的一个概念, 而不是实体的 AWS Account. 每个 OU 可以有一个 Policy, 这个 Policy 会自动应用到所有的子节点上.

每个 Organization 一般会包含:

- A management account
- Zero or more member accounts
- Zero or more organizational units (OUs)
- Zero or more policies

Ref:

- Core Concept: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/core-concepts.html
