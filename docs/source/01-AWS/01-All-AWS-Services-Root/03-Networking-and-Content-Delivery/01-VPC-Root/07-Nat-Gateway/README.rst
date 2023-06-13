.. _aws-vpc-nat-devices:

AWS VPC Nat Devices, Nat Gateways and Nat Instances
==============================================================================
Keywords: AWS VPC Nat Device, Gateway, Instance


Overview
------------------------------------------------------------------------------
Nat Devices 是一类用于使得位于私网中的设备能访问公网的设备. Nat Devices 这一名词不是 AWS 专有, 而是网络工程中历史悠久的技术之一. 主要用来解决 IPV4 地址不够用的问题. 简单来说就是既然不可能给每个私网的设备分配一个公网 IP, 那么就可以让整个私网只用一个公网 IP, 然后内部可以有几百万个地址 (16M). 然后位于私网的设备对外访问的时候都通过 Nat Devices 进行代理, 然后 Nat Devices 对外只用公网 IP, 并且记录这个请求和私网 IP 的映射关系. 我推荐先阅读以下两篇博文, 对 Nat 有一个基本的了解.

Reference:

- `NAT转换是怎么工作的？ <https://www.zhihu.com/question/31332694>`_
- `什么是NAT？ <https://info.support.huawei.com/info-finder/encyclopedia/zh/NAT.html>`_

由于 Nat Devices 本质上是一个路由器硬件设备. 既然是硬件设备, 自己维护就必然存在硬件坏掉, 维护, 替换等问题, 很难做到高可用. 更不用说还有流量的高峰低谷问题, 设备多了浪费钱, 设备少了带宽不够. 而 AWS 将这个硬件设备给虚拟化了, 从而让客户能够轻松的配置商用的私有网络. 具体的做法也不神秘, 本质上就是 AWS 维护着一个巨大的 Nat 设备池子, 整个 AWS 数据中心里有非常多网路中继节点, 而每一个中继节点都是一个高可用的集群, 而每个集群里都有非常多的 Nat 设备, 每个 Nat 设备都负责不止一个 AWS 用户的 VPC. 每个 AWS 用户的 VPC 在每个中继节点都至少有 3 个 Nat 设备正在为其服务. 从客户的角度, 实现了高可用. 从 AWS 的角度, 实现了最大化的对每个 Nat 设备的利用 (多租户).


Nat Gateways vs Nat Instances
------------------------------------------------------------------------------
AWS 提供了两种 Nat 设备, Nat Gateway 和 Nat Instances. Nat Gateways 是一个服务, 点点鼠标就能给客户分配一个或多个高可用, 高带宽的 Nat 设备. 而 Nat Instances 则是一个预装了 Nat 软件的 EC2 AMI 镜像, 从而让用户能自己用虚拟机搭建一个 Nat Devices, 但这样你就需要自己维护冗余, 实现高可用了, 显然不是那么容易.

明显 Nat Gateway 更方便, 所以它也是用户的主流选择之一.


Nat Gateway and VPC
------------------------------------------------------------------------------
单个 Nat Gateway 默认是 5Gbps 的带宽, 并能自动 Scale 到 100Gbps. 如果 100Gbps 还不够, AWS 推荐将你的私网分为多个 Private Subnet, 然后给每一个 Private Subnet 配一个 Nat Gateway (通常在路由表中一个 Private Subnet 只能配一个 Nat Gateway, 虽然你可以在 Private Subnet 的 CIDR 网段再自己分, 但是没有必要, 非常不好维护). 因为 Nat Gateway 每处理 1Gb 数据就是 0.045 美元, 而 100Gbps 运行一小时就是 $16,200, 一天就是 $388,800, 一个月就是 $11,664,000, 一个月一千多万美元的网费, 这已经非常夸张了. 更加常见的情况是一个公司里有 3 个 Private Subnet, 分别位于 3 个不同的 AZ, 然后配 3 个 Nat Gateway, 这样让流量更加平稳.


Reference
------------------------------------------------------------------------------
- `Nat Devices <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat.html>`_
- `Nat gateways <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html>`_
- `Nat instances <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html>`_
