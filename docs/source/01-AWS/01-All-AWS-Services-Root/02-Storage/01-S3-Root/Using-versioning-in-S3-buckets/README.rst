Using versioning in S3 buckets
==============================================================================
keywords: AWS, S3, Bucket, Object, Version, Versioning.


Summary
------------------------------------------------------------------------------
Versioning 是 AWS S3 中的一个功能, 可以让保留 Object 的所有修改历史, 并且在删除的时候也是用的软删除, 只是将其标记为已删除, 而所有的数据都还在. 这个功能在一些例如网盘, 文件历史等场景中非常有用. 配合上 Life Cycle 功能, 可以实现自动将旧数据或是已被标记为删除的数据转移到低成本的存储中, 或是直接删除.

Reference:

- `Using versioning in S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html>`_

下面是一些我自己写的博文和代码示例:

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    Using-Versioning-in-S3-Bucket.ipynb
