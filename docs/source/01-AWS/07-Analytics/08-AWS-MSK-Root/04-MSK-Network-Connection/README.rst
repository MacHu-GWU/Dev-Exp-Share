.. _aws-msk-network-connection:

MSK Network Connection
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

.. _aws-msk-network-connection-summary:

1. Summary
------------------------------------------------------------------------------
你要跟 MSK 进行通信, 不管是调用 MSK API, 还是调用 Kafka API, 还是 Data Read / Write, 你都要满足网络连接的条件. 如果你没有网络连接的条件, 无论你有多高的 MSK 权限你都无法跟 MSK 进行通信.

谈到跟 MSK 通信, 总会有一个 Client 机器发起通信的 Request, 或者接受 MSK 的 Response. 这个 Client 可以按照所处的网络进行如下分类.

- 位于跟 MSK 同一个 VPC 内
- 位于跟 MSK 同一个 AWS Account / Region, 不同的 VPC
- 位于跟 MSK 同一个 AWS Account, 不同的 Region
- 跟 MSK 不同的 AWS Account
- 位于 On-prem
- 位于 SAAS 服务提供商的服务器所在网络

本文我们想讨论对于基于以上所有情况已有的 Client, 我们应该怎样配置网络使其能跟 MSK 通信. 并且延伸讨论对于未来的新的 Client, 基于我们设计的基础设施, 如何最快最简单的接入已有的网络.


2. Challenges
------------------------------------------------------------------------------


.. _aws-msk-network-connection-options:


3. Options
------------------------------------------------------------------------------
本章我们介绍目前 AWS 提供了哪些选择用于组网.


4. Solutions
------------------------------------------------------------------------------
本章针对 aws-msk-network-connection-summary_ 中提到的问题, 结合 aws-msk-network-connection-options_ 中给出的选择, 一一给出解决方案.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


4.1 位于跟 MSK 同一个 VPC 内
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Client 处于同一个 VPC 下, Public / Private Subnet 皆可.
- 参考 :ref:`aws-vpc-security-group-best-practice-default-security-group`, 给 MSK 和 Client 相同的 Default Security Group.


4.2 位于跟 MSK 同一个 AWS Account / Region, 不同的 VPC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 为 MSK VPC 和 Client VPC 创建 VPC Peering, 记得更新 Route Table.
- VPC Peering 的多个 VPC 互相之间 CIDR Block 不能重叠.
- VPC Peering 支持位于不同的 AWS Account, 以及不同的 AWS Region.
- Client 处于自己 VPC 下, , Public / Private Subnet 皆可.
- 你无法给 VPC A 中的资源 Attach 一个来自于 VPC B 的 SG. 解决方法如下:
- 根据 `这篇文档 <https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html>`_ 你可以给 VPC A 中的资源 attach 一个 VPC A 的 SG, 其中 rule 允许来自于 VPC B 的 SG ID 的 Traffic, 只要他们是同一个 Account, Region.


4.3 位于跟 MSK 同一个 AWS Account, 不同的 Region
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 为 MSK VPC 和 Client VPC 创建 VPC Peering.
- Client 处于自己 VPC 下, , Public / Private Subnet 皆可.
- 你无法给 VPC A 中的资源 Attach 一个来自于 VPC B 的 SG. 解决方法如下:
- 根据 `这篇文档 <https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html>`_ 你无法给 VPC A 中的资源 attach 一个 VPC A 的 SG, 其中 rule 允许来自于 VPC B 的 SG ID 的 Traffic, 因为你无法 Reference 位于另一个 Region 的 SG, 即使他们是同一个 Account. 但是你可以在 Reference 里定义 VPC B 的 CIDR Block.


4.4 跟 MSK 不同的 AWS Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 为 MSK VPC 和 Client VPC 创建 VPC Peering.
- Client 处于自己 VPC 下, , Public / Private Subnet 皆可.
- 你无法给 VPC A 中的资源 Attach 一个来自于 VPC B 的 SG. 解决方法如下:
- 根据 `这篇文档 <https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html>`_ 你可以给 VPC A 中的资源 attach 一个 VPC A 的 SG, 其中 rule 允许来自于另一个 Account 的 VPC B 的 SG ID 的 Traffic, 要注意你的 Reference Id 的格式要是 ``${12digits_account_id}/sg-1a2b3c4d``.


4.5 位于 On-prem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 为 On-prem 和 AWS 之间拉一条 Direct Connect 专线, 使得 On-prem 和 AWS 之间的通信不走公网, 速度跟 AWS 之间内部通信一样快.
- 单独开一个 AWS Account 作为 Transit Account, 并创建一个 Transit Gateway (TGW). TGW 跟 On-prem 连接, 定义好路由. 所有其他的 AWS Account 的 VPC 也跟 TGW 连接. 并更新路由. 这样所有的连接到 Transit Gateway 的网络就可以互联了, 并且可以用 Route Table 随时开关网络之间的连接.
- Update MSK 的 Security Group, 把允许的 Reference 设为用于运行 App 的 VPC 的 CIDR Block.
- 从 On-prem 对 MSK bootstrap endpoint 发起的连接会被 TGW 所处理.


4.6 位于 SAAS 服务提供商的服务器所在网络
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

