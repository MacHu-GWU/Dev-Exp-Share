.. _aws-redshift-knowledge-graph:

AWS Redshift Knowledge Graph
==============================================================================
本文把 AWS Redshift 数据仓库的知识点按照逻辑顺序梳理了一遍. 不涉及任何知识细节, 只是对知识的归纳总结.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is AWS Redshift
------------------------------------------------------------------------------

What is:

- 是 AWS 云原生 Data Warehouse 数据仓库 应用. Red 暗指 Oracle 红色的 logo, 对标取代 Oracle 的数据仓库方案.
- 提供对 PB 级的数据的高性能查询. 查询语法使用 SQL.
- 完全由 AWS 托管, 维护, 备份, 免除了运维的麻烦, 只需要几下点击, 15 分钟内就可以启用 AWS Redshift Data Warehouse.

Why:

- 业界领先的数据仓库, 稳定性, 可用性, 性能, 效率, 管理, 易用性, 安全性 全方位领先
- 多种权限管理模式, IAM Role 模式, User Password 模式. 细粒度的数据访问权限管理, database / table / column / row 级别的管理.


AWS Redshift Architect
------------------------------------------------------------------------------
- 分布式架构:
    - Redshift 是一个典型的 主/从 分布式系统.
    - 有 Leader Node 负责 管理集群, 路由查询, 汇总数据 等工作. Computer Node 负责储存数据, 执行 query. 无论是 Leader 还是 Computer node 都有冗余设计, 不存在单点故障, 数据也有备份. 一个 Node 就是一个有独立 CPU, 内存, 磁盘的 VM 虚拟机 EC2.
    - sharding 机制叫做 slice, 每个 node 都会被 partition 成很多个 slice. 通常一个 slice 就是一个 CPU, 也是最小的计算处理单元. Leader Node 会将数据路由到具体的 slice 上做处理.
- 网络:
    - Redshift 集群需要被部署到 VPC 上, 但是在 VPC 内部 Redshift 在物理上会被部署到靠近的位置, 并且用超高性能网络连接, 所有 Node 间的数据传输都是内网. 而备份和冗余则通过网络备份到其他的 AZ 和 Region.
- 管理:
    - Redshift 在系统管理上基于 Postgres 修改而来,
- 性能:
    - 在硬件层使用 Massively parallel processing (MPP) 向量化的指令集 CPU, 使得并行处理的性能极强.
- 存储:
    - 存储层使用 columnar 列式存储, 并且数据都采用了高性能的压缩算法, 同时又不牺牲查询性能.
    - 列式存储的基本单位是大小为 1MB 的 block, 数据都会被编码为高性能的二进制格式, 每个 block 上只储存一个 column 中多个行的数据, 每个 block 会有数据的统计信息, 比如最大最小值, 这些统计信息可以用来提高查询性能, 避免扫描不必要的数据.
- 计算:
    - 每个查询都会经过针对 列式存储 分布式架构 高度优化的 query optimizer.
    - 特定的查询结果会被缓存在 leader node 的内存中以提高整体 cluster 性能.
    - SQL 查询会在 leader node 上被 query optimizer compile 成 byte code 再发送给 computer node 执行.
- WLM (work load management):
    - 允许用户对并发查询进行管理, 防止单个查询占用过多系统资源, 对多个查询任务指定有限级, 从而保持整个系统的高可用性和稳定性.


Manager Cluster
------------------------------------------------------------------------------
- Create Cluster
    - Redshift 和 RDS 很像, 在管理层面上都是一个数据库.
    - 和 RDS 类似, 需要被部署到 VPC 以内, 有 Public accessible 和 Non public accessible 两种模式, Public accessible 通常是 dev 环境, 通常放在 public subnet 上, 靠 Security group 防止未授权的 IP 访问. Non public accessible 通常是 prod 环境, 通常放在 private subnet 上, 只能从 VPC 内部访问.
    - 和 RDS 类似, 都需要 database subnet group 以及 security group
- Connect to Cluster
    - 连接到 Redshift 集群需要满足两个条件: 网络条件, 你的网络能 reach out Redshift 集群, 以及 Security group 允许你的连接. 用户权限, 你使用的 database user 或是 IAM role 要有足够的权限. 两者缺一不可.
    - Redshift 有非常精细化的 permission management 的机制, 也是分为 principal, resource, action (谁, 能对什么, 干什么) 三个部分. 同时有 user group 的概念能批量管理权限.
- Manage Cluster
    - 维护 Redshift 大部分工作是自动的, 比如: 对数据和磁盘进行清理 VACUUM, 对软件升级, 对操作系统打补丁, 定期备份.
    - 监控集群性能的工作也是自动的, AWS Cloudwatch 能对 CPU, 内存, 磁盘, 网络, 延迟, Query 性能进行自动监控.
    - 数据备份默认是 1 天一次, 你也可以手动或者用 lambda 进行自动增量备份. 关于 snapshot 和 backup 的原理可以参考 :ref:`backup-and-snapshot`


User Management
------------------------------------------------------------------------------
- 数据权限管理主要有三个核心概念 principal, resource, action (谁, 能对什么, 干什么)
- Redshift 支持 User / User Group / IAM Role 三种 principal
- Redshift 支持 Cluster / Database / Schema / Table or View / Column 这几种 resource
- Redshift 支持 Select / Insert / Update / Delete / Reference 以及很多非数据的, 系统管理性质的 action
- 推荐不要直接给 User 任何权限, 而是给 User Group 权限, 然后把 User 放到不同的 User Group 中进行管理. 这里的 User Group 等价于 IAM User Group, 也等价于 Lake Formation 中的 Tag
- View 是数据访问权限管理利器, 你可以用 Subquery 来创建一个 View, 然后只给用户这个 View 的权限, 从而实现非常细粒度的数据访问权限管理


Table Design
------------------------------------------------------------------------------
- Column compression: 由于使用了列式存储, 所以对不同的 column 采用不同的压缩手段能减少磁盘用量, 还能提高查询性能.
    - AZ64
    - Byte-dictionary
    - Delta
    - LZO
    - Mostly
    - Run Length
    - Text255 / Text32k
    - ZSTD
- Data distribution style (distribution key): 由于是分布式系统, 所以需要一个 distribution key 来决定由哪个 slice 来处理数据
    - distribution style 有 KEY / EVEN / ALL / AUTO 四种. 一个 Table 只能有一个 distribution column
- Data sort keys: 可以指定一个或者多个 sort key 让数据在存储前就排序好, 这样能大幅增加 JOIN, ORDER BY, WHERE 等查询性能
    - 有 compound sort key 和 interleaved sort key 两种方式


Load Data
------------------------------------------------------------------------------
- 用 COPY 命令从 S3 中读取数据是最高效的.
- 数据最好预先压缩过. 每个文件大小为 1 ~ 128 MB 比较合适.
- 用 manifest, 使用一个 COPY 命令同时并行读取多个文件的效率要远远高于使用多个并发 COPY 命令对单个文件进行读取.
- COPY 数据时 manifest 内部的的顺序是预先外排序过的能避免 VACUUM, 提高吞吐量. COPY 本身会做文件内部的内排序, 而多个文件之间的外排序如果你在执行命令的时候就排序好了这样是最好的.


Unload Data
------------------------------------------------------------------------------


Query Data
------------------------------------------------------------------------------
