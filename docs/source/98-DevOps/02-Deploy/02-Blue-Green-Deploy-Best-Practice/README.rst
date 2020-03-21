.. _devops-blue-green-deploy-best-practice:

Blue Green Deploy Best Practice
==============================================================================

简单来说, 你需要一个 Endpoint Swap 的模块. 在你将两组 App 实例部署之后, 将 Endpoint 从 Blue 切换到 Green. 该方法通常通过更新 DNS Table 或是 Route Table 来实现.
