VPC Network Access Control List (ACL)
==============================================================================

网络控制列表作用于 Subnet 级别, 定义了网络端口的 Inbound 以及 Outbound 的 Rule. 对应于 AWS Resource 级的概念是 Security Group. 两者都是根据 IP 地址和通讯协议进行过滤.

- Network ACL 作用于 Subnet
- Security Group 作用于 EC2, RDS, Lambda, Container

Network ACL 的规则过滤方式跟 Security Group 很不一样. ACL 的规则有一个编号. 当一个网络通信请求发起后, ACL 会按照编号, ``*`` 视为最大, 从小到大进行检查, 如果当前规则跟当前请求不匹配 (不匹配指的是完全无关, 比如规则指定的是 80 端口, 而通信请求是 5000 端口, 而不是指的是拒绝), 则检查下一条规则, 如果当前规则匹配, 则按照规则同意或拒绝. 然后忽略之后的所有规则. 一旦匹配上之后,  如果小号的 Rule 允许, 而大号的 Rule 不允许, 以小号的为准. (参考资料: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-rules)
