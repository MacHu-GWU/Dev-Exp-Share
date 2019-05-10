.. _s3-ebs:

Elastic Block Storage
==============================================================================

数据卷灵活配置的虚拟移动硬盘, 可以将任何容量的硬盘, 挂载到任何机器上, 只需要几分钟时间. EBS 通常和 EC2 一起使用.

SSD (固态硬盘):

- EBS Provisioned IOPS SSD (io1): IO 密集型, 例如数据库应用
- EBS General Purpose SSD (gp2)

HDD (磁碟机硬盘):

- Throughput Optimized HDD (st1): IO 密集型, 例如数据库应用
- Cold HDD (sc1)