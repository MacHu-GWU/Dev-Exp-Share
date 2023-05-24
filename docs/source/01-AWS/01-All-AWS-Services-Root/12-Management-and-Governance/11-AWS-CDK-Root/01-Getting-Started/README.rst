Getting Started with AWS CDK
==============================================================================
这篇文章是我把在使用 AWS CDK 三个月以来学到的知识重新归纳梳理成文, 用于快速上手用 AWS CDK 进行 Infrastructure as Code 的开发.


1. 背景知识
------------------------------------------------------------------------------


1.1. Infrastructure as Code (IAC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 2007 年亚马逊云服务开始发力之前, IT 运维主要是在自建机房部署服务器. 而到了云时代, 对云上基础设施进行运维的方式跟以前大大不同了. 云厂商通常会提供一套 API, 用于 Create / Update / Delete 这些云资源. 但是一次次调用 API 来修改云资源的方式会让代码变得非常冗长. 于是就有了用声明式的语法来定义云上资源的方式. 它的核心就是定义了你所期望 (Desired) 的云资源的状态, 然后交给执行引擎去分析要达到这个状态, 需要做哪些变动, 哪些变动要先执行, 哪些变动要后执行. 这样可以使得代码更加简洁, 无论是对云厂商还是对用户而言都更好. 这种技术就叫做 Infrastructure as Code (下称 IAC), 基础设施即代码.

2010 年 AWS 发布了 CloudFormation, 是一款用 JSON 来定义基础设施的云服务. 显然 JSON 不是一款编程语言, 用来做 IAC 显得不是那么灵活. 而 2014 年 Hashicorp 公司发布了 Terraform, 是一款用 HCL, 一款 Hashicorp 公司发明的特殊领域编程语言, 比起 JSON 来已经好很多了, 但是仍然不是一款通用的编程语言. 在开源社区, 2013 年 Cloudtool 公司发布了 Troposphere, 允许用 Python 用面向对象的语法来生成最终的 CloudFormation template JSON. 但是这并没有得到官方的支持. AWS 于 2019 年发布了 CDK, 从此成为了官方支持的主流 IAC 工具.


1.2. AWS CDK 是什么
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
由上一节的讨论我们可以得知, 一款优秀的 IAC 工具需要具备如下几点:

1. 是真正的通用编程语言, 可以利用丰富的语言特性.
2. 可以支持多种流行的编程语言, 让各种背景的开发者都能上手.
3. 支持多种云服务, 而不是只支持某一家云厂商, 从而一次定义, 处处运行, 方便迁徙.

AWS CDK 由于只需要为自家产品服务, 所以它放弃了 #3, 但是对 #1, #2 的支持非常好. AWS 开发了一个黑科技 `jsii <https://github.com/aws/jsii>`_, 它能让其他编程语言和 TypeScript / JavaScript 中定义的类, 属性, 方法进行交互. 以此为基础, AWS 开发了 CDK, 基本上 Terraform Cloudformation 能做到的东西 CDK 都能做到. 然后亚马逊用各种编程语言 + jsii, 实现了在各种编程语言里写 CDK. 以 Python 为例, AWS CDK 的安装包里有 TypeScript 全部源码, 当你运行 Python 写的 Construct 的时候, CDK 会从 TypeScript 的源码 fork 一份出来然后通过 API 来跟 TypeScript 交互. (V2 版本为止是这样, 请参考这篇讨论 https://github.com/aws/jsii/issues/3389#issuecomment-1225625101). 当然这种方式的问题就是要经过从 TypeScript API 生成, Python 到 TypeScript, 最后 TypeScript 编译成 JavaScript 执行这么长的步骤, 这也导致运行的速度会比较慢. 但是作为一个运维工具, 用 CDK 进行部署是低频但是重要的需求, 所以性能不佳是完全可以接受的.


1.3. 一些小小私货
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我个人在 2018 年发布了 `cottonformation <https://github.com/MacHu-GWU/cottonformation-project>`_, 一款类似于 troposphere 的纯 Python 的 IAC 工具, 具有 IDE 友好的自动补全和类型提示, 并且没有什么依赖, 性能优异, 具有 CDK L1 Construct 的所有功能. 但是我个人精力有限, 所以我只在自己的项目中使用它. 个人用它的开发效率比用 CDK 和 Terraform 只快不慢.


1.4. 一些有用的链接
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- CDK 的官方文档, 里面有各个编程语言的子文档: https://docs.aws.amazon.com/cdk/v2/guide/work-with.html


2. AWS CDK in Python
------------------------------------------------------------------------------
CDK 支持 TypeScript, JavaScript, Python, Java, C#, Go. 除了 TypeScript 和 JavaScript 是 CDK 的第一实现语言, Python 是第二个支持的, 可见 AWS 对其的重视程度.

本章主要以 Python 开发者的角度来讲解 CDK 的使用.


2.1 安装前的准备工作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
而 CDK 本身是用 TypeScript 实现的, 也被称作 CDK 的 "核心编程语言". 假设你是用 Python 来开发 CDK, 那么这里 Python 就被称作 "目标编程语言".

用 Python 的 CDK 的开发者工具是由 3 个部件组成:

1. 在 NodeJS 中通过 npm 安装的包作为核心.
2. 目标编程语言中的 CDK 工具包, 在 Python 中是 `aws-cdk-lib <https://pypi.org/project/aws-cdk-lib/>`_.
3. 目标编程语言中的 (例如 Python) JSII 工具包, 在 Python 中是 `JSII <https://pypi.org/project/jsii/>`_, 使得目标编程语言能和 JavaScript 交互.

其中 #1 是无论使用哪种编程语言都要做的准备, 而 #3 一般以 #2 的依赖存在, 你安装 #2 的时候就会自动安装 #3.

为了照顾很多 Python 开发者并不熟悉其他编程语言的生态, 这里做一些名词解释:

- `TypeScript <https://www.typescriptlang.org/>`_ 是基于 JavaScript 的强类型编程语言. 由微软开发. TypeScript 会被编译器编译成 JavaScript 后执行.
- `NodeJS <https://nodejs.org/en>`_ 是一个 JavaScript 运行环境 (Runtime). 你可以这么理解. 浏览器中的 JavaScript 是在浏览器的 Runtime 中运行的, 用的是 Google 的 V8 编译器. 而 NodeJS 则是用于后端开发, 在本地环境中基于 V8 编译器的运行环境. 简单来说就是在本地运行 (相较于浏览器而言) 的 JavaScript 运行环境. 它不是一个语言.
- `NPM <https://www.npmjs.com/>`_ 是一个 NodeJS 的包管理工具. 你可以理解为是 Python 中的 pip 在 NodeJS 中的对应.

下面我们来介绍如何在 Mac 上安装 Node:

1. 安装 Node, 最好参考 Node 官方文档 https://nodejs.org/en/download/package-manager/

.. code-block:: bash

    # 安装最新的 node
    brew install node
    # 安装特定版本的 node, 推荐安装 18
    # 我现在的时间是 2023 年 5 月, 这是一个 LTS, long term support 版本, 支持到 2025 年 4 月,
    # 并且 CDK 在这个版本上充分测试过了
    brew install node@18

    # 如果安装了特定版本的 node, 你需要手动将其加到 PATH 中从而让你的 shell 能找到正确的 node
    export PATH="/opt/homebrew/opt/node@18/bin:$PATH"
    export LDFLAGS="-L/opt/homebrew/opt/node@18/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/node@18/include"

    # 该命令可以更新 node
    brew upgrade node

    # Linux 上的安装取决于你的系统
    depends on OS

    # 这里要注意, 你如果需要用特定版本的 node, brew 是可以允许你同时安装多个版本的 node,
    # 并且将全局的 node 命令绑定到特定版本
    # 如果你不小心安装错了 node, 比如直接用 brew install node 安装了
    # 那么你重新安装特定版本的 node 之后, 需要重新绑定 simlink, 使得全局的 node 指向
    # 的是你需要的那个版本, 下面的命令可以做到这一点
    brew link --overwrite node@18

2. 安装 Node 下的 CDK. 其他编程语言只是实现了一层壳, 还是需要调用 Node CDK 的 API. 最好参考 AWS CDK 官网文档 https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html.

.. code-block:: bash

    node
    npm install -g aws-cdk
    cdk --version


2.2. 在 Python 中安装 ``aws-cdk-lib``
------------------------------------------------------------------------------
AWS CDK for Python 是以 PyPI 上的第三方包的形式存在的. 在 CDK 1.X 的时候, 你需要安装的 `aws-cdk.core <https://pypi.org/project/aws-cdk.core/>`_. 然后各个服务有相应的子模块, 例如 S3 的是 `aws-cdk.aws-s3 <https://pypi.org/project/aws-cdk.aws-s3/>`_. 这对于开发者维护每个依赖的版本非常不方便. 从 CDK 2.X 开始, 你可以只安装一个 `aws-cdk-lib <https://pypi.org/project/aws-cdk-lib/>`_ 就可以了. 而对于还不是 stable 的实验性功能, 你可以通过安装  ``aws-cdk/aws-lambda-alpha`` 来使用. 但不推荐在生产环境中使用它们:

.. code-block:: bash

    pip install aws-cdk-lib

Reference:

- CDK Python 入门文档: https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html
- CDK Python Reference: https://docs.aws.amazon.com/cdk/api/v2/python/modules.html


3. 用 CDK 来部署一个 S3 Bucket
------------------------------------------------------------------------------


3.1 BootStrap 引导程序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在你第一次在某个 AWS Account 和 Region 中使用 CDK 的时候, 你需要做 Bootstrap. 这个 Bootstrap 的行为是为了在 AWS 中创建一些必要的资源来供 CDK 这个工具本身所使用. 我们快速的理解一下为什么要这么做. 我们拿 Terraform 来举例. 在使用 Terraform 的时候一般要指定 backend, 用来保存 metadata, deployed.json, 以及并发控制锁. 默认会在本地文件夹中进行. 如果你需要多人协作, 则通常用 S3 来保存 Metadata, 用 DynamoDB 来加锁. 但是 Terraform 是开源软件, 它不强制你用什么 Backend. 而 CDK 是完完全全为 AWS 打造的工具, 它自己就内置了自动配置 Backend 的功能.

Bootstrap 的过程中会在特定的 Account 和 Region 创建一个名为 ``CDKToolKit`` 的 CloudFormation Stack, 包括以下资源, 其中资源的名字都是 LogicID, 具体的 ResourceId 是根据你的 CDK 版本, AWS Account ID, Region 等生成的, 我们来一一介绍以下这些资源都是用来干什么的:

- ContainerAssetsRepository (AWS::ECR::Repository): 用来保存 Container Image 的.
- CloudFormationExecutionRole (AWS::IAM::Role): CDK 用这个来创建 CloudFormation Stack 中所定义的资源.
- DeploymentActionRole (AWS::IAM::Role): CDK 用这个来执行 CloudFormation Stack 的创建, 更新, 删除等操作, 而创建 Stack 中所定义的资源则是由 ``CloudFormationExecutionRole`` 来管
- FilePublishingRole (AWS::IAM::Role): CDK 用这个来发布 File Asset 到 S3 Bucket
- FilePublishingRoleDefaultPolicy (AWS::IAM::Policy): 上面这个 Role 的 Policy
- ImagePublishingRole (AWS::IAM::Role): CDK 用这个来发布 Container Image
- ImagePublishingRoleDefaultPolicy (AWS::IAM::Policy): 上面这个 Role 的 Policy
- LookupRole (AWS::IAM::Role): CDK 用这个 Role 来执行 list, descript 一类的 API
- StagingBucket (AWS::S3::Bucket): 用来保存 CloudFormation Template 的
- StagingBucketPolicy (AWS::S3::BucketPolicy):
- CdkBootstrapVersion (AWS::SSM::Parameter): 用来保存 BootStrap 的版本号

而运行 Bootstrap 的命令有很多种, 我们来了解一下有哪些方法以及分别适用于什么情况:

.. code-block:: bash

    # 在有 cdk.json 的目录下运行该命令, 默认使用当前的 AWS Default Profile 所对应的 Account 和 Region
    cdk bootstrap

    # 显式运行指定的 AWS Account 和 Region
    # 该命令通常用于 bootstrap 同一个 Account 但是不同的 Region,
    # 因为一个 AWS Profile 通常没有几个 Account 的权限, 这需要用 assume role 来做到
    cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1 aws://ACCOUNT-NUMBER-2/REGION-2 ...

    # 显式指定 AWS CLI Profile 所对应的 Account 和 Region
    cdk bootstrap --profile prod

Reference:

- Bootstrapping: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html
- How to BootStrap: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html#bootstrapping-howto

CDK 概念
------------------------------------------------------------------------------

Construct, L1, L2, L3 construct 的区别:

https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib

- L1 为最底层 API, 代表 CloudFormation (CFN) Resource, 所以 import name 一般是以 ``Cfn`` 开头. 你需要明确指定所有要求的 Property 的值.
- L2 为 L1 的 Wrapper, 通常提供了比较靠谱的默认值, 你无需指定所有的 Property 值即可顺利使用.
- L3 叫做 Pattern, 也是多个 Resource 的集合.


AWS CDK v2
------------------------------------------------------------------------------
- `Migrating to AWS CDK v2 <https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html>`_
- `Runtime context <https://docs.aws.amazon.com/cdk/v2/guide/context.html>`_: cdk.json Document

