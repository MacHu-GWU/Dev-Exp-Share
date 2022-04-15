.. _aws-vpc-peering:

VPC Peering
==============================================================================
Keyword: AWS VPC Peering, Peer

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


简介
------------------------------------------------------------------------------
VPC 内部之间是可以通过路由通信的. 但是两个不同的 VPC 之间是无法直接通过路由通信的. 要想把两个 VPC 当成一个 VPC 用, AWS 的解决方案是 `VPC Peering <https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html>`_ (`Transit Gateway <https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html>`_ 是更高级的解决方案, 这里先不做介绍)

Ref:

- https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html


多个 VPC 之间互联
------------------------------------------------------------------------------
VPC Peering 不支持自动桥接, 你如果想要两个 VPC 能通信, 必须直接为这两个 VPC 建立 VPC Peering. 例如你有 A - B, B - C, 但是 AC 没有 Peering, 你是不能让 A 和 C 直接通信的.


为 VPC Peering 配置路由
------------------------------------------------------------------------------
假如我们有两个 IP 地址, Route Table 要怎么做才能让上面的机器互相通信呢? 假设有这两个 VPC.

- VPC A: 10.10.0.0/16
- VPC B: 10.11.0.0/16

你需要满足 VPC A 的 Route 里要有一个 Destination 是 B 的地址, VPC B 的 Route 里要有一个 Destination 是 A 的地址. 这个 target 一般是 VPC 的全部 CIDR, 但是 destination 只是部分的 CIDR, 这取决于你要连接的应用. 例如 A 上是 Web App, 要跟 B 上的 Relational Database 通信, 那么这个 destination 的 CIDR 就是在 B 上的 Database 所用到的 CIDR Block. 具体例子如下:

- VPC A Route Table: destination 10.11.1.0/28, target 10.11.0.0/16
- VPC B Route Table: destination 10.10.1.0/24, target 10.10.0.0/16


常见的坑
------------------------------------------------------------------------------
- 所有的 VPC 之间的 CIDR Block 不能有 Overlap, 不然一旦 Peer 到一起, 路由无法知道这个 IP 地址到底是属于哪个 VPC 的.
- 你需要为你的 IAM User 的添加 `特定的权限 <https://docs.aws.amazon.com/vpc/latest/peering/security-iam.html>`_ 才能创建 Peering.
- 你从 A 创建了一个到 B 的 Peering 的请求后, 你需要在 B 接受这个请求才算 Peering 成功.
- VPC Peering 可以跨 Region.
