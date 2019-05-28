VPC Security Group vs Network Access Control List
==============================================================================

- Security Group:
    - 作用于具体的 Entity, 例如 EC2, RDS
    - Stateful: 也就是连接一旦建立, 那么就无视 Security Group 的其他规则. 例如: 外部发起请求访问位于 SG 内的 EC2, 如果 Inbound 允许了, 那么请求就会被成功建立, 哪怕 Outbound 规则不允许, 但是由于请求是由外部发起的, 则通信还是依然可以进行. 从内部发起的请求同理.
- Network Access Control List:
    - 作用于 VPC Subnet
    - Stateless: 请求 和 响应 都要受到 Network ACL 的限制. 只要有一个不允许就不行. Network ACL 的 Rule 有序号的概念, 从小到大依次 Evaluate

