.. _aws-eb:

AWS Elastic Beanstalk (EB) Docs
==============================================================================

EB 是亚马逊云上用于快速部署生产环境中的 Web 应用的服务. 减少了管理 虚拟机, 负载均衡, 日志管道, 弹性伸缩 等基础架构的麻烦.

.. contents::
    :depth: 1
    :local:


Elastic Beanstalk 具体解决了什么问题
------------------------------------------------------------------------------

首先我们来定义一下, **什么是通用型的 Web 应用**. 简单来说, 淘宝, 博客, GitHub 等这些网站都是 Web 应用, 主要面向真人用户. 而还有一类 Web 应用主要面向编程接口, 俗称 API Server. 这一类服务的部署方式可以沿用 Web 应用的方式, 但是 EB 不是主要为 API Server 服务的.

我们来了解一下一个通用型的 Web 应用, 通常需要哪些组件.

- 虚拟机 集群: 对于流量大的应用, 肯定需要多台虚拟机用于处理大量流量, 单机是肯定不够的, 而且多台机器可以保证一台机器挂掉, 服务依然可用.
- 负载均衡: 负载均衡 位于 用户客户端 和 虚拟机 集群之间. 用户访问网站时, 实际上是访问的是负载均衡的入口, 负载均衡将请求转发到具体的虚拟机. 负载均衡能保证流量均匀的分配到每一台服务器上. 负载均衡由于只专注一件事, 其本身必须是高性能, 高可用的.
- 日志管道: 多台虚拟机的日志需要经过汇总, 统一的打到一个日志管道上. 供监控, 调试所使用
- 弹性伸缩: 对于流量的变化, 自动调整虚拟机的数量.

而 EB 能够用高度抽象的配置语言, 对以上四大组件进行配置, 然后使得用户专注于写应用代码. 在部署的时候同时部署以上的所有组件, 在摧毁的时候也同时摧毁以上所有组件.

同时 EB 支持 5种 部署模式 (参考 https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html):

- All at once
- Rolling
- Rolling with additional batch
- Immutable
- Blue/Green


Elastic Beanstalk 是怎么解决这些问题的
------------------------------------------------------------------------------

EB 提供了一个 console, 用于可视化所有的设置. EB 还有个命令行工具. 叫做 aws eb cli (``pip install awsebcli``), 用于在 Git 仓库中初始化配置文件, 并根据配置文件将代码打包, 部署到服务器上. 而这个部署过程是用 CloudFormation 进行实现的. EB 会根据配置文件生成一个 CloudFormation Template, 然后根据你选择的 部署模式 将所有的 EC2, Security Group, IAM Role, ELB, ASG, Log Group 一次性部署.


TODO 如何进行测试
------------------------------------------------------------------------------


重要的文档链接
------------------------------------------------------------------------------

- EB 支持的编程语言平台: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts-all-platforms.html
- YAML 配置文件的结构, Key, Value: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html
- EB 的部署模式: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html
- EB 命令行手册: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html
