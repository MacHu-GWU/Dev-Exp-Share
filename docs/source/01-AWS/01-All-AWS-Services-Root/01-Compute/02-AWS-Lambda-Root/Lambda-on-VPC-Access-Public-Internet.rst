How can I grant internet access to my VPC Lambda function?
==============================================================================
Lambda function 默认是放在由 AWS 管理的网络环境中的, 并且是有 outbound public network access 的. 你可以将其视为一个 AWS 管理着的 VPC, 只不过这个 VPC 对开发者不可见.

如果你需要 Lambda function 跟位于 VPC Private Subnet 中的资源进行通信, 例如跟位于 Private Subnet 中的 RDS 数据库通信等. 这时你就需要将 Lambda function 部署到你自己的 VPC 中, 而不是 AWS 管理的 VPC 中.

将 Lambda function 部署到自己的 VPC 中要注意如下事项:

- Lambda function 只能位于 Private Subnet 中, 不能位于 Public Subnet 中.
- 位于 Private Subnet 就意味着默认是没有 outbound public network access 的, 你必须要为其配置 NAT Gateway 才能让其访问公网. 但是这取决于你的应用, 很多私有应用是不需要访问公网的.
- 位于 Private Subnet 的 Lambda function 不能直接跟一些 AWS Service 通信. 这些 AWS Service 的共同特点是它们的客户端程序都是跟一个位于公网的 API Endpoint 通信的. 由于 Lambda function 没有公网访问权限, 所以它们无法直接跟这些 AWS Service 通信. 但你可以为这些 AWS Service 创建 VPC Endpoint, 本质上是一个位于你自己的 VPC 上的 Endpoint, 并自动将流量路由到 AWS 内部的 Endpoint 上, 从而让位于 VPC Private Subnet 中的资源能跟这些 AWS Service 通信.
- 有些网络通信是需要 Security Group (SG) 的, 例如 RDS. 为了让两者能互相通信, 你可以为它们创建一个 SG, 其中定义了允许从自己这个 SG 的来的所有流量, 并将这个 SG 给 RDS 和 Lambda.

Reference:

- `Repost - How do I give internet access to a Lambda function that's connected to an Amazon VPC? <https://repost.aws/knowledge-center/internet-access-lambda-function>`_
