.. _aws-ebs:

AWS Elastic Block Storage (EBS) Docs
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


EBS and EC2
------------------------------------------------------------------------------

EC2 必定有一个 Root Device. 而 EC2 的启动方式有两种:

1. instance store-backed instance: 虚拟机启动时跟虚拟机的 image 所在的盘一起启动作为磁盘. 启动了就不能 stop, 只能 terminate. 一旦 terminate 或者崩溃, 磁盘上的所有数据丢失. 常用于临时扩容, 无状态的机器, 比如 web 服务器.
2. amazon ebs-backed instance: 虚拟机启动时, 挂载 EBS 作为磁盘. 启动之后可以 stop. 并且机器本身和数据相互独立, 机器挂掉了数据可以还在. 并且可以挂掉机器, 用另一个机器 + 原来的 ebs 重新启动. 常用于有状态, 长期存在的机器, 比如 cicd 服务器.

如果你用 CloudFormation 启动 EC2, BlockDeviceMapping 这一属性可以控制用哪种方式启动. 具体请参考: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html

EBS-backed 由于更加常用, 并且更加复杂, 我们详细介绍下使用 EBS-backed 的启动方式时, 如何配置 EBS: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html

Device name 是 EBS 卷在操作系统内的标识符, 这个目录在机器上会被 Linux 系统通过链接的方式拼接到主磁盘. 这与 Linux 的文件系统有关.

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html