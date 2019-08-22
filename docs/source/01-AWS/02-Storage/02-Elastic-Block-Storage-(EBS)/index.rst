.. _s3-ebs:

Elastic Block Storage
==============================================================================


Volume Type
------------------------------------------------------------------------------

数据卷灵活配置的虚拟移动硬盘, 可以将任何容量的硬盘, 挂载到任何机器上, 只需要几分钟时间. EBS 通常和 EC2 一起使用.

SSD (固态硬盘):

- EBS General Purpose SSD (gp2): 普通电脑的硬盘
- EBS Provisioned IOPS SSD (io1): IO 密集型, 例如数据库应用

HDD (磁碟机硬盘):

- Cold HDD (sc1): for large data that is infrequently accessed
- Throughput Optimized HDD (st1): IO 密集型, streaming workload,

Reference:

- Volume Type: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html


Encryption
------------------------------------------------------------------------------

- EBS 使用 KMS 进行 Encryption at rest.
- 只有在创建 Volume 的时候可以启动 Encryption, 创建后无法启动.
- 只有部分 EC2 Instance Type 可以支持 Encryption (通常是那些高性能的).
- 由于 RDS 实际上运行在 EC2 上, 也挂载了 EBS, 所以对数据库数据加密的原理, 和对 EBS 加密的原理实际上是一样的.

Following types of data are encrypted:

- Data at rest inside the volume
- All data moving between the volume and the instance
- All snapshots created from the volume
- All volumes created from those snapshots

Reference:

- Amazon EBS Encryption: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html
