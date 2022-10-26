Sagemaker Domain, Studio and Canvas
==============================================================================
Keywords: Sagemaker, Domain, Studio, Canvas


What is Sagemaker Domain, Studio, Canvas
------------------------------------------------------------------------------
对于数据科学家和数据分析师来说, 杀手应用是 Jupyter Notebook. 而 AWS Sagemaker 的杀手应用则是 Studio, 一个 AWS 基于 Jupyter Lab 进行二次开发的 IDE 环境. 界面跟 Jupyter Lab 非常类似. 很多人会将 Sagemaker Studio 和 Jupyter Lab 划等号. 从 UI 上看两者是类似的, 但是从概念上看两者并不一样.

这几个东西经常放在一起讲, 我们先来对其做一个简单区分:

1. Domain

    一个 SM Domain 就是一堆对用户不可见的 网络, 文件系统, 虚拟机 等实体资源. 而你的 ML 开发环境, 脚本存储等都需要在上面运行. 一个 SM Domain 下有如下资源.

    1. 一个 EFS 文件系统
    2. 一堆 Authorized User
    3. 一堆 Security Policy
    4. 一个 VPC

    一个 AWS Account 的一个 Region 只能有一个 SM Domain. 在这个 Domain 的 内部, 你可以 Share notebook 和文件以及其他的 Artifacts. 一个 Domain 下可以有很多 UserProfile 和 App. 一个 UserProfile 就代表了一个 IAM Role, 你要使用 App 就得 assume 一个 UserProfile. 而这个 UserProfile 的 IAM 权限决定了他进入 App 之后能干什么.

    在 Domain 上可以运行很多 App, 例如 Python 开发者用的 Studio, R 开发者用的 RStudio, 不会写代码的人用的 Canvas.

    参考资料:

    - Onboard to Amazon SageMaker Domain: https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-onboard.html

2. Studio App

    是你的 ML 开发的 IDE. 背后是在 Domain 上的某台机器运行着的 Jupyter Lab. 要运行 Studio 你要先选择 UserProfile 然后点 Launch App, 然后就会自动选择 Domain 上的某台机器运行 Jupyter Lab, 并且自动连接上 EFS 上的文件数据.

3. RStudio App

    我没有研究, 估计是 R 语言对应着的环境

4. Canvas App

    是 AWS 开发的一个 low code ML 的环境, 让用户不写 Code 也能构建 ML 模型

简单来说就是 Sagemaker Domain 是 Infrastructure, 而 Sagemaker Studio / RStudio / Canvas 这些都是运行在 Domain 上面的 App.


IAM Permission
------------------------------------------------------------------------------
你在创建 Sagemaker Domain 的时候就会连带创建一些 Service Role. 而允许创建和修改 IAM Role 的权限一般只有 Admin 才有. 所以 `这篇官方文档 <https://docs.aws.amazon.com/sagemaker/latest/dg/gs-set-up.html>`_ 才会说让有 Admin 权限的人来负责创建 Sagemaker Domain. 而其他权限较低的 Data Scientist 和 ML Engineer 都是 User.

你需要给你的 Domain 一个 Execution Role 作为那些 App 所拥有的权限. 如果你使用 wizard 自动创建这个 Execution Role, 那么你会发现里面的 Policy 实际上是一个 ``arn:aws:iam::aws:policy/AmazonSageMakerFullAccess`` 以及一个允许对一些 S3 Bucket 进行访问的 Policy. 非常简单. 你完全可以自己创建这个 Role.


Network Configuration
------------------------------------------------------------------------------
创建 Sagemaker Domain 的时候有两种网络模式. 一种是 "Public Access" 还有一种是 "VPC Only". 请注意这里的 "Public Access" 并不是说你的 Sagemaker Domain 上运行的 Jupyter Notebook 什么的都可以被所有人访问到. 并不是这样. 你还是需要 login AWS Console, 然后点击 Launch App, 后台实际上会自动生成一个临时的 Token 和 URL 进行连接. 这里的 "Public Access" 指的是你位于 Domain 上的 EC2 资源是否有 Public Access 的网络连接. 这里我们分情况讨论.

"Public Access"

"VPC Only Mode" 的含义以及网络配置前提条件, 详情请参考 `这篇文档 <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-and-internet-access.html#studio-notebooks-and-internet-access-vpc>`_

简单来说就是你的 Sagemaker Domain 要在 Private Subnet 上运行, 并且为 S3, Sagemaker, Sagemaker-runtime, Service-Catalog 创建 Private Link, 以确保从 Jupyter Notebook 上能访问这些 API. 这些 Private Link 是必须得, 因为你在启动 Studio App 的时候就需要用到这些 API, 如果没有 Private Link 你连 Studio 都进不去. 而你在从 Console 连接到 Studio App 的时候是不需要 Security Group 的, 因为 Studio IDE 本身是运行在 AWS 一个巨大的 Pool 里的, 并不是运行在 VPC 上, 而你的 Notebook 和本地文件存放在位于 VPC 里的 EFS 中, 所以数据是安全的.


Delete Sagemaker Domain
------------------------------------------------------------------------------
删除 Sagemaker Domain 也比较 Tricky. 毕竟很多 App 都在上面跑着, 如果点两下就能删掉一个 Domain 那也太不安全了.

要删掉 Domain, 就要删掉上面所有的 User Profile; 要删掉 User Profile, 就要删掉所有与之相关的 App. 其中 Jupyter Server App 要被删掉, 就要先删掉 EFS (不然会无限自动启动, 我也不知道这么做对不对, 反正删掉 EFS 之后就不会无限启动了). 你按照这个顺序反过来即可. 详情请参考 `这篇文档 <https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-delete-domain.html>`_


Sagemaker Domain 底层架构
------------------------------------------------------------------------------
这里有个 **巨坑**. 虽然 Sagemaker Domain 是有 VPC Mode 这个选项, 但是无论是 Sagemaker Studio App, 还是 Jupyter Notebook, 还是 Remote Training, 还是 Endpoint, 实际都 **不在** 你自己的 VPC 上运行. 而是在一个 AWS 内部的 Isengard Account 上运行的. 所以你的 VPC 的 Security Group 不影响你的 Sagemaker 资源. 你的 VPC 只用来部署 EFS 文件系统, 以及如果你需要 call AWS API 的时候可以用 VPC Endpoint 将流量限制在 AWS Network 以内, 而不走公网.


参考资料
------------------------------------------------------------------------------
- Amazon SageMaker Machine Learning Environments 详细介绍了 Domain, Studio, RStudio, Canvas 等概念和用法: https://docs.aws.amazon.com/sagemaker/latest/dg/domain.html
- 详细介绍了创建 Sagemaker Domain 的前提条件: https://docs.aws.amazon.com/sagemaker/latest/dg/gs-set-up.html
- 详细介绍了 Sagemaker Domain 的两种网络配置模式的区别和前提条件: https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-and-internet-access.html#studio-notebooks-and-internet-access-vpc
- 介绍了如何删除一个 Sagemaker Domain: https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-delete-domain.html
