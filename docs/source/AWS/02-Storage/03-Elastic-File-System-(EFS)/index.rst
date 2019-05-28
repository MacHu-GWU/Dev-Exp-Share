Elastic File System
==============================================================================

一句话解释 EFS 的作用: 给 EC2 提供文件系统, 更重要的是, 给多个 EC2 提供 共享文件系统. 而一个 EBS 卷只能挂载到一个 EC2 上.

- EFS 的作用是给 VPC 内的 EC2 提供文件系统.
- 必须为 EFS 指定 VPC 配合使用.
- 必须为 EFS 指定 Mount Target.
- 每一个 AZ 可以创建一个 Mount Target.
- 如果一个 AZ 上有多个 Subnet, 可以在其中一个 Subnet 上创建一个 Mount Target. 所有在当前 AZ 上的 EC2 都共享使用同一个 Mount Target.
- AWS 建议为每一个 AZ 都创建一个 Mount Target. 因为 在一个 AZ 上的 EC2 访问另一个 AZ 上的 Mount Target 价格很贵.
- 位于同一个 Region 下的两个 VPC 可以通过使用 VPC Peering 来共享访问一个 EFS. 不同一个 Region 的不行.
- EFS 有专用的 Network File System Port, 而 EC2 本身受到 Security Group 的限制, 所以 Security Group 设置不当可能会导致 EC2 无法访问 EFS.
- EFS 的加密分两种, 存储加密和传输加密. 存储加密只能在创建 EFS 的时候启用. 传输加密则不是 EFS 本身的功能, 需要在启动 EC2 时使用 EFS Mount Helper, 断开再重新挂载同一个 EFS 即可使得传输加密生效, https://docs.aws.amazon.com/efs/latest/ug/encryption.html#encryption-in-transit
- Performance Mode 有两种: General 和 Max IO. Max IO 是给 几十个上百个 EC2 分享同一个 EFS 时用的, 延迟高一些. General 比较快, 但是 IO 的容量不是特别大.
- Throughput Mode 有两种: Burst 和 Provisioned, Burst 是大多数时间很普通, 5MB/s, 一天能有 18 分钟提供 100MB/S 的速度. Provisioned 适用于 100MB ~ 1TB /S 级别的速度.




EFS vs EBS
------------------------------------------------------------------------------

- Reference: https://dzone.com/articles/confused-by-aws-storage-options-s3-ebs-amp-efs-explained
- EBS, 块存储, 文件被分为 64KB 大小的块存储.
- EFS, 一个完整的 NTFS 文件系统.

