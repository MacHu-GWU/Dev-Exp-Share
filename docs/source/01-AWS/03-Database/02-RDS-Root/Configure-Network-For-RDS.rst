Configure Network For RDS
==============================================================================

为数据库配网络的活对于没有做过运维的人来说, 非常晦涩难懂, 我也是花了很多时间才彻底弄懂在 AWS 上怎么给数据库配网络.

AWS 的网络安全服务是 VPC, 里面的内容非常多, 我尽量在不涉及 VPC 的细节的情况下, 说明白怎么给数据库配网络.

**理解数据库应该允许哪些网络访问**:

1. 首先数据库肯定不能允许从公网随意访问, 更加不能将公网的 IP 地址公开.
2. App 访问数据库应该是从私网内部访问, 也就是说 APP 和 数据库 需要在一个私网环境下. AWS 中私网的定义是 VPC. 而私网中能与公网通信的子网叫做 Public Subnets, 私网中只能与内部通信的子网叫做 Private Subnets. 很显然, App 服务器需要放在 Public Subnets, 因为需要被公众所访问, 而 数据库服务器 需要放在 Private Subnets.
3. 开发者偶尔需要从本地的开发电脑连接数据库, 通常有两种办法:
    1. 先 SSH 到一台位于私网的 Jumphost 电脑上, 然后再从该电脑连接数据库.
    2. 将本地的开发电脑的 IP 地址加入到数据库服务器的白名单里. 该方法不推荐在生产环境中使用.

下面我们来一步步从头配置 RDS 的网络.

**首先, 配置 VPC**:

1. 进入 VPC Dashboard, 选择 Create VPC Wizard.
2. 选择 VPC with Public and Private Subnets, 这也是最常用的网络配置.
3. 为你的 VPC 配置一个 Elastic IP (在 VPC 主菜单里), 作为你的公网固定 IP 地址. 点击确定.

**为 VPC 配置 Security Group**:

位于 VPC 上的 EC2 可能会有不同的用途, 根据用途, 允许的网络访问模式也会不相同. 所以 AWS 通过设置一批在 VPC 下的 Security Group, 分别定义详细的网络访问规则. 然后给不同的 EC2 指定 Security Group. 对于数据库, 如果是 Postgres, 我们需要为 Inbound 打开 TCP/IP 的 5432 端口, 允许外部访问该端口. 而 Outbound 则不用做任何限制.

Create VPC Wizard 会自动给你创建一个默认的 Security Group, 但我们需要自己创建一个专门为 Postgres 数据库服务的 Security Group, 以和其他 EC2 区分开.

1. 点击 Create Security Group 创建 Security Group, 指定名字, VPC 就好.
2. 拖到下面, 选择 Edit Inbound Rule, 点击 Add Rule, 选择 Type 为 PostgreSQL, 填写 VPC CIDP (Wizard 默认会用 10.0.0.0/16).

**创建 RDS**:

在创建数据库之前, 先要配置 **Database Security Group**, 以用于之后将 Database 所在的 EC2 和 VPC 中的 Subnet 连接起来:

1. 在 RDS 的 Dashboard 中, 选择 Subnet groups, 选择 Create DB Subnet Group.
2. 选择你的 VPC, 以及至少两个位于不同 AZ 的 Private Subnets.

然后, 创建数据库实例:

 1. 在最后一步, Advance Configuration 中, 指定 VPC, 至少两个位于不同 AZ 的 Private Subnets, 以及前面设置的 VPC Security Group (注意, 这里不是 Database Subnet Group), 以及刚刚创建的 DB Subnet Group.


到这里整个 RDS 的配置就结束了, 从 VPC 的内部, 例如位于 Public Subnet 的 EC2, Private Subnet 的 Lambda Function 都可以访问数据库了.

在整个过程中, 我们接触到了许多新的概念, 我现在把他们都列出来, 你还能回忆起来它们的概念都是什么吗?

1. VPC (重要)
2. VPC Subnet, Private Subnet, Public Subnet (重要)
3. Internet Gateway
4. NAT Gateway (重要)
5. Route Table
6. VPC Security Group
7. DB Subnet Group

