AWS CodeBuild Basic
==============================================================================
Keywords: AWS CodeBuild Basic


1. What is AWS CodeBuild
------------------------------------------------------------------------------
AWS CodeBuild 是一个全托管的 CI 服务. 和市面上的明星 CI 产品 CircleCI, GitHub, Jenkins 的定位是有很大的不同的. 虽然他们都提供了用 yaml 或是 DSL 来 orchestrate build job 的功能. 但是内核上有本质区别.

CircleCI 着眼于强大的编排, 并行执行能力, 以及强大的 Orb (和 GitHub Action 类似, 都是 CI job 级的复用). GitHub 着眼于丰富的 Environment, 以及跟 GitHub 的良好支持. Jenkins 作为老牌 CI 产品着眼于强大的 UI 和插件, 适合能自己折腾自己搭建的企业. 而 AWS CodeBuild 则是着眼于给用户在 Orchestration 以及 Trigger 上最大的自由度, 以及跟 AWS 其他服务紧密结合, 特别是与 AWS 的 Git 仓库服务 CodeCommit, 以及持续部署服务 CodeDeploy.

简单来说你如果是企业用户, 希望这个环境非常的私密, 但你又不想要花精力搭建 CI 的基础设施 (例如搭建 Jenkins Cluster), 那么 CodeBuild 就是一个非常合适的产品.

- SUBMITTED
- QUEUED
- PROVISIONING
- DOWNLOAD_SOURCE
- INSTALL
- PRE_BUILD
- BUILD
- POST_BUILD
- UPLOAD_ARTIFACTS
- FINALIZING
- COMPLETED


2. Build Environment
------------------------------------------------------------------------------
所谓 Build Environment 就是 OS, Programming Language Runtime 和 tools 的组合. 一个 Environment 必定包含一个 Docker image 作为主要的运行环境.

你可以查看下面几篇文档了解有哪些自带的 Environment:

- 有哪些 AWS CodeBuild 自带的 Docker Image: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
- 有哪些 Programming Language Runtime 可以用: https://docs.aws.amazon.com/codebuild/latest/userguide/available-runtimes.html
- 这些 Runtime 有哪些具体版本: https://docs.aws.amazon.com/codebuild/latest/userguide/runtime-versions.html

其次你可以为这些 Environment 配置不同的计算资源, 你可以查看下面的文档了解有哪些选项:

- https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html

虽然 AWS 说 Build Environment 必定包含一个 Docker Image, 但是 Environment 其实还是一个已经预热好的 VM 虚拟机. 而这个 Docker Image 只是用来运行你的 Build Job 而已. 你可以将 CodeBuild 的运行环境理解为一个完全隔离的 VM. 本质上是 AWS 维护了一个巨大的 EC2 Cluster, 然后再这个 Cluster 上虚拟出非常多的隔离环境, 创建这些隔离环境的速度只比 container 慢一点, 大约是 3 - 5 秒这个级别. 由于本质上还是 VM, 所以你可以在里面 build docker image, 或是启用几个 docker image 作为 background job, 例如使用 postgres 数据库进行测试.

Ref:

- https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref.html


3. Buildspec File
------------------------------------------------------------------------------
Jenkins 用 Groovy, 而 CircleCI, GitHub Action 用 YAML. AWS CodeBuild 也用 YAML 作为定义 Orchestration 的声明文件. 这个特殊的文件叫做 ``buildspec.yml``, 默认放在根目录下, 你也可以放在其他目录下, 不过你要显式告诉 CodeBuild 在哪里.

这个 ``buildspec.yml`` 主要包含这么 3 个部分.

1. Environment: 定义你的运行环境, 用什么 OS 和编程语言, 有哪些工具, 环境变量有什么
2. Job: 一个 build job 分几个 Phase, 这里跟 Jenkins 里的 stage 类似, 不过 CodeBuild 定死了只有 4 个 Phase, install, pre_build, build, post_build. 这里定义了你具体的 CI 逻辑
3. Artifacts, Report: 定义了 artifacts 上传到哪里, 生成的 test report 储存在哪里, 以及 cache 相关的内容.


