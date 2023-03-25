Amazon Machine Image (AMI) Management
==============================================================================


What is AMI
------------------------------------------------------------------------------
AMI 是 Amazon Machine Image 的简称, 简单来说 AMI 就是一个虚拟机的镜像, 也是我们常用的虚拟机软件 VM 的 VM Image. 而 Image 实际上是一个虚拟机在字节级别上完全的复制并压缩, 对于 AMI 来说这个字节级别上完全的复制的底层是 snapshot, 而对于别的虚拟化软件例如 VMware 来说有不同的文件格式.

我们在启动一个 EC2 时, 需要选择一个 AMI (镜像) 以及选择一个 EBS 作为硬盘,

AMI 的构建工具:

- packer
- AWS EC2 image build

AMI 的管理方法有:

- EC2 AMI registry
- S3 (将 AMI 导出备份到 S3)


AMI, Snapshot, EBS 之间的关系
------------------------------------------------------------------------------
AMI 本质上是一个抽象概念, 它的底层是 Snapshot, 而 Snapshot 是 EBS 的一个快照. 如果你不理解快照技术, 你可以这么简单的理解下. EBS 以 4KB 为一个 block (实际上可以从 512B 到 64KB 不等, 我们用 4KB 举例), 而一个硬盘在更改的时候你不需要记录整个硬盘的值, 而只需要记录发生更改的 block 就好了. snapshot 就是记录了硬盘当前状态的 block 的索引, 而不是实际的数据, 实际的数据还保存在 AWS 的数据中心里. 有这个 Snapshot, 将数据复制一份是非常容易的.

当你创建 EC2 的时候, 它需要 mount 一个 EBS, 而这个 EBS 则是根据 Snapshot 生成的, 你可以将这里的 EBS 理解成 Snapshot 的实例. 当然 EBS 本身是块存储的一个服务, 只是在这个例子中你可以这么理解.

你在删除 AMI 的时候其实只删除了 Metadata, snapshot 并不会默认删除. 有了 snapshot, 你可以随时恢复 AMI. 另外 snapshot 可以堆叠到 EC2 中, 相当于 EC2 中的磁盘的 "一层", 堆叠的时候就是从 snapshot 创建一个 EBS mount 上去.


