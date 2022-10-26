AWS CodeBuild BuildSpec File
==============================================================================



Regular Build Spec File Reference
------------------------------------------------------------------------------


Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cache 功能可以将文件或者文件夹缓存起来, 以供之后的 Build job 使用. 如果有一些需要的文件被正常创建的时间开销要大于通过网络传输的开销, 那么就很适合用 Cache.

AWS CodeBuild 提供了两种 Cache:

- AWS S3: 保存在 S3 中. 可以跨 Build Job 复用.
- Local Cache: 保存在 build host 的本地文件系统中, 只能用于一次 build job 的后续步骤, 不能跨 Build Job 使用.

无论是哪种 Cache, 它的本质 **不是将**

例如对于 Python 开发者而言, 你可以将 Python 的 ``site-packages`` 目录缓存起来. 这样之后 ``pip install requirements.txt`` 的时候很多依赖都已经被安装过了, 可以节约大量时间.

例如对于 Docker image build 的项目, Layer 也可以被缓存起来以增加构建速度.

每次 Run build job 的时候, 在执行 Phase 之前这些缓存就会被下载并解压, 并覆盖已有的文件. 而每次执行完 build job 之后, 会把自动将 Cache 所监视的文件与之前构建的 Cache 进行比对, 并进行更新. 所以下一次 build 的时候就可以用到最新的 Cache 了.

Cache 的本质是一个 Git 文件系统, 维护了 metadata, fingerprint, 以及 simlink 的指针. 由于使用了 Git 文件系统来监控里面包含的文件, 所以每次 Cache 所监视的文件发生变化, 构建新的 Cache 只会发生在哪些变化的文件上, 从而获得非常好的增量更新性能. 而对于 S3 而言就是一个打包的 zip 压缩包, 解压后就是一堆 Git 文件系统的索引以及文件包, 并不是跟你 Cache 所对应的目录一样的文件树结构.

Ref:

- Buildspec reference: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html, 搜索 ``cache/paths`` 关键字
- Build caching in AWS CodeBuild: https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html

Shell Command and Failure
------------------------------------------------------------------------------
在 0.2 版本中, 每一个 command 命令的状态在各个 command 之间是保留的. 意思是比如第一个命令改变了当前的 directory, 创建了一些文件, 第二个命令是可以接着第一个命令往下做, 继承了第一个命令的状态. 具体 AWS CodeBuild 并不是简单的在一个 shell 里按照顺序执行命令, 但是你可以这么理解.

在一个 phase 里的 commands 部分, 如果一个命令 fail 了 (exit code not zero), 后面的命令是不会执行的. 但有时候你需要在出错之后, 依然进行一些收尾工作. 例如你开始启动了一个数据库, 但是测试挂了, 你之后销毁数据库的命令就不会被执行到. 这时你可以用 `finally <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.phases.finally>`_ 执行这些无论成功或是失败都要执行的收尾工作.

- On-failure: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.phases.on-failure
- Build phase transitions: https://docs.aws.amazon.com/codebuild/latest/userguide/view-build-details.html#view-build-details-phases


Batch Build Spec File Reference
------------------------------------------------------------------------------



