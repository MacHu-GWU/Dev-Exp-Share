.. _aws-vpc-connectivity-options:

VPC Connectivity Options
==============================================================================

Ref:

- Introduction: https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/introduction.html
- Network-to-Amazon VPC connectivity options (从非 AWS 的网络环境连接 VPC): https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/network-to-amazon-vpc-connectivity-options.html
- Amazon VPC-to-Amazon VPC connectivity options (VPC 到 VPC 之间的连接, 可以跨 Account, 跨 Region): https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html
- Software remote access-to-Amazon VPC connectivity options (软件到 VPC 之间的连接, 通常这个软件是运行在非 AWS 环境中的, 如果已经运行在 AWS 环境中就是上面这个情况了): https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/software-remote-access-to-amazon-vpc-connectivity-options.html
- Transit VPC option (以上三种都是点对点的连接, 复杂度为 O(N*N) 在点多了的时候不 Scale, 而 Transit VPC 是一个中心化的桥梁, 连接以上所有的网络, 复杂度为 O(N)): https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/transit-vpc-option.html