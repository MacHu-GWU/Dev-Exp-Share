.. _vm-virtualization-type:

Virtual Machine Virtualization Type
==============================================================================
在云时代, 将实体硬件资源切割成小块分发给用户的核心技术就是虚拟化. 这里有计算虚拟化, 网络虚拟化, 存储虚拟化. 而计算虚拟化又分 VM 虚拟机技术和 Container 容器技术. 例如 AWS EC2 就是 VM 虚拟机技术. 本文讨论的是 VM 虚拟机技术.


Overview
------------------------------------------------------------------------------
虚拟机实现方式历史其实非常悠久, 从 1990 年开始到 2015 年云时代已经发展了 25 年了, 主要有 HVM, PV, PV on HVM 三类虚拟机的实现方式:

- **HVM**: Hardware assisted Virtual Machine. 也叫全虚拟化, EC2 的主力虚拟化方式. 全虚拟化或者叫硬件协助的虚拟化技术使用物理机CPU的虚拟化扩展来虚拟出虚拟机. 全虚拟化技术需要Intel VT或者AMD-V硬件扩展. Xen使用Qemu来仿真PC硬件, 包括BIOS, IDE硬盘控制器, VGA图形适配器(显卡), USB控制器, 网络适配器(网卡)等. 虚拟机硬件扩展被用来提高仿真的性能. 全虚拟化虚拟机不需要任何的内核支持. 这意味着, Windows操作系统可以作为Xen的全虚拟化虚拟机使用(众所周知, 除了微软没有谁可以修改Windows内核). 由于使用了仿真技术, 通常来说全虚拟化虚拟机运行效果要逊于半虚拟化虚拟机.
- **Paravirtualization (PV)**: 也叫半虚拟化. 半虚拟化是由Xen引入的高效和轻量的虚拟化技术, 随后被其他虚拟化平台采用. 半虚拟化技术不需要物理机CPU含有虚拟化扩展. 但是, 要使虚拟机能够高效的运行在没有仿真或者虚拟仿真的硬件上, 半虚拟化技术需要一个Xen-PV-enabled内核和PV驱动. 可喜的是, Linux, NetBSD, FreeBSD和OpenSolaris都提供了Xen-PV-enabled内核. Linux内核从2.6.24版本起就使用了Linux pvops框架来支持Xen. 这意味着半虚拟化技术可以在绝大多数的Liunx发行版上工作(除了那么内核很古老的发行版). 关于半虚拟化技术的更多信息可以参考 `维基百科 <https://wiki.xenproject.org/wiki/Paravirtualization_(PV)>`_
- **PV on HVM**: 为了提高性能, 全虚拟化虚拟机也可以使用一些特殊的半虚拟化设备驱动 (PVHVM 或者 PV-on-HVM驱动). 这些半虚拟化驱动针对全虚拟化环境进行了优化并对磁盘和网络IO仿真进行分流, 从而得到一个类似于或优于半虚拟化虚拟机性能的全虚拟化虚拟机. 这意味着, 你可以对只支持全虚拟化技术的操作系统进行优化, 比如Windows.

2006 年 Linux 发布了内核版本 2.6.20, 该版本发布了基于内核的虚拟机技术 KVM (Kernel based Virtual Machine.

Reference:

- - `Linux AMI virtualization types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/virtualization_types.html>`_: AWS 的官方文档, 介绍了 HVM 和 PV 两种技术的比较
- `What is KVM <https://www.redhat.com/zh/topics/virtualization/what-is-KVM>`_: 介绍了 Kernel Virtual Machine 虚拟机技术.


AWS Nitro
------------------------------------------------------------------------------
AWS Nitro 是 2017 年发布的一项 AWS 专属的虚拟化技术. 它和现有的虚拟化技术的本质区别是, 现有的虚拟化技术都是要在宿主机器上运行一些组件, 即使这些组件非常底层, 但是还是要占用宿主机的资源. 无论怎么优化宿主机器, 本质上都是要在宿主机上运行软件. 而 Nitro 则是从根上出发, 把虚拟化的程序做到了专用硬件中, 然后直接插在机器的 PCI 总线上, 把宿主机几乎 100% 的资源都交给了用户. 这项技术原本是一家以色列公司开发的, AWS 将其收购之后在此基础上进行了改进, 从而成为了 AWS Nitro.

- `AWS Nitro 架构简介 <https://zhuanlan.zhihu.com/p/270522703>`_: 详细拆解 AWS Nitro 的架构.
- `一文带你了解AWS Nitro System <https://cloud.tencent.com/developer/article/1852632>`_
- `看 AWS 如何通过 Nitro System 构建竞争优势 <https://www.cnblogs.com/jmilkfan-fanguiju/p/16228459.html>`_
