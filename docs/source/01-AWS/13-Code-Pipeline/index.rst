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


Code Commit
------------------------------------------------------------------------------

什么是 Code Commit? Code Commit 其实就是 Git 服务器的实现, Code Commit Repository 相当于一个用户界面远没有 GitHub 友好的 GitHub.


使用 Code Commit Repository 作为 Git Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 创建代码仓库: 进入 Code Commit 的菜单, 点击 Repositories 菜单, 点击 Create Repository, 这里输入的名字就是相当于你 GitHub Repo Name. 然后记录下 Https Clone Url. 这样 ``$ git clone <http_clone_url>`` 命令就可以将代码拖到本地了.
2. 创建连接密码: 进入 IAM, 找到你的 IAM User, 选择你的 User 后, 选择 Security Credential Tab, 在 HTTPS Git credentials for AWS CodeCommit 一项中选择 Generate, 创建用户名和密码.


使用 GitHub Repository 作为 Code Commit 的 Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




Code Build
------------------------------------------------------------------------------



Build Spec File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Build Spec File 就相当于 TravisCI 中的 ``.travis.yml``, CircleCI 中的 ``.circleci/config.yml``, 定义了多个 Job, 每个 Job 要执行的命令.

- Build Spec File Reference: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html


Code Deploy
------------------------------------------------------------------------------

我们已经有了 Code Build 中的容器, 按理说可以执行一些命令将 App 部署了, 那 Code Deploy 存在的意义又是什么呢? Code Deploy 是一项跟 AWS EC2, Lambda, ECS 结合很紧的服务, 主要是负责将 App 部署到这些 AWS 原生计算平台上的.
