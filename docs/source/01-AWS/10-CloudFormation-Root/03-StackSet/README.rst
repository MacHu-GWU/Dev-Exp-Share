Stackset Docs
==============================================================================

.. contents::
    :local:


FAQ
------------------------------------------------------------------------------

- Stackset 解决了什么问题?
- Stackset 能允许用户将 CloudFormation Template Deploy 同时 deploy 到多个 REGION, 乃至多个 Account 的多个 Region.

- 将一套 CloudFormation Template Deploy 到多个 Account 有什么好处?
- 很多企业使用大量的 AWS 账户, 通常用 AWS Organization 将这些账户按照部门, 项目分层. 很多用户希望对这些账户按照一定的内部标准进行管理.

- 将一套 CloudFormation Template Deploy 到个 Region 有什么好处?
- 很多企业的生意是全球化的, 他们将跨区域构建他们的应用. 为依据国家和地区的法规处理敏感数据以及选择存储位置. 另外, 多区域灾难恢复对于大型企业也是必须的.

- 你的这些回答的依据是?
- https://aws.amazon.com/cn/blogs/china/use-cloudformation-stacksets-to-provision-resources-across-multiple-aws-accounts-and-regions/


Stackset 的权限管理
------------------------------------------------------------------------------

- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html