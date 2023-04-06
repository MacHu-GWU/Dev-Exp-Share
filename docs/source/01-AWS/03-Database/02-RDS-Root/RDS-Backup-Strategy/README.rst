RDS Backup Strategy
==============================================================================


Scheduled backup 原理
------------------------------------------------------------------------------
Scheduled backup 指的是你定时对数据库进行备份, 使得你能将数据库恢复到备份时的状态.

数据库的底层数据是储存在磁盘上的, 对数据库的备份的实体实质上是对磁盘的快照 Snapshot. 只要有了 Snapshot, 恢复数据库是非常容易的. 但是要注意的是, Snapshot 是对整个磁盘的一份快照, 只记录了备份瞬间的状态, 它不是增量备份, 所以你无法恢复到过去的任意时间点.


Point in time backup 原理
------------------------------------------------------------------------------
PIT 备份指的是你能恢复到




Incremental Backup 原理
------------------------------------------------------------------------------
AWS 允许你将 Snapshot 导出为 S3, 然后你就可以将 S3 object 拷贝到其他的 Account 或是 region, 然后恢复数据库了.

- `start_export_task <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/start_export_task.html>`_: 将 snapshot 导出到 S3.
- `describe_export_tasks <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_export_tasks.html>`_: 获取导出任务的状态, 运行中, 失败了, 成功了.


Reference:

- `Backing up and restoring <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html>`_: RDS 官方文档中关于备份的部分.
- `Restoring from a DB snapshot <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_RestoreFromSnapshot.html>`_: 从 DB snapshot 恢复数据库.
- `Exporting DB snapshot data to Amazon S3 <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html>`_: 将 DB snapshot 导出为 S3.


Copy Snapshot to the Same Account But different Region
------------------------------------------------------------------------------

Share Snapshot to Another Account and the Same Region
------------------------------------------------------------------------------
这里有个坑! Target Account 必须要有访问 Source Account 的 KMS key 的权限才能拷贝, 因为 Snapshot 是加密的. 而如果 Source Snapshot 是用的 default KMS key, 那么你就无法分享这个 snapshot 到其他的 Account. 这是因为你无法修改 default KMS key 的权限. 这时候你可以现将这个 snapshot 在 Source Account 中拷贝一份, 拷贝的时候选择用一个 customer managed KMS key, 然后就可以分享了.

Reference:

- `How can I share an encrypted Amazon RDS DB snapshot with another account? <https://repost.aws/knowledge-center/share-encrypted-rds-snapshot-kms-key>`_: 如何将加密的 snapshot 分享给其他 account?
- `How can I change the encryption key used by my Amazon RDS DB instances and DB snapshots? <https://repost.aws/knowledge-center/update-encryption-key-rds>`_: 如何修改 snapshot 上 用于加密的 KMS key?


Share Snapshot to Another Account and Different Region
------------------------------------------------------------------------------
先用 ``Share Snapshot to Another Account and the Same Region`` 一节中的方法将 Snapshot share 到新的 Account, 然后在新的 Account 中再拷贝到其他的 Region
