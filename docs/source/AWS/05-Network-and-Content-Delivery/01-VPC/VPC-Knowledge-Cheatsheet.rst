VPC Knowledge Cheatsheet
==============================================================================

- 一个 VPC 只能位于一个 Region. 不能同时跨越多个 Region.
- 可以在多个 Region 上部署

- Public Subnet 和 Private Subnet 是逻辑意义上的概念. Subnet 本身没有 Private 和 Public 的属性.
- Public Subnet 还是 Private Subnet 由 Route Table 决定. Destination = 0.0.0.0/0 路由到 Internet Gateway 的是 Public Subnet, Destination = 0.0.0.0/0 路由到 Nat Gateway 的是 Private Subnet.


- 一个 VPC 必须有至少一个 Main Route Table.
- 没有跟任何 Route Table 关联的 Subnet 自动使用 Main Route Table 的设置.
- 由于默认会使用 Main Route Table 的设置, 而出于安全考虑, 我们希望默认的 Subnet 是私有的. 所以通常 Main Route Table 的设置是为 Private Subnet 服务的.
- 位于 Main Route Table 的设置通常是为 Private Subnet 服务, 所以我们需要手动将 Public Subnet 跟 Secondary Route Table 相关联.

VPC Peering:

- VPC Peering 解决的是 位于不同 VPC 中的 Private Subnet 中的机器互相通信的问题.
- VPC 与 私有数据中心 的连接 不用 VPC Peering, 而是用 Direct Connect.
- VPC Peering 是点对点关系, 也就是 已有 A - B, B - C, 但 A - C 不会自动 Peering. 如果你需要 A 中的设备能跟 C 中的通信, 则需要单独为 A, C 建立 Peering
- VPC Peering 可以跨越 Region.
- VPC Peering 之后, Private 之间的通信用的是 Private IP.
- VPC Peering 之后, 各自的 VPC 跟外网通信, 依旧只能用自己的 Internet Gateway / NAT Gateway, 不能使用 Peered 的 VPC 的.

VPC Endpoint:

- VPC Endpoint 解决的是让位于 VPC 内部的机器不通过 Internet Gateway, Nat Gateway, Direct Connect, 直接通过 Private Link Endpoint 访问其他 AWS 资源.
- 两种类型: Interface Endpoint (有 IP 地址的, 例如 EC2 Cloudformation, Cloudwatch), Gateway
- VPC Endpoint 常用于让其他人直接访问 S3, DynamoDB.

相关文献:

- Multiple Region Multi-VPC Connectivity: https://aws.amazon.com/answers/networking/aws-multiple-region-multi-vpc-connectivity/
- Single Region Multi-VPC Connectivity: https://aws.amazon.com/answers/networking/aws-single-region-multi-vpc-connectivity/

HTTPS:

- 要让 HTTPS 通信成功, 对于 Network ACL, inbound 需要是 443, outbound 则要允许 1024 - 65535, outbound 只允许 443 是不够的.

VPC DNS:

- DNS hostname vs DNS resolution: 默认情况下 VPC 是没有 hostname 的, 所以你 VPC 里的 EC2 也没有 DNS name. 当你在 VPC Action -> DNS hostname 中设置了 DNS 域名到 Elastic IP 的对应关系之后, 就可以用了. DNS resolution 是 Amazon DNS Server 解析域名的操作名称.
-