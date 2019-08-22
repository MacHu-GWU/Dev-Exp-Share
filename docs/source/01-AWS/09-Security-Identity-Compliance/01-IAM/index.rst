IAM
===


Important Concept
------------------------------------------------------------------------------

- Policy: 控制对 AWS 具体的 Resource 的使用, 非常具体, 非常精细.
- User: 一个 AWS 用户的具体权限, 由许多 Policy 组成.
- Role: 一个 AWS Resource 的具体权限, 由许多 Policy 组成.
- User Group: 所有被归入该用户组的用户自动获得该组给予的权限.


Resolve Policy Conflict:

Explicit Deny > Explicit Allow > Default Deny