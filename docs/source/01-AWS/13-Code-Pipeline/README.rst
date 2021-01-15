Code Pipeline
==============================================================================

.. contents::
    :depth: 1
    :local:

Code Pipeline 是 AWS 提供的 持续集成, 持续部署 (CI/CD) 解决方案, 里面包含了 4 个子模块, Code Commit 负责管理代码仓库, Code Build 负责在容器中运行 test 和 build, Code Deploy 负责将 build 好的代码 deploy, 而 Code Pipeline 则负责将 Code Commit, Code Build, Code Deploy 编排到一起.

- Code Commit 中的概念 Source
- Code Build 中的概念 Project
- Code Deploy 中的概念 Application
- Code Pipeline 中的概念 Pipeline

什么是 Code Commit:

Code Commit 其实就是 Git 服务器的实现, Code Commit Repository 相当于一个用户界面远没有 GitHub 友好的 GitHub.


什么是 Code Build:

Build Spec File 就相当于 TravisCI 中的 ``.travis.yml``, CircleCI 中的 ``.circleci/config.yml``, 定义了多个 Job, 每个 Job 要执行的命令.

- Build Spec File Reference: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html

什么是 Code Deploy:

我们已经有了 Code Build 中的容器, 按理说可以执行一些命令将 App 部署了, 那 Code Deploy 存在的意义又是什么呢? Code Deploy 是一项跟 AWS EC2, Lambda, ECS 结合很紧的服务, 主要是负责将 App 部署到这些 AWS 原生计算平台上的.

.. autotoctree::
    :maxdepth: 1
