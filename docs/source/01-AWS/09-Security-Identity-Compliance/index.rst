.. _aws-sic:

Security Identity Compliance (SIC)
==============================================================================

Security, 让特定的人或系统 (Identity), 访问特定的系统, 允许其进行特定的操作, 这就是科技领域内安全的含义.

Identity, 一个身份, 这个身份可以是人, 也可以是虚拟的软件系统. 用各种身份验证的方式, 证明你是某个 Identity 的所有者.

Compliance, 审计, 让第三方监控所有的系统, 所有的操作, 是由哪些 Identity, 在什么时间, 从哪里发起的.

亚马逊有一系列服务能满足 SIC 的需求, 其中比较关键的几个是:

- IAM (Identity, and Access Management): 定义了亚马逊账户, 用户, AWS 服务, 权限, 实现了允许哪些 Identity, 能访问哪些 Service, 进行哪些操作 Action.
- KMS (Key Management Service): 秘钥管理服务, 将你的秘钥托管.
- Secret Manager: 敏感信息管理服务, 将你的敏感信息用 KMS 加密, 安全的传递给有权限的人使用.
- Cognito: 用户登录托管服务, 让你的 APP 轻松用上安全, 效率的登录, 以及权限管理功能.