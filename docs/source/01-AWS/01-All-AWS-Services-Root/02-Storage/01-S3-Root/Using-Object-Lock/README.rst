Using Object Lock
==============================================================================
Keywords: AWS, S3, Object, Lock


Summary
------------------------------------------------------------------------------
有些监管行业需要保证你存储层满组 write-once-read-many (WORM) model. 即数据一旦被写入, 一定时间内 (或永久) 就不能被修改和删除.

注意:

- 这个功能只能在创建 Bucket 的时候打开. 不能在已有的 Bucket 上打开. 而且你必须在创建 Bucket 的时候开启 Object Versioning.

Reference:

- `Using S3 Object Lock <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html>`_


Retention Modes
------------------------------------------------------------------------------
Retention modes 是一个非常重要的概念. 目前 Object Lock 支持两种 retention modes:

- governance mode: users can't overwrite or delete an object version or alter its lock settings unless they have special permissions. With governance mode, you protect objects against being deleted by most users, but you can still grant some users permission to alter the retention settings or delete the object if necessary. You can also use governance mode to test retention-period settings before creating a compliance-mode retention period.
- compliance mode: a protected object version can't be overwritten or deleted by any user, including the root user in your AWS account. When an object is locked in compliance mode, its retention mode can't be changed, and its retention period can't be shortened. Compliance mode helps ensure that an object version can't be overwritten or deleted for the duration of the retention period.

简单来说 governance (监管) 模式就是说大部分人都改不了, 除非有特殊的 IAM 权限. 而 compliance (合规) 模式就是所有人都改不了, 包括开启这个模式的本人, 也包括 AWS Account Root User.
