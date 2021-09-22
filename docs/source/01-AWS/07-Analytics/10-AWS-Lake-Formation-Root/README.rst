
测试用例:

1. 使用 Admin 创建 AWS Glue Database ``lakeformation_access_poc`` 和 Table ``users``, ``items``, ``orders``.
2. 创建一个 Assume IAM Role (Principal 是 AWS Account), 这个 Role 只是为了方便测试, 在 Console Assume 这个 Role 就可以在 Console 模拟使用这个 Role 的权限了. 这样免除了为了测试 Role 还创建 EC2 / Lambda 的麻烦.
3. 先 Assume 这个 Role 测试在 Athena 中 Query ``users`` Table, 确保成功.
4. 用 LakeFormation 限制这个新的 Role, 让他无法在 Athena 中 Query ``users`` Table.
