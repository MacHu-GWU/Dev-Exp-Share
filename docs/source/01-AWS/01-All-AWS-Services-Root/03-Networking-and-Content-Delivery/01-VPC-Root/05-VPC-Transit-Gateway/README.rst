.. _aws-vpc-transit-gateway:

VPC Transit Gateway
==============================================================================

Ref:

- Network-to-Amazon VPC connectivity options: https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/network-to-amazon-vpc-connectivity-options.html
- Building a global network using AWS Transit Gateway Inter-Region peering: https://aws.amazon.com/blogs/networking-and-content-delivery/building-a-global-network-using-aws-transit-gateway-inter-region-peering/


FAQ
------------------------------------------------------------------------------
**General**

- Q: How do I control which Amazon Virtual Private Clouds (VPCs) can communicate with each other?

    You can segment your network by creating multiple route tables in an AWS Transit Gateway and associate Amazon VPCs and VPNs to them. This will allow you to create isolated networks inside an AWS Transit Gateway similar to virtual routing and forwarding (VRFs) in traditional networks. The AWS Transit Gateway will have a default route table. The use of multiple route tables is optional.

    - 在 Transit Gateway 的 Route Table 定义对 Destination 的请求要被 Route 到哪里去.
    - Transit Gateway 是一个独立的服务, 无需放置在 VPC 之中.

- Q: How does routing work in AWS Transit Gateway?

    AWS Transit Gateway supports dynamic and static routing between attached Amazon VPCs and VPNs. By default, Amazon VPCs, VPNs, Direct Connect gateways, Transit Gateway Connect and peered Transit Gateways are associated to the default route table. You can create additional route tables and associate Amazon VPCs, Direct Connect gateways, VPNs, Transit Gateway Connect and peered Transit Gateways with it.

    The routes decide the next hop depending on the destination IP address of the packet. Routes can point to an Amazon VPC or a VPN connection, or a Direct Connect gateway, or a Transit Gateway Connect, or a peered Transit Gateway.

- Q: How are routes propagated into the AWS Transit Gateway?

    There are 2 ways that routes get propagated in the AWS Transit Gateway:

    Routes propagated to/from on-premises networks: When you connect VPN or Direct Connect Gateway, routes will propagate between the AWS Transit Gateway and your on-premises router using Border Gateway Protocol (BGP).
    Routes Propagated to/from Amazon VPCs:  When you attach an Amazon VPC to an AWS Transit Gateway or resize an attached Amazon VPC, the Amazon VPC Classless Inter-Domain Routing (CIDR) will propagate into the AWS Transit Gateway route table using internal APIs (not BGP). CIDR is a method for allocating IP addresses and IP routing to slow the growth of routing tables on routers across the Internet, and to help slow the rapid exhaustion of IPv4 addresses. Routes in the AWS Transit Gateway route table will not be propagated to the Amazon VPC’s route table. The VPC owner needs to create a static route to send Traffic to the AWS Transit Gateway.
    Peering attachments between Transit Gateways do not support route propagation. You need to create static routes in Transit gateway route tables to send traffic on peering attachments.

- Q: Can I connect Amazon VPCs with identical CIDRs?

    AWS Transit Gateway doesn’t support routing between Amazon VPCs with identical CIDRs. If you attach a new Amazon VPC that has a CIDR which is identical to an already attached Amazon VPC, AWS Transit Gateway will not propagate the new Amazon VPC route into the AWS Transit Gateway route table.

    - 请不要给不同的 VPC 相同的 CIDR Block, 即使是 CIDR Overlap 也不行.
    - 如果先后 Attach 到 Transit Gateway 的 VPC 有着相同的 CIDR Block, 那么后来的自动被忽略, 只有第一个 VPC 会被添加到 Route Table 中.

- Q: What is AWS Transit Gateway Connect?

    AWS Transit Gateway Connect is a feature of AWS Transit Gateway. It simplifies the branch connectivity through native integration of SD-WAN (Software-Defined Wide Area Network) network virtual appliances into AWS Transit Gateway. AWS Transit Gateway Connect provides a new logical attachment type called Connect attachment that utilizes the Amazon VPC or AWS Direct Connect attachments as the underlying network transport. It supports standard protocols such as Generic Routing Encapsulation (GRE) and Border Gateway Protocol (BGP) over the Connect attachment.

    没搞懂

- Q: Which AWS partners support AWS Transit Gateway Connect?

    AWS Transit Gateway Connect is supported by a number of leading SD-WAN and Networking partners. Please visit the `Partners <https://aws.amazon.com/transit-gateway/partners/#AWS_Transit_Gateway_Connect_Partners>`_ page for more information.

