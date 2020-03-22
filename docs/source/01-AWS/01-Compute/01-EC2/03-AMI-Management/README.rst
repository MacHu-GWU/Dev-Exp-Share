Amazon Machine Image (AMI) Management
==============================================================================

AMI 是 Amazon Machine Image 的简称, 简单来说 AMI 就是一个虚拟机的镜像, 也是我们常用的虚拟机软件 VM 的 VM Image.

而 Image 实际上是一个虚拟机在字节级别上完全的复制并压缩.

我们在启动一个 EC2 时, 需要选择一个 AMI (镜像) 以及选择一个 EBS 作为硬盘.

AMI 的构建:

- packer
- aws image build

AMI 的管理:

- EC2 AMI registry
- s3