4. Regular Job and Batch Job
------------------------------------------------------------------------------
CodeBuild 里有两种 Job, 一种是普通 Job, 另一种是 Batch Job. 简单来说普通 Job 就是做一件事, 而 Batch Job 则是将很多普通 Job 组织起来, 按照一定的编排顺序执行. 本质上这就是 CircleCI 中的 `workflow <https://circleci.com/docs/workflows>`_ 功能. 每一个 Job 对应一个 ``buildspec.yml`` 文件, 最后有一个总览的 ``buildspec-batch.yml`` 文件将这些 Job 编排到一起.


5. Source
------------------------------------------------------------------------------
Source 通常指的是 Git. AWS 默认支持和 GitHub, GitHub Enterprise, BitBucket 以及自家的 AWS CodeCommit 打通. 对于其他的 Git 系统例如 GitLab, 你可以通过配置 post commit git hook 自动在每次 commit 后将代码打包发到 AWS S3, 然后以 S3 为 Source.


6. Trigger
------------------------------------------------------------------------------
Trigger 指的是我们希望哪些 Git event, 以什么方式 trigger CodeBuild run. 这点 CodeBuild 功能不是很强大, 但是他提供了底层的接口允许你实现任何东西.

抛开 CodeBuild 不谈, 任何 Git Repo 的 SAAS 提供商与 CI 服务相结合的原理都是通过 Webhook. Webhook 是 `Git hook <https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks>`_ 的变种. 对本地的 git 进行各种操作后自动发送 event 这叫 git hook. 而对 SAAS 服务商提供的远程 git 操作触发的 event 就叫做 webhook. 你可以通过配置让 SAAS 服务提供商将 webhook 发送到指定的 API 接受. 这个 API 往往是由 CI 服务的提供商维护的, 于是 CI 就可以收到这些 event, 并对其进行处理, 以决定要不要, 如何 trigger build job. 市场上的 CircleCI 和 GitHub 打通, travis 和 GitHub 打通都是通过这个原理实现的.

对于 CodeBuild 而言, 我们完全可以创建一个 API Gateway, 后面是 Lambda Function. 然后我们把 Webhook event 发送到这个 API Gateway endpoint. 之后就可以在 Lambda Function 中对 event 进行分析, 从而做到任何你想做到的事情.

在不使用 Lambda 的情况下, AWS CodeBuild 支持 0 代码配置 GitHub Enterprise 的 Trigger 以及 AWS CodeCommit 的 Trigger. 但有能力的公司最好还是自己配置 Lambda, 这样才能灵活适配企业内部的各种独特的需求.


7. FAQ
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Why my build run takes very long for Provisioning (>= 3 minutes)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
所谓 Provisioning 就是创建 build job 的 environment. 最流行的 runtime 是 Docker Container. 由于本质上 CodeBuild 是一个超级大的 EC2 Cluster 集群, 你发起一个请求, 那么 AWS CodeBuild 就会自动找到一个 EC2 来运行你的 Build Job. 但是这么多用户可能要用到不同的 Docker Image, 不可能所有的 EC2 上都预先缓存了所有的 Docker Image. AWS 的原则是在所有机器上默认缓存每个不同类别的 Environment 的最新版本. 你如果在 Build Project 中选择的是默认使用最新, 那么 Provisioning 的时间就比较可控, 而如果你用的是特定版本号的 AWS managed environment, 那么你只能祈祷好运最近有人用过同样的 environment 刚好在分配给你的这台机器上运行过.

如果你使用的是自定义的 Image, 那么你就得自己负责让这个 Image 小一点, 这样每次 Provision 的时间也短一点.

Ref:

- https://github.com/aws/aws-codebuild-docker-images/issues/296
- https://www.reddit.com/r/aws/comments/fjvvb8/codebuild_provisioning_very_slow_most_times/