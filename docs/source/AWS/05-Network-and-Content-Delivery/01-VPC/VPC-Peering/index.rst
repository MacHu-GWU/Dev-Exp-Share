VPC Peering
==============================================================================

假如我们有两个 IP 地址, Route Table 要怎么做才能让上面的机器互相通信呢?

- VPC A: 10.10.0.0/16
- VPC B: 10.11.0.0/16

VPC A 的 Route 里要有一个 Destination 是 B 的地址, VPC B 的 Route 里要有一个 Destination 是 A 的地址,

- VPC A Route Table: destination 10.11.1.0/28, target 10.11.0.0/16
- VPC B Route Table: destination 10.10.1.0/24, target 10.10.0.0/16
