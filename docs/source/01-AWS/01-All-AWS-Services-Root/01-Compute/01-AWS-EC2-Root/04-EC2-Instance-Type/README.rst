EC2 Instance Type
==============================================================================
Keywords: AWS EC2 Instance Type


Overview
------------------------------------------------------------------------------
AWS 的 EC2 在所有云服务提供商提供的虚拟机产品线中, 可选的类型是最多的.

- `Cloud comparison: AWS EC2 vs Azure Virtual Machines vs Google Compute Engine <https://acloudguru.com/blog/engineering/cloud-comparison-aws-ec2-vs-azure-virtual-machines-vs-google-compute-engine>`_: 比较了三大云服务提供商的虚拟机产品线.


Instance Type
------------------------------------------------------------------------------
AWS EC2 Instance Type 的命名是有规律的, 一般是 ``${前缀}${第几代}${后缀}`` 这样的形式.

- 前缀: 一般是字母, 也可能是单词, 决定了大类别.
- 第几代: 一般是数字, 数字越大就越新.
- 后缀: 大类别下的小类别, 一般指的是优化方向.

我们以最常用的 T 系列为例. T 系列是 General Purpose 类型, 也就是通用型, 是 Burstable 的类型 (高负载时可以 burst 到更高的性能). 从 t2 开始, 到 t3, t3a, t4g. t3 就是 t2 的下一代, 什么都不说就一般指的是 X64 架构, 也一般是 Intel 的芯片. t3a 里的 a 指的是 AMD 芯片. 一般其他型号相同, 有 a 的会便宜个 10%. 而 t4g 则是 ARM 架构, 以功耗比高为买点, 一般会便宜个 20%, 甚至 40%. 由于是用的 Graviton 这种专门的 ARM 芯片, 所以名字是 g.

我们总结一下:

- 前缀:
    - General Purpose:
        - T: burstable
        - M: 很多机器
- 后缀:
    - a: AMD processors
    - g: AWS Graviton processors, ARM 芯片
    - i: Intel processors
    - d: Instance store volumes, 除了 EBS 之外, 自己本身就带磁盘
    - n: Network optimization
    - b: Block storage optimization
    - e: Extra storage or memory
    - z: High frequency, 单核超高频率

Instance Type Naming Convention:

- a: AMD processors (AMD 的芯片)
- g: AWS Graviton processors (ARM) 架构
- i: Intel processors
- d: Instance store volumes
- n: Network optimization
- b: Block storage optimization
- e: Extra storage or memory
- z: High frequency

按照不同用途分类:

- General Purpose:
    - Burstable performance: t4g, t3a, t3, t2
- Compute Optimized:
    - c5, c5n:
    - c6g, c6gd, c6gn:
    - c6i, c6id:
    - c6in:
    - hpc6a:
- Memory Optimized:
    - R5, R5a, R5b, R5n:
    - R6a:
    - Hpc6id:
    - R6g, R6gd:
    - R6i, R6id:
    - R6in, R6idn:
    - u-*:
    - etc ...
- Storage Optimized:
    - d2:
    - d3, d3en:

按照不同用途分类的中文版:

- A/T/M: general purpose, 普通目的. A 是 Arm, T 是比较常用的个人电脑级别, 内存一般不超过 32G, M 是服务器级, 高性能, 内存可以高达 384 G.
- C: compute optimized, 高性能计算. 适合用于游戏服务器, 高性能 Web 服务器, 图像视频转码等.
- R/X: memory optimized, 高内存. 适合用于缓存服务器, 比如 Redis, Memorycache
- P: accelerated computing, 硬件加速高性能计算. 适合用于密码加密解密, 大量浮点运算.
- H/I/D: storage optimized, 存储性能优化. 适合用作数据库服务器, 高性能随机读写.

Reference:

- `EC2 Instance Type Look up <https://aws.amazon.com/ec2/instance-types/>`_: 表格化的 EC2 Type 速查, 可以按分类查看每个 Type 的 vCPU, Memory, Network Bandwidth, EBS Bandwidth 信息.
- `EC2 Instance Type Document <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_: 对 EC2 Type 的详细介绍文档, 包括每个 Type family 的介绍.
- `Amazon EC2 On-Demand Pricing <https://aws.amazon.com/ec2/pricing/on-demand/>`_: 按需付费的价格表.
- `Amazon EC2 Spot Instances <https://aws.amazon.com/ec2/spot/>`_: 空闲虚拟机的价格表.
- `Amazon EC2 Reserved Instances Pricing <https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/>`_: 长期合同的折扣价格表.
- `Amazon EC2 Dedicated Hosts Pricing <https://aws.amazon.com/ec2/dedicated-hosts/pricing/>`_: 专属部署的价格表.


Root Device Type
------------------------------------------------------------------------------
存储方式:

- **EBS**: EC2 主力存储方式, 使用弹性块作为存储方式, 原理上是将高性能的存储集群上的 volume 映射到 EC2 上的某个目录, 然后使用内部的高性能连接和虚拟机进行通信. **EBS 是有3 份冗余的, 而且在虚拟机关闭后, 你可以选择不删除 EBS 上的数据, 而且 EBS 上的数据可以被很容易的 Mount 到其他的 EC2 上, 或是 detach**.
- **Instance store**: 使用虚拟机的宿主上的磁盘空间作为存储方式, **很显然宿主上的存储是没有冗余的, 如果出错或丢失了, 就永久无法恢复. 而虚拟机一旦被 terminate, 数据就会全部丢失**.