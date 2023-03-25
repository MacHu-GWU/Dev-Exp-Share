AMI Backup Strategy
==============================================================================
Keywords: Amazon Machine Image, AMI, Backup, Restore, VM.

AMI 是 EC2 的底层镜像, 记录了 EC2 的磁盘每个比特的状态. 有了 AMI, 恢复 EC2 是非常容易的. 你可以理解为 AMI 在 EC2 在, AMI 没了 EC2 就没了, 课件 AMI 的重要.

要想备份 AMI, AWS 提供了三种方法:

1. 复制到同一个账号下的其他 Region: 该方法相当于是在其他 Region 生成一个新的 AMI. 但你无法跨 Account 复制.
2. 将 AMI 导出为 S3 上的单个 Object: 该方法最为推荐, 本质是将 Snapshot 进行压缩后保存在 S3 上, 而且是单个文件. 美中不足的是只能指定 S3 bucket, 不能指定 S3 prefix. 导出导入的速度都很快. 有这么几个相关的 API:
    - `create_store_image_task <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_store_image_task.html#>`_: 创建 AMI 备份.
    - `describe_store_image_tasks <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_store_image_tasks.html#>`_: 查看备份工作的运行状态, 还在运行, 失败了, 还是成功了.
    - `create_restore_image_task <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_restore_image_task.html#>`_: 从备份恢复 AMI.
3. 将 AMI 导出为 VM 文件: 该方法的目的是将 VM 文件拿到 on-prem 里用 VM 软件从 AMI 的导出启动虚拟机, 如果你还是要在 AWS 上启动这个 EC2, 那么你不应该考虑该方法. 这里有个坑, 你照着 `Required permissions for VM Import/Export <https://docs.aws.amazon.com/vm-import/latest/userguide/required-permissions.html>`_ 和 `How do I use VM Import/Export to export a VM based on my Amazon Machine Image (AMI)? <https://aws.amazon.com/premiumsupport/knowledge-center/ec2-export-vm-using-import-export/>`_ 两篇文档配好了权限之后, 你一定要完完全全按照文档里的来, IAM Role name, 与 bucket 相关的 IAM policy 部分, 就用 root folder, 千万不要自己加 prefix, 以及导出的时候在 API 里要填 ``exports/`` 作为 S3 prefix, 不然会出错.

还有的一种常见的方法是从 instance 不关机直接导出, 但是这种方法不推荐. 因为你完全可以将 EC2 instance 导出成为 AMI, 然后再用上面的方法备份, 会灵活的多.

Reference:

- `Store and restore an AMI using S3 <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ami-store-restore.html>`_: 介绍了如何用 S3 来备份 AMI.
- `Required permissions for VM Import/Export <https://docs.aws.amazon.com/vm-import/latest/userguide/required-permissions.html>`_:  介绍了将 Image 导出为 VM 镜像的权限, 这个文档很重要, 但也很 tricky.
- `How do I use VM Import/Export to export a VM based on my Amazon Machine Image (AMI)? <https://aws.amazon.com/premiumsupport/knowledge-center/ec2-export-vm-using-import-export/>`_: 介绍了如何将 Image 导出为 VM 镜像.
