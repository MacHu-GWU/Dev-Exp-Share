CI/CD Product Overview
------------------------------------------------------------------------------


About this Ariticle
------------------------------------------------------------------------------
CI/CD 又名持续集成和持续交付是现代软件工程的基础设施, 保证了代码能快速的交付到生产环境中. 市场上跟 CI/CD 有关的服务太多了, 让人眼花缭乱. 我们就来挑几个市场上最流行的产品来梳理一下跟 CICD 有关的重要概念, 以后再看到任何一个新产品的时候, 可以很快的了解它的作用以及很快上手.

首先来看一下持续交付的底层到底是什么? 我们在软件开发的过程中, 一定会经过以下几个步骤:

1. 写源代码
2. 测试
3. 构建, 发布 artifacts
4. 部署
5. 以上步骤可能会在几个不同的环境中重复, 例如 dev, test, prod.

但无论做什么, 这些步骤的底层都是终端命令. 本质上持续集成持续交付就是一步一步的运行命令, 最终把代码部署到生产环境中. 这些命令之间的执行顺序错综复杂, 依赖繁复. 而且可能需要在不同的机器和系统上运行. 而人类希望能有一个用户友好的界面能了解这个过程中到底发生了什么. 为了解决这个问题, CI/CD 系统营运而生.

本文会按照由简单到复杂, 由具体到抽象的顺序, 介绍以下内容:

1. 以市场上比较流行的 GitHub action 为例来看看 CI/CD 的具体实现. 这个实现中设计哪些概念, 它们都是用来做什么的, 互相之间的层级关系是怎样的, 最终如何达成了 CI/CD 的目标.
2. 平行地将 GitHub action 和 Jenkins, CirCleCI, AWS CodeBuild + CodePipeline 进行比较. 了解它们之间的异同.
3. 总结一个 CI/CD 系统的本质是哪些模块, 回过头来再看市场上流行的 CI/CD 产品.


CI/CD GitHub Action
------------------------------------------------------------------------------
**Step**

CI/CD 最小的单元是终端命令. 在 GitHub Action 中一个 `step <https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps>`_ 就是按照顺序执行的一组命令. 在下面的例子中, 我们定义了一个叫做 ``Print a greeting`` 的 Step, 里面只有一条命令就是 ``echo ...``:

.. code-block:: yaml

    name: Greeting from Mona

    on: push

    jobs:
      my-job:
        name: My Job
        runs-on: ubuntu-latest
        steps:
          - name: Print a greeting
            env:
              MY_VAR: Hi there! My name is
              FIRST_NAME: Mona
              MIDDLE_NAME: The
              LAST_NAME: Octocat
            run: |
              echo $MY_VAR $FIRST_NAME $MIDDLE_NAME $LAST_NAME.

**Job**

在 Step 之上的概念是 `job <https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobs>`_, 一个 Job 包含多个 Steps, 并且会按照顺序执行这些 Steps. 一个 Job 有着确定的 Runtime (运行环境), 例如 Windows 还是 Linux, 虚拟机 还是 容器. Job 可以说是开发者跟 CI/CD 系统打交道时最常用的概念. 运行一个 Job 的过程可以叫做是 job run. 在下面的例子中, 我们定义了一个叫做 ``production-deploy`` 的 Job, 里面有 3 个 Steps. 其中前两个都是安装一些依赖, 最后一个则是运行 ``npm install`` 命令:

.. code-block:: yaml

    name: example-workflow
    on: [push]
    jobs:
      production-deploy:
        if: github.repository == 'octo-org/octo-repo-prod'
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-node@v3
            with:
              node-version: '14'
          - run: npm install -g bats

**Workflow**

在 Job 之上的概念是 `Workflow <https://docs.github.com/en/actions/using-workflows/about-workflows>`_. 既然每一个 Job 都是有自己独立的 Runtime, 而 CI/CD 中有些步骤需要在不同的 Runtime 中跑, 那么自然而然的就会需要用 Workflow 来 Orchestrate (编排) 许多 Job. 而编排就会涉及到顺序执行, 并行执行, 条件判断等等. 在下面的例子中就是一个顺序执行的例子, 先运行 setup, 再运行 build, 最后运行 test Job:

.. code-block:: yaml

    jobs:
      setup:
        runs-on: ubuntu-latest
        steps:
          - run: ./setup_server.sh
      build:
        needs: setup
        runs-on: ubuntu-latest
        steps:
          - run: ./build_server.sh
      test:
        needs: build
        runs-on: ubuntu-latest
        steps:
          - run: ./test_server.sh

总结下来就是, 无论是多么复杂的业务逻辑, 本质上就是在不同的 Runtime 中运行很多个 Job, 而每个 Job 中有多个 Step, 而每个 Step 中就是具体的终端命令. 接下来我们来看一下其他的 CI/CD 产品.


Other CI/CD Products
------------------------------------------------------------------------------
**GitHub Action**

这里概念我们就不介绍了, 只说一下它的独特之处. GitHub 在 2018 年 10 月被微软收购之后, 财大气粗. 于同年 2018 年 11 月发布了 GitHub Action. 提供了丰富的基于 Windows, MacOS 和 Linux 既有虚拟机, 又有容器的选项. 并且背靠微软, 对 Windows 的支持非常好. 弥补了开源软件通常对 Windows 支持不佳的问题. 并且是唯一一家支持 Mac Runtime 的服务提供商. 并且和 GitHub 紧密结合. 对开源项目完全免费.

