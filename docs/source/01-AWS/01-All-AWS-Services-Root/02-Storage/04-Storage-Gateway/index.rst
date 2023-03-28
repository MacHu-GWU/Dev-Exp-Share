.. _aws-storage-gateway:

AWS Storage Gateway Docs
==============================================================================

简单来说, Storage Gateway 就是一个将用户的电脑和 AWS 的其他存储服务 (S3, EBS, EFS) 连接起来的服务. VTL (Virtual Tape Library) 是虚拟化的备份服务. 相当于以前的工作电脑备份软件. 在你的电脑上安装一个 Client, 然后将电脑数据备份到 AWS 上.

在过去, 企业数据备份通常是用 Tape (磁条机), 因为 Tape 便宜, 存放的时间久, 可以容错, 单位体积可存放的数据多. Storage Gateway 就是在 Console 里设置一个 VTL, 然后在用户机器上装客户端, 就可以持续的将数据备份到 AWS 上了.



