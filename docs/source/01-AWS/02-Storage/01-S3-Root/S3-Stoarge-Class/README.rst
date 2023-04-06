Using Amazon S3 Storage Classes
==============================================================================
Keywords: Amazon AWS S3 Storage Class, Standard, IA, Infrequent Access, Archive, Lifecycle.


Storage Classes Summary
------------------------------------------------------------------------------
S3 storage classes 是一种针对不同的使用需求, 采用不同的存储策略的功能. 这些不同的策略会在下面这几个维度上有所不同:

- 存储的费用
- 数据读写的费用
- 数据读取的速度 (延迟)
- 数据的 availability (数据并不会丢, 但是可能会有时候不可用)
- 数据的 durability (数据会不会丢)

简单来说, 你存储的费用越低, 代价就是你读的时候更贵, 同时读取的速度更慢. 例如热数据一般用 Standard, 读写很快, 存储最贵. 如果不常用数据一般用 Infrequent Access (IA), 存比较便宜, 读比较贵. 如果是长期储存用的归档数据, 一般用 Archive (归档) 那么存储最便宜, 但是有可能读的时候要几个小时准备数据, 读取的时候也比较贵.

到 2023-03-25 为止, 有这么几种 Storage class 的选项:

- S3 Standard: 标准
- Reduced Redundancy: 数据可能会丢, 官方不推荐, 请谨慎使用
- S3 Intelligent-Tiering: 自动根据数据多久没用了改变 Storage Class, 有 Frequent Access, Infrequent Access, Archive Instant Access 三种 IA 类型的 class, 还有 Archive Access, Deep Archive Access 两种 archive 类型的 Class.
- IA:
    - S3 Standard-IA: 存储便宜, 读取收费贵
    - S3 One Zone-IA: 存储更便宜, 但是只在一个 Availability Zone 有备份, 虽然数据肯定不会丢, 但是 availability 会低一些.
- Archive:
    - S3 Glacier Instant Retrieval: 读取的时候立刻就能读到, 无需等待
    - S3 Glacier Flexible Retrieval: 最少存 90 天不能改变 (可以读), 如果 overwrite 了就会收 90 天的费用
    - S3 Glacier Deep Archive: 最少存 180 天不能改变 (可以读), 如果 overwrite 了就会收 180 天的费用

值得注意的事, 读取 Archive 的数据有三种方式:

- Expedited: 快速读取, 价格最贵, 等待时间最短, 大约 1 - 5 分钟
- Standard: 标准读取, 价格中等, 等待时间较短, 大约 3 - 5 小时
- Bulk: 批量读取, 最便宜, 但是等待时间也最长, 可能会需要 5 - 24 小时.

Reference:

- `Amazon S3 Storage Classes <https://aws.amazon.com/s3/storage-classes/>`_: 关于 Storage Class 的信息汇总的官方文档.
- `Using Amazon S3 storage classes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html>`_: 关于 Storage Class 的详细技术文档.
- `Archive retrieval options <https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html>`_: 关于从 Archive Storage class 中读取数据的几种方式的介绍.


Managing your storage lifecycle
------------------------------------------------------------------------------
Storage LifeCycle 是一种规定了一个 Object 在何种情况下, 自动转变成何种 Storage Class 的功能. 例如, 你可以规定一个数据创建后的 30 天内是 Standard, 30 - 90 天自动变为 IA, 90 天后自动变为 Archive. 这个跟 Intelligent-Tiering 的功能有点类似, 但是 Intelligent-Tiering 是自动的, 且判定依据是这个数据在多少天内没有被读过, 而 Storage LifeCycle 是手动的, 判定依据是这个数据创建了多少天.

这里有很多知识点, 我们这里不展开讨论, 只列出了重要的知识点:

- `Transitioning objects <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html>`_: S3 有这么多 Storage Class, 不是每一个 Storage Class 相互之间都能 transition 的, 你可以到官方文档查看哪些是允许的, 哪些是不允许的.
- `LifeCycle Configuration Element <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_: LifeCycle Configuration 是一个 XML 文件. 有一些关键的 Tag 例如 Rule, Filter (决定了对哪些 object 生效), Transition (决定了什么时候 transition 以及变成什么 storage class).

Reference:

- `Managing your storage lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>`_: 介绍 Storage lifecycle 的详细技术文档.
- `Examples of S3 Lifecycle configuration <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html>`_: LifeCycle Configuration 的一些例子.
