Bastion Host (壁垒主机)
==============================================================================

通常是指一台位于 VPC Public Subnet 的机器, 允许开发者 SSH 到该机器上, 然后通过该机器访问 位于 Private Subnet 上的资源.

Bastion Host 通常是给人用的, 不是给机器用的. 比如说, Web App 服务器通常位于 VPC Public Subnet, Web App 就根本不需要 Bastion Host.
