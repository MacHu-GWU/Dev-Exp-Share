Lambda Required Security Group
==============================================================================


Access Public Internet from VPC
------------------------------------------------------------------------------

如果 Lambda 需要从 VPC 内部访问公网 (例如爬虫), 则需要在 Security Group 中加入如下设置, **允许 HTTP 和 HTTPS 协议**.

Outbound:

- HTTPS TCP 443 0.0.0.0/0
- HTTPS TCP 443 ::/0
- HTTP TCP 80 0.0.0.0/0
- HTTP TCP 80 ::/0

Inbound 无需设置.


Access AWS API (like Boto3) from VPC
------------------------------------------------------------------------------

如果 Lambda 需要从 VPC 内部访问 S3 API, 则需要在 Security Group 中 **允许 HTTPS 协议**. 这是因为 AWS 的 API 是通过 HTTPS 协议通信的.

Outbound:

- HTTPS TCP 443 0.0.0.0/0
- HTTPS TCP 443 ::/0
