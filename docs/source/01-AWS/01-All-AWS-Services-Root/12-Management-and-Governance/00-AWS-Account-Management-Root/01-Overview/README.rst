AWS Account Management Overview
==============================================================================


How it Works
------------------------------------------------------------------------------
在企业中当你的业务和开发者多了以后, 一个 AWS Accounts 必然就无法满足业务需求, 必然要将业务分散到多个 AWS Accounts 中去. 而这里的核心就是通过 AWS Organizations 这个专门为该目的设计的 AWS Service 来管理. 简单来说就是参考你的公司架构图和业务架构图, 构建一个 AWS Accounts 的架构图, 并将其归属到一个 AWS Organization 这样的逻辑概念中去. 如果你的公司特别大, 是集团公司, 或是有很多子公司, 那么你还需要很多个 AWS Organizations.


How to Learn
------------------------------------------------------------------------------
有两个文档非常有帮助, 一个是 AWS Whitepaper, 更加容易上手, 从需求出发详细的讲解了你需要知道的概念和思路. 另一个是  AWS Organizations 这个 Service 的 User Guide, 有点像开发者手册, 比较具体的讲里面的功能怎么用. 建议从 AWS Whitepaper 开始.

- AWS Whitepaper - Organizing Your AWS Environment Using Multiple Accounts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html?did=wp_card&trk=wp_card
- AWS Organizations User Guide: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html


How to Build
------------------------------------------------------------------------------
AWS Account 有 Free tier, 允许你实验性的使用大多数的服务. 并且 AWS Account 没有最低消费的限制. 而且对于 AWS Account Management 来说, 你要做的主要是:

- 创建 AWS Account
- 创建 AWS Organization
- 创建 Organizational Unit (OU)
- Attach Service Control Policy (SCP) 到 OU
- 用 CloudFormation 来部署 IAM Permissions

以上这些都不收费. 你可以自己开几个 Account 做实验. 之后将它们 Close 掉即可.

Reference:

- AWS Free Tier: https://aws.amazon.com/free
- How do I create and activate a new AWS account?: https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/?p=ft&z=subnav&loc=4&refid=78b916d7-7c94-4cab-98d9-0ce5e648dd5f
- How do I close my AWS account: https://aws.amazon.com/premiumsupport/knowledge-center/close-aws-account/
