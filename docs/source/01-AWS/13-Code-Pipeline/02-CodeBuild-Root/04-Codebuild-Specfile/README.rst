AWS Codebuild Build Spec File Reference
==============================================================================



Regular Build Spec File Reference
------------------------------------------------------------------------------


Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cache 功能可以将文件或者文件夹缓存起来, 以供之后的 Build job 使用.

例如对于 Python 开发者而言, 你可以将 Python 的 ``site-packages`` 目录缓存起来. 这样之后 ``pip install requirements.txt`` 的时候很多依赖都已经被安装过了, 可以节约大量时间.

例如对于 Docker image build 的项目, Layer 也可以被缓存起来以增加构建速度.

每次 Run build job 的时候, 在执行 Phase 之前这些缓存就会被下载并解压, 并覆盖已有的文件. 而每次执行完 build job 之后, 会把自动将 Cache 所监视的文件与之前构建的 Cache 进行比对, 并进行更新. 所以下一次 build 的时候就可以用到最新的 Cache 了.

Cache 的本质是一个 Git 文件系统, 维护了 metadata, fingerprint, 以及 simlink 的指针. 由于使用了 Git 文件系统来监控里面包含的文件, 所以每次 Cache 所监视的文件发生变化, 构建新的 Cache 只会发生在哪些变化的文件上, 从而获得非常好的增量更新性能. 而对于 S3 而言就是一个打包的 zip 压缩包, 解压后就是一堆 Git 文件系统的索引以及文件包, 并不是跟你 Cache 所对应的目录一样的文件树结构.

Ref:

- Buildspec reference: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html, 搜索 ``cache/paths`` 关键字
- Build caching in AWS CodeBuild: https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html


Batch Build Spec File Reference
------------------------------------------------------------------------------
