AWS CDK
==============================================================================


AWS CDK 是什么?
------------------------------------------------------------------------------

本质上 AWS CDK 是为了提供类似于 Terraform 和 Cloudformation 的 AWS 原生 Infrastructure as Code 解决方案.

亚马逊 有一个黑科技 `jsii <https://github.com/aws/jsii>`_ 能让其他编程语言和 TypeScript / JavaScript 中定义的类, 属性, 方法进行交互. 以此为基础, AWS 开发了 CDK, 基本上 Terraform Cloudformation 能做到的东西 CDK 都能做到. 然后亚马逊用各种编程语言 + jsii, 实现了在各种编程语言里写 CDK. 以 Python 为例, AWS CDK 的安装包里有 TypeScript 全部源码.


一些有用的链接
------------------------------------------------------------------------------

- CDK 的官方文档, 里面有各个编程语言的子文档: https://docs.aws.amazon.com/cdk/v2/guide/work-with.html
- CDK python 文档: https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html


CDK in Python
------------------------------------------------------------------------------

无论使用哪种编程语言都要做的准备:

虽然这段说的是在 Python 下使用 CDK, 但是这段准备工作是在你使用其他语言时也要做的.

1. 安装 Node, 最好参考 Node 官方文档 https://nodejs.org/en/download/package-manager/ ::

    # Mac

    brew install node
    brew upgrade node

    # Linux
    depends on OS

2. 安装 Node 下的 CDK. 其他编程语言只是实现了一层壳, 还是需要调用 Node CDK 的 API. 最好参考 AWS CDK 官网文档 https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html::

    node
    npm install -g aws-cdk
    cdk --version

3. AWS CDK for Python 是以 Pypi 上的第三方包的形式存在的. 其中必须要安装的是 ``aws-cdk.core``. 然后各个服务有相应的子模块. pip 安装命令为::

    pip install aws-cdk.core
    pip install aws-cdk.aws_s3


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