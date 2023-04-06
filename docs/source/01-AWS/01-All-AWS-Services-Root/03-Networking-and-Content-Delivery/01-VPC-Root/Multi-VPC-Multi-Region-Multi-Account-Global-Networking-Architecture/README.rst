.. _multi-vpc-region-account-global-networking-architecture:

Multi VPC Multi Region Multi Account Global Networking Architecture
==============================================================================


Overview
------------------------------------------------------------------------------
VPC 是 AWS 中的核心网络服务, 用于企业组建内部网络. 一个 VPC 是位于一个 AWS Account 上的某个具体的 Region 的. 在企业应用中, 随着业务复杂度的不同, 可能有如下需求 (按照从简单到难排序):

- 只有云网络, 只有一个 VPC, 没有自建的数据中心 (on-prem).
- 有 VPC 也有自建的数据中心, 两者需要通信.
- 在一个 Account 一个 Region 上有多个 VPC.
- 在多个 Account 一个 Region 上有多个 VPC.
- 在一个 Account 多个 Region 上有多个 VPC (跨 region).
- 在多个 Account 多个 Region 上有多个 VPC (global).
- 在多个 Account 多个 Region 上有多个 VPC, 以及位于世界不同位置的多个自建数据中心.

本文是一个综述性的文章, 在以上的问题的大框架下, 介绍了如何为复杂多变的业务需求在 AWS 上组网的总体思路.


AWS Networking Services
------------------------------------------------------------------------------
我们先简单了解一下 AWS 有哪些与网络相关的服务:

- VPC (Virtual Private Cloud): 云上虚拟私有网络. 免除了企业自己搭建私有网络基础设置的麻烦. 是 AWS 网络的核心
- Direct Connect: 跟合作的 ISP (Internet Service Provider) 在你的 On-Prem 和 AWS 之间拉一条专线. 使得所有 On-Prem 与 AWS 之间的网络通信不经过公网, 不仅保障了隐私, 而且提高了速度, 使得 On-Prem 和 AWS 之间的通信速度和 AWS 内部之间的通信速度一样快.
- VPC Peering: 将多个 VPC 两两连接起来, 使得多个 VPC 的 Subnet 互相能直接通信. 默认情况下两个不同的 VPC 私网之间是无法通信的. 该服务是通过两两连接实现的多个 VPC 互联, 在有 N 个 VPC 的时候复杂度是 O(N).
- Transit Gateway: 为多个 VPC 以及 On-Prem 提供一个中心化的网关将他们连接起来. 这是 VPC Peering 的升级版, 在 VPC 数量增多的时候为最优解. 当然也更复杂, 更贵.
- VPC Endpoint: 为位于 VPC 内的计算资源例如 EC2 和 AWS 服务之间建立私有连接. 以 S3 为例, 使得 API 请求不走公网的 Endpoint, 而是走私网的 Endpoint, 使得 Traffic 不经过公网, 不仅保障了隐私, 而且提高了速度.
- Client VPN Endpoint: 为企业中的个人用户的电脑提供从任何地方通过 VPN 访问 VPC 的服务. 连上了 VPN 后就相当于已经在 VPC 里面了.

- Network-to-Amazon VPC connectivity options: https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/network-to-amazon-vpc-connectivity-options.html
- Building a global network using AWS Transit Gateway Inter-Region peering: https://aws.amazon.com/blogs/networking-and-content-delivery/building-a-global-network-using-aws-transit-gateway-inter-region-peering/