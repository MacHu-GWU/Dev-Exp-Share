AWS Lambda and VPC
==============================================================================
Keywords: AWS Lambda VPC, Public, Private Subnet, NAT Gateway, VPC Endpoint


Overview
------------------------------------------------------------------------------
在默认设置下 (不开启 VPC) Lambda function 是放在由 AWS 管理的网络环境中的, 并且是有 outbound public network access 的. 你可以将其视为一个 AWS 管理着的 VPC, 只不过这个 VPC 对开发者不可见. 这种情况下的 Lambda 可以视为一个在你的笔记本电脑上跑的程序, 网络是公网上的任意一个 Wifi. 但有的时候你的 Lambda 需要访问一些位于 VPC 内的资源, 例如跟位于 Private Subnet 的数据库通信, 这时 Lambda 就必须要部署在在你自己的 VPC 内了 (我们不讨论 SSH Tunnel 这一类用跳板机的技术). 本文详细的介绍了在 VPC 内使用 Lambda 的方方面面.


Lambda 访问公网
------------------------------------------------------------------------------
我们知道, VPC 里有 Public Subnet 和 Private Subnet. 对外的流量 Public Subnet 走 Internet Gateway, Private Subnet 走 Nat Gateway. 和位于 Public Subnet 上并开启了自动 Public IP 的 EC2 不同, **Lambda 没有 Public IP, 而只有 Private IP, 所以 Lambda 就算放在 Public Subnet 上也无法访问公网**. 如果你的 Lambda 必须要访问公网, 那么你需要给你的 Private Subnet 创建一个 NAT Gateway 并且把 Lambda 放在 Private Subnet 上. 因为 Private Subnet 的对外的路由是走 NAT Gateway 的.

将 Lambda 部署到 VPC 中的时候, 我们需要注意以下几点:

- 如果你的 Lambda 需要访问公网, 则 Lambda function 一定要放在 Private Subnet 上而不是 Public Subnet 上. 因为 Public Subnet 路由不走 NAT.
- 如果你的 Lambda 只需要私网流量, 例如只跟数据库通信, 则 Lambda function 可以放在 Public Subnet 上. 因为 Public Subnet 上的 Lambda 无法访问公网.


Lambda 访问 AWS Service API
------------------------------------------------------------------------------
所有的 AWS Service API 本质上都是一个位于公网的 API Endpoint. 例如 S3 的 get_object / put_object API. 默认情况下你的 Lambda 没有配置 Nat gateway 的时候是无法访问公网的, 也就无法访问 AWS Service API. 这篇文档 :ref:`aws-nat-gateway-vs-vpc-endpoint` 介绍了如何让位于私网上的设备访问 AWS Service API, 当然 Lambda 也不例外.


Lambda 和 Security Group
------------------------------------------------------------------------------
Security Group 是 VPC 内的防火墙机制. 和 EC2 一样, Lambda 也可以配置 Security Group. 例如你的 Lambda 需要访问 RDS Database, 那么你可以为 Lambda 和 RDS 创建一个 Security Group, 并在其中定义允许从自己这个 SG 的来的所有流量. 这样就能让 Lambda 访问 RDS 了. 由于 Lambda 本身的没有 Inbound, 不存在你要通过网络连接 Lambda 的情况, 所以 Lambda 的 Inbound Rule 就留空的即可. 因为对 Lambda 的请求通常是通过 API 进行的, 你无需 SSH 到 Lambda 上 (也无法这么做).


Reference
------------------------------------------------------------------------------
- `Configuring a Lambda function to access resources in a VPC <https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html>`_: Lambda 官方文档中关于 VPC 的部分.
- `Repost - How do I give internet access to a Lambda function that's connected to an Amazon VPC? <https://repost.aws/knowledge-center/internet-access-lambda-function>`_: 一篇被问过很多次的关于 Lambda 和 VPC 的问题, AWS 官方将其发出来了.
