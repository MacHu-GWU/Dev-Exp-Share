EC2 Instance Type
==============================================================================

.. contents::
    :depth: 1
    :local:


Virtualization Type
------------------------------------------------------------------------------

主要有 3 类虚拟机的实现方式:

- **HVM**: Hardware assisted Virtual Machine. 也叫全虚拟化, EC2 的主力虚拟化方式. 全虚拟化或者叫硬件协助的虚拟化技术使用物理机CPU的虚拟化扩展来虚拟出虚拟机. 全虚拟化技术需要Intel VT或者AMD-V硬件扩展. Xen使用Qemu来仿真PC硬件, 包括BIOS, IDE硬盘控制器, VGA图形适配器(显卡), USB控制器, 网络适配器(网卡)等. 虚拟机硬件扩展被用来提高仿真的性能. 全虚拟化虚拟机不需要任何的内核支持. 这意味着, Windows操作系统可以作为Xen的全虚拟化虚拟机使用(众所周知, 除了微软没有谁可以修改Windows内核). 由于使用了仿真技术, 通常来说全虚拟化虚拟机运行效果要逊于半虚拟化虚拟机.
- **Paravirtualization (PV)**: 也叫半虚拟化. 半虚拟化是由Xen引入的高效和轻量的虚拟化技术, 随后被其他虚拟化平台采用. 半虚拟化技术不需要物理机CPU含有虚拟化扩展. 但是, 要使虚拟机能够高效的运行在没有仿真或者虚拟仿真的硬件上, 半虚拟化技术需要一个Xen-PV-enabled内核和PV驱动. 可喜的是, Linux, NetBSD, FreeBSD和OpenSolaris都提供了Xen-PV-enabled内核. Linux内核从2.6.24版本起就使用了Linux pvops框架来支持Xen. 这意味着半虚拟化技术可以在绝大多数的Liunx发行版上工作(除了那么内核很古老的发行版). 关于半虚拟化技术的更多信息可以参考维基百科 http://wiki.xenproject.org/wiki/Paravirtualization_(PV
- **PV on HVM**: 为了提高性能, 全虚拟化虚拟机也可以使用一些特殊的半虚拟化设备驱动(PVHVM 或者 PV-on-HVM驱动). 这些半虚拟化驱动针对全虚拟化环境进行了优化并对磁盘和网络IO仿真进行分流, 从而得到一个类似于或优于半虚拟化虚拟机性能的全虚拟化虚拟机. 这意味着, 你可以对只支持全虚拟化技术的操作系统进行优化, 比如Windows.


Root Device Type
------------------------------------------------------------------------------

存储方式:

- **EBS**: EC2 主力存储方式, 使用弹性块作为存储方式, 原理上是将高性能的存储集群上的 volume 映射到 EC2 上的某个目录, 然后使用内部的高性能连接和虚拟机进行通信. **EBS 是有3 份冗余的, 而且在虚拟机关闭后, 你可以选择不删除 EBS 上的数据, 而且 EBS 上的数据可以被很容易的 Mount 到其他的 EC2 上, 或是 detach**.
- **Instance store**: 使用虚拟机的宿主上的磁盘空间作为存储方式, **很显然宿主上的存储是没有冗余的, 如果出错或丢失了, 就永久无法恢复. 而虚拟机一旦被 terminate, 数据就会全部丢失**.


Instance Type
------------------------------------------------------------------------------

亚马逊的专门优化的虚拟机:

- A/T/M: general purpose, 普通目的. A 是 Arm, T 是比较常用的个人电脑级别, 内存一般不超过 32G, M 是服务器级, 高性能, 内存可以高达 384 G.
- C: compute optimized, 高性能计算. 适合用于游戏服务器, 高性能 Web 服务器, 图像视频转码等.
- R/X: memory optimized, 高内存. 适合用于缓存服务器, 比如 Redis, Memorycache
- P: accelerated computing, 硬件加速高性能计算. 适合用于密码加密解密, 大量浮点运算.
- H/I/D: storage optimized, 存储性能优化. 适合用作数据库服务器, 高性能随机读写.

Reference:

- https://aws.amazon.com/ec2/instance-types/
