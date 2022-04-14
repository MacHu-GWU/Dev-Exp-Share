Networking in AWS
==============================================================================


Summary
------------------------------------------------------------------------------
这是一篇综述性质的文章. 介绍了 AWS 上与企业组网相关的常见问题以及解决方案.



AWS Networking Services
------------------------------------------------------------------------------
我们先简单了解一下 AWS 有哪些与网络相关的服务

- VPC (Virtual Private Cloud): 云上虚拟私有网络. 免除了企业自己搭建私有网络基础设置的麻烦. 是 AWS 网络的核心
- Direct Connect: 跟合作的 ISP (Internet Service Provider) 在你的 On-Prem 和 AWS 之间拉一条专线. 使得所有 On-Prem 与 AWS 之间的网络通信不经过公网, 不仅保障了隐私, 而且提高了速度, 使得 On-Prem 和 AWS 之间的通信速度和 AWS 内部之间的通信速度一样快.
- VPC Peering: 将多个 VPC 两两连接起来, 使得多个 VPC 的 Subnet 互相能直接通信. 默认情况下两个不同的 VPC 私网之间是无法通信的. 该服务是通过两两连接实现的多个 VPC 互联, 在 VPC 数量变多的时候配置起来会比较麻烦.
- Transit Gateway: 为多个 VPC 以及 On-Prem 提供一个中心化的网关将他们连接起来. 这是 VPC Peering 的升级版, 在 VPC 数量增多的时候为最优解. 当然也更复杂, 更贵.
- VPC Endpoint: 为位于 VPC 内的计算资源例如 EC2 和 AWS 服务之间建立私有连接. 以 S3 为例, 使得 API 请求不走公网的 Endpoint, 而是走私网的 Endpoint, 使得 Traffic 不经过公网, 不仅保障了隐私, 而且提高了速度.
- Client VPN Endpoint: 为企业中的个人用户的电脑提供从任何地方通过 VPN 访问 VPC 的服务. 连上了 VPN 后就相当于已经在 VPC 里面了.

网络通信速度从慢到快:

1. Home -> AWS
2. On-Prem -> AWS (企业的网一般要快些)
3. AWS EC2 on VPC -> AWS (默认走公网)
4. 以下两个差不多:
    - On-Prem -> AWS via Direct Connect
    - AWS EC2 on VPC -> AWS via VPC Endpoint


VPC Peering vs Transit Gateway
------------------------------------------------------------------------------
VPC Peering

- VPC Peering:
    - Advantage:
        - Lowest cost options (便宜)
        - Pay only for data transfer (根据 data transfer 收费)
        - No aggregate bandwidth limit
    - Disadvantage:
        - Complex at scale (不 scale, VPC 多了设置复杂)
        - Max 125 connections per VPC (VPC 之间的两两连线不能超过 125 个, 因为组合数 C(16, 2) = 120 也就是说 VPC Peering 最多支持 16 个 VPC 互联)
        - VPC Peering 不支持 On-Prem 和 VPC 互联

- Transit Gateway:
    - Advantage:
        - Simplified management of VPC connections (Scale)
        - AWS manages the auto scaling and avalaiblity needs (AWS 自动 Scale 带宽)
        - Supported 1000’s of connections (最多支持 1000 个连接, 也就是说支持 1000 个 VPC + On-Prem 的互联)
    - Disadvantage:
        - Hourly charges per attachments in addition to data fees (不仅 data 要收费, 每个连接本身固定要收费)
        - Max bandwidth burst to 50 Gbps (每个 VPC 之间互相通信的带宽上限是 50Gbps)
        - Infra-region security groups don’t support Transit Gateway (如果用 VPC Peering, 一个 VPC 上的 security group 是可以定义另一个 VPC 的访问的, 而 Transit Gateway 则不行)

Ref:

- https://aimlessengineer.com/2021/08/19/vpc-peering-vs-transit-gateway/
- https://d1.awsstatic.com/whitepapers/building-a-scalable-and-secure-multi-vpc-aws-network-infrastructure.pdf