**Jenkins**

Jenkins 是一个 2011 年发布的老牌开源 CI/CD 软件. 它本质上是一个 Web 服务器, 可以以单机或集群的方式部署. 支持虚拟机和容器的 Runtime.

`Jenkins Pipeline <https://www.jenkins.io/doc/book/pipeline/>`_ 和 GitHub Action Workflow 是同一级别的概念, 负责对 `Stage <https://www.jenkins.io/doc/book/pipeline/syntax/#stages>`_ 进行编排. 而不同的 Stage 可以用不同的 Runtime. 所以 Jenkins Stage he GitHub Action Job 是同一级别的概念. 在 Stage 里面会有许多 `Step <https://www.jenkins.io/doc/book/pipeline/syntax/#steps>`_, 每个 Step 就是一系列终端命令. 所以 Jenkins Step 和 GitHub Action Step 是同一级别的概念.

Jenkins 没有 SAAS 的版本, 至少 Jenkins 背后的公司不提供. 所以你需要自己配置安装 Jenkins 的服务器集群. 即使云上有很多成熟的方案, 不过你还是要自己维护.

**CircleCI**

CircleCI 是一个 2011 年成立的 CI/CD 服务提供商. 它提供 SAAS 版本和私有部署版本.

在 CircleCI 中同样有 `Step, Job <https://circleci.com/docs/jobs-steps/>`_, `Workflow <https://circleci.com/docs/workflows/>`_ 的概念, 和 GitHub Action 中的概念是一一对应的.

CircleCI 是创业公司, 它主打基于容器的 CI/CD. 对 Windows, Mac 的支持不够好. 但是它有很多很新的工具, 例如 可以复用的 Orb (虽然 GitHub Action 也有类似的). 同样对 Open Source 项目免费.

**AWS CodeBuild + CodePipeline**

AWS CodeBuild 是一个云服务, 可以用来在容器上运行 CI/CD. 一个 CodeBuild build job 对应着 GitHub Action 中的一个 Job. 在 Build job 有 Install, pre build, build, post build 四个 Phase, 每个 Phase 中可以按顺序运行很多 Command. 这个 CodeBuild Phase 就是和 GitHub Action Step 同级的概念.

而 AWS CodePipeline 则是为 CI/CD 专用的编排服务. 它可以对 CodeBuild Job run 进行编排. 除此之外, 它还和 AWS 各种原生服务紧密结合, 例如用 CloudFormation 部署, 用 S3 来保存 Artifacts, 用 CodeDeploy 来部署应用等等.

AWS 套餐的特点是它比较的私密, 毕竟继承了设计完善的 AWS IAM 的权限管理方式. 而且 CodePipeline 对 AWS 原生的支持简化了在使用其他产品时候需要写命令行命令来跟 AWS API 交互进行部署的麻烦, 只需要点击几下即可. 并且它是完全托管的服务, 无需管理任何基础设施, 开箱即用. 但是价格也是这些产品中最贵的.


Summary
------------------------------------------------------------------------------
看了这么多 CI/CD 的产品, 总结下来就是 Step 提供对一组为了达成某一个小目标的抽象, 而 Job 提供了执行一系列的 Step 的抽象, 定义了运行环境, 网络, 权限管理, 磁盘等硬件. 而 Workflow 则是对许多 Job 的编排. 其中 AWS CodePipeline 稍微特殊一点, 因为许多 Job 其实并不需要一个虚拟环境, 例如 CloudFormation 部署, 只需要一个命令即可, 所以它增加了很多对 AWS 原生服务的支持.

下表列出了这些产品的对比结果:

+-------------+---------------+------------------------+----------+------------------------------+
|             | GitHun Action |         Jenkins        | CircleCI | AWS CodeBuild + CodePipeline |
+=============+===============+========================+==========+==============================+
| Open Source |       ❌       |            ✅           |     ❌    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|  Free Plan  |       ✅       | Not a Service Provider |     ✅    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|     SAAS    |       ✅       |            ❌           |     ✅    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|  Self Host  |       ✅       |            ✅           |     ✅    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|   Windows   |       ✅       |            ✅           |     ✅    |               ✅              |
+-------------+---------------+------------------------+----------+------------------------------+
|    Linux    |       ✅       |            ✅           |     ✅    |               ✅              |
+-------------+---------------+------------------------+----------+------------------------------+
|    MacOS    |       ✅       |            ❌           |     ❌    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|      VM     |       ✅       |            ✅           |     ❌    |               ❌              |
+-------------+---------------+------------------------+----------+------------------------------+
|  Container  |       ✅       |            ✅           |     ✅    |               ✅              |
+-------------+---------------+------------------------+----------+------------------------------+
|     Step    |      Step     |          Step          |   Step   |             Phase            |
+-------------+---------------+------------------------+----------+------------------------------+
|     Job     |      Job      |          Stage         |    Job   |         CodeBuild Job        |
+-------------+---------------+------------------------+----------+------------------------------+
|   Workflow  |    Workflow   |        Pipeline        | Workflow |         CodePipeline         |
+-------------+---------------+------------------------+----------+------------------------------+