- Q: What types of appliances work with AWS Transit Gateway Connect?

    Any third-party network appliances that support standard protocols such as GRE and BGP will work with AWS Transit Gateway Connect.

- Q: Can I create Connect attachments with an existing AWS Transit Gateway?

    Yes, you can create Connect attachments on an existing AWS Transit Gateway.

- Q: Does AWS Transit Gateway Connect support static routes?

    No, AWS Transit Gateway Connect does not support static routes. BGP is a minimum requirement.

- Q: Are the BGP sessions established over the GRE tunnel?

    Yes, the BGP sessions are established over the GRE tunnel.

- Q: Can I associate a route table to the Connect attachment?

    Yes, similar to any other Transit Gateway attachments, you can associate a route table to the Connect attachment. This route table can be same/different to that of the VPC or AWS Direct Connect (underlying transport mechanism) attachment’s associated route table.

**Performance and limits**

- Q: What are the default limits or quotas for AWS Transit Gateway?

    Details on limits and quotas can be found in our `documentation <https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-quotas.html>`_.

    Should you need to exceed these limits, please create a support case.

    主要这么几个:

    - 跟 VPC 通信的带宽上限是 50Gbps
    - 你无法在 VPC A 中的 Security Group 定义 Reference 另一个 VPC B 中的 Security Group. 因为这个连接要经过 Transit Gateway, VPC A 收到的 traffic 不会从 VPC B 中来, 自然也无从用 SG 来验证. 如果你想要用 SG 来验证, 请使用 VPC Peering

**Security and compliance**

- Q: With which compliance programs does AWS Transit Gateway conform?

    AWS Transit Gateway inherits compliance from Amazon VPC and meets the standards for PCI DSS Level 1, ISO 9001, ISO 27001, ISO 27017, ISO 27018, SOC 1, SOC 2, SOC 3, FedRAMP Moderate, FedRAMP High and HIPAA eligibility.

**Feature interoperability**

- Q: Does AWS Transit Gateway support IPv6?

    Yes, AWS Transit Gateway supports attaching Amazon VPCs with IPv6 CIDRs.

- Q: Which Amazon VPC features are not supported in the first release?

    Security Group Referencing on Amazon VPC is not supported at launch. Spoke Amazon VPCs cannot reference security groups in other spokes connected to the same AWS Transit Gateway.

- Q: Can I associate my AWS Transit Gateway with a Direct Connect gateway in a different account?

    Yes, you can associate your AWS Transit Gateway with an AWS Direct Connect gateway from a different AWS account. Only the owner of the AWS Transit Gateway can create association to a Direct Connect gateway. You cannot use Resource Access Manager to associate your AWS Transit Gateway with Direct Connect gateway. For more information, please review the AWS Transit Gateway Support section in the Direct Connect FAQs.

- Q: I want to associate my Transit Gateway to a Direct Connect gateway. Can I use the same Autonomous System Number (ASN) for the Direct Connect gateway and the Transit Gateway?

    No, you cannot use the same ASN for the Transit Gateway and the Direct Connect gateway.

- Q: Which attachment types can I use to route multicast traffic?

    You can route multicast traffic within and between VPC attachments to a Transit Gateway. Multicast routing is not supported over AWS Direct Connect, AWS Site-to-Site VPN, and peering attachments.

- Q: Does AWS Transit Gateway Connect supports IPv6?

    Yes, AWS Transit Gateway Connect supports IPv6. You can configure both the GRE tunnel and the Border Gateway Protocol (BGP) addresses with IPv6 addresses.

- Q: Can I use different address families for the GRE tunnel and BGP addresses?

    Yes, you can configure the GRE tunnel and the BGP addresses to be same or different address family. For example, you can configure the GRE tunnel with IPv4 address range and the BGP addresses with IPv6 address range and vice versa.

- Q. Does AWS Transit Gateway support IGMP for multicast?

    Yes, AWS Transit Gateway supports IGMPv2 (Internet Group Management Protocol version 2) for multicast traffic.

- Q. Can I have both IGMP and static members in the same multicast domain?

    Yes you can have both IGMP and static members in the same multicast domain. IGMP-capable members can dynamically join or leave a multicast group by sending IGMPv2 messages. You can add or remove static members to a multicast group using console, CLI or SDK.

- Q. Can I share a Transit Gateway for multicast?

    Yes you can use AWS Resource Access Manager (RAM) to share a transit gateway multicast domain for VPC subnet associations across accounts or across your organization in AWS Organizations.

Ref:

- https://aws.amazon.com/transit-gateway/faqs/