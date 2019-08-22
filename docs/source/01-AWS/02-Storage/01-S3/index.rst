S3
==============================================================================

Concept:

- Bucket
- Object
    - Key
    - Metadata
- Storage Classes
    - S3 Standard
    - Standard IA (Infrequence Access)
    - One Zone IA
    - Glacier

Features:

- Version
    - 你开启了 Version 后,
- Object Lifecycle Management
    - 定期删除, 或者移到更低的 Storage Class.
- Access Control List and Bucket Policy
    - `Access Control List <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html>`_: 作用于 Bucket Level, 常用于允许其他 AWS Account 的 User 访问该 Bucket.
    - Bucket Policy: 对 Bucket 中的 Object 进行精细的控制. 比如说对某个 Prefix 下的所有 Object, 对于特定的用户, 用户组, IP, 允许 / 拒绝 某一个, 某一组操作.