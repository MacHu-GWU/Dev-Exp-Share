Managing your storage lifecycle
==============================================================================

Overview
------------------------------------------------------------------------------
Lifecycle 顾名思义就是生命周期, 说的是一个 S3 object 是有其生命周期的, 在到达生命周期的不同阶段的时候, 自动改变它的 Storage class. 不同的

Reference:

- `Managing your storage lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>`_
- `Supported transitions and related constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html#lifecycle-general-considerations-transition-sc>`_: 不是所有的 Storage class 都可以互相转化, 这篇文档介绍了哪些 Transition 是允许的.
- `Lifecycle and other bucket configurations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-and-other-bucket-config.html>`_: 这篇文档介绍饿了 Lifecycle configuration 和其他的 S3 configuration, 例如 versioning, MFA, logging 等是如何联动的.
- `Lifecycle configuration elements <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_: 介绍了 LifeCycle configuration 到底怎么写.
