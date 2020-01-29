Identity Authentication Management (IAM)
==============================================================================

.. contents::
    :local:

Important Concept
------------------------------------------------------------------------------

- Policy: 控制对 AWS 具体的 Resource 的使用, 非常具体, 非常精细.
- User: 一个 AWS 用户的具体权限, 由许多 Policy 组成.
- Role: 一个 AWS Resource 的具体权限, 由许多 Policy 组成.
- User Group: 所有被归入该用户组的用户自动获得该组给予的权限.


Policy Evaluation Logic
------------------------------------------------------------------------------

Explicit Deny > Explicit Allow > Default Deny


Useful Feature
------------------------------------------------------------------------------

- Resource Policy: 比如 S3, SQS, Glue Catalog 等资源都可以设置 Resource 级别的 Policy 作为 IAM 的补充. 简单来说 IAM 决定了用户可以做哪些事, Resource Policy 决定了哪些用户可以对自己做哪些事.
- Organization Service Control Policy: 是一个组织对整个账户进行的限制.
- Permission Boundary: 是一个高级应用, 作用于 IAM User 和 IAM Role, 决定了这个用户的最大权限. 如果没有这个设定, 例如 IAM User 如果被禁止删除 S3, 但是允许创建 IAM, 那么这个用户可以创建一个可以删除 S3 的 Role 然后删除之. 这个叫做 Cascade Update. 设置了 Permission Boundary 可以避免这种情况.

当这三个概念和传统的 IAM Policy 互相作用时如何决定用户的最终权限, 请参考这篇博文:

- Permissions Boundaries for IAM Entities https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html

