VPC Flow Log
==============================================================================

**What are VPC Flow log?**

VPC Flow logs is a feature that enables you to capture information about the IP traffic going to and from network interface in your VPC

简单来说就是 VPC 的网络流量日志. 它是 VPC 的一个功能, 允许你将日志输出到 Cloudwatch 和 S3 Bucket. 界面在你的 VPC 里, 选中你的 VPC, 下面就会出现一个 Flow Log 的菜单.

VPC Flow Log 可以作用于 VPC, Subnet, Network Interface 级别.

**What are they use for?**

1. To troubleshould why specific traffic is not reaching an instance
2. To diagnose overly restrictive security gorup rules
3. Uses as a security tool to monitor the traffic that is reaching your instances with a VPC
