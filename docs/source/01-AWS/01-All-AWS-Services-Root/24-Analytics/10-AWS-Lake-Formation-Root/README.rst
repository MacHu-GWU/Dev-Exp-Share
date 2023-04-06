.. _aws-lake-formation-root:

AWS Lake Formation Root
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:



Q/A:

-




测试用例:

1. 使用 Admin 创建 AWS Glue Database ``lakeformation_access_poc`` 和 Table ``users``, ``items``, ``orders``.
2. 创建一个 Assume IAM Role (Principal 是 AWS Account), 这个 Role 只是为了方便测试, 在 Console Assume 这个 Role 就可以在 Console 模拟使用这个 Role 的权限了. 这样免除了为了测试 Role 还创建 EC2 / Lambda 的麻烦.
3. 先 Assume 这个 Role 测试在 Athena 中 Query ``users`` Table, 确保成功.
4. 用 LakeFormation 限制这个新的 Role, 让他无法在 Athena 中 Query ``users`` Table.







- Setup Lake Formation Admin User: Lake Formation Console -> Left panel menu -> Permission -> Choose administrators -> choose an IAM User
- Register an data lake location: Lake Formation Console -> Left panel menu ->
    - Note: ``AWSServiceRoleForLakeFormationDataAccess`` 是一个 Service Link Role. 一般的 Role 你选择了使用这个 Role, Role 本身的 Policy 不会有任何变化. 而 Service Link Role 会在你选择了 S3 Location 之后, 自动将 S3 Location 添加到 IAM Policy 中, 免除了你手动修改的麻烦.


- Named data catalog resources security: Grant / Revoke a Principal access to a Resource. This is very similar to the legacy Resource Policy.
- LF Tag security model:


X, Resource
Y, Principal

With ``Named data catalog resources`` security model, We need to manage X * Y access definition. With ``LF-Tag`` security model, We only need to maintain X + Y access definition.

aws glue get-resource-policy --resource-arn arn:aws:glue:us-east-1:669508176277:table/lakeformation_access_control_poc/users
aws glue get-resource-policy --resource-arn arn:aws:glue:us-east-1:669508176277:database/lakeformation_access_control_poc