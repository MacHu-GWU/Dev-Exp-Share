VPC For Human
==============================================================================

- VPC
- Subnet
- Elastic IPs
- Route Tables
- Internet Gateway
- Network Address Transition

为了帮助大家理解, 假设我们是淘宝, 我们有一个淘宝网站的服务器, 后台有一个数据库. 我们需要怎样配置我们的网络, 来保证服务器和数据库的性能和安全呢?

首先, 大众是需要访问网站服务器, 所以网站服务器需要能从公网访问到.



用 VPC 搭建公网私网架构
------------------------------------------------------------------------------

**用 VPC Wizard 创建 VPC**:

1. 进入 VPC Dashboard, 选择 Create VPC Wizard.
2. 选择 VPC with Public and Private Subnets, 这也是最常用的网络配置.
3. 为你的 VPC 配置一个 Elastic IP (在 VPC 主菜单里), 作为你的公网固定 IP 地址. 点击确定.

默认情况下 Wizard 只会为你的 VPC 分别配置 1 个 Public 和 Private 的 Subnet, IP 地址分别是 10.0.0.0/16 和 10.0.1.0/16. 基本上大部分的数据库服务都要求部署在至少 2 个 Availability Zone 上, 意味着私网至少需要 2 个 Subnets.

这里的 Public 和 Private Subnets 是逻辑意义上的 Subnets. 使用 Internet Gateways 和 Elastic IP 访问公网. 而 Private Subnets 通过 NAT Gateway 访问公网.

**Wizard 为你创建的资源**:

1. 1 个 VPC, 跟指定的 EIP 相连. 该 EIP 无法被其他 VPC 使用.
2. 2 个默认的 Subnet, 1 个 Public, 1 个 Private.
3. 1 个 Internet Gateway 跟你的 VPC 相连.
4. 1 个 主要的 Route Table, 跟你的 VPC 相连. 为 Public Subnets 服务.
5. 1 个 主要的 VPC Security Group. 定义了网络通信 Inbound 和 Outbound 的规则.

查看一下 VPC, 你的 VPC 的公网 IP 是 EIP, 私网 IP 是 IPV4 CIDR, 默认是 10.0.0.0/16.

查看一下 Route Table, 一共有两个 Route Table:

Route Table 1, main table, 为 NAT 服务:

- Destination = 10.0.0.0/16, Target = local: 所有要去 10.0.0.0/16 的请求, 发送给此 VPC.
- Destination = 0.0.0.0/0, Target = nat-088a299b91dda0db1: 所有要去其他地方的请求, 发送给 NAT Gateway.

Route Table 1, main table, 为 Internet Gateway 服务:

- Destination = 10.0.0.0/16, Target = local: 所有要去 10.0.0.0/16 的请求, 发送给此 VPC.
- Destination = 0.0.0.0/0, Target = igw-070f42a0791741850: 所有要去其他地方的请求, 发送给 NAT Gateway.

位于 Private Subnets 上的数据库服务器想从公网下载更新补丁:

1. 向 NAT Gateway 发起请求.
2. NAT Gateway 通过 Internet Gateway 下载补丁包, 下载完毕后传给数据库服务器.

这里

**添加 Private Subnet**:

前面提到过, 大部分的数据库服务出于容错的考虑, 至少需要连接 2 个以上的 Subnets (防止一个网络挂掉, 导致数据库不可用)

1. 进入 VPC -> Subnets, 点击 Create Subnets.
2. 指定我们之前创建的 VPC, 选择一个与之前不同的 Availability Zone, 设置 IPv4 CIDR Block, 建议使用奇数作为 Private Subnet, 偶数作为 Public Subnet. 所以我们使用 10.0.3.0/16.


理解 CIDR Block
------------------------------------------------------------------------------
10.10.1.148/32 指的是 10.10.1.148 这一具体的 IP 地址.
10.10.1.0/28 指的是 10.10.1.0 - 10.10.1.15 之间的全部 IP 地址.
