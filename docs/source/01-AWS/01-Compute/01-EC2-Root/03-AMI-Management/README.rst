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


AMI Backup Strategy
------------------------------------------------------------------------------
要想备份 AMI, AWS 提供了三种方法:

- 复制到同一个账号下的其他 Region: 该方法相当于是在其他 Region 生成一个新的 AMI. 但你无法跨 Account 复制.
- 将 AMI 导出为 S3 上的单个 Object: 该方法最为推荐, 本质是将 Snapshot 进行压缩后保存在 S3 上, 而且是单个文件. 美中不足的是只能指定 S3 bucket, 不能指定 S3 prefix. 导出导入的速度都很快. 这里有这么几个 API 会比较重要, ``create_store_image_task``, ``describe_store_image_tasks``, 和 ``create_restore_image_task``, 分别对应了 备份 和 恢复.
- 将 AMI 导出为 VM 文件: 该方法的目的是将 VM 文件拿到 on-prem 里用 VM 软件从 AMI 的导出启动虚拟机, 如果你还是要在 AWS 上启动这个 EC2, 那么你不应该考虑该方法. 这里有个坑, 你照着 `Required permissions for VM Import/Export <https://docs.aws.amazon.com/vm-import/latest/userguide/required-permissions.html>`_ 和 `How do I use VM Import/Export to export a VM based on my Amazon Machine Image (AMI)? <https://aws.amazon.com/premiumsupport/knowledge-center/ec2-export-vm-using-import-export/>`_ 两篇文档配好了权限之后, 你一定要完完全全按照文档里的来, IAM Role name, 与 bucket 相关的 IAM policy 部分, 就用 root folder, 千万不要自己加 prefix, 以及导出的时候在 API 里要填 ``exports/`` 作为 S3 prefix, 不然会出错.

还有的一种常见的方法是从 instance 不关机直接导出, 但是这种方法不推荐. 因为你完全可以将 EC2 instance 导出成为 AMI, 然后再用上面的方法备份, 会灵活的多.

Reference:

- Store and restore an AMI using S3:https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ami-store-restore.html
- Required permissions for VM Import/Export: https://docs.aws.amazon.com/vm-import/latest/userguide/required-permissions.html
- How do I use VM Import/Export to export a VM based on my Amazon Machine Image (AMI)?: https://aws.amazon.com/premiumsupport/knowledge-center/ec2-export-vm-using-import-export/
