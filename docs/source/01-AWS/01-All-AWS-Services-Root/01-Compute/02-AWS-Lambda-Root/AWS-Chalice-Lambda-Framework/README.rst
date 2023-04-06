AWS Chalice
==============================================================================
Keywords: AWS Chalice, Lambda, Microservice, Serverless, Framework, Python, Best Practice



What is AWS Chalice
------------------------------------------------------------------------------
随着微服务的火热, 开源的微服务框架越来越多. 比如有下面几个著名框架.

- `serverless <https://www.serverless.com/>`_: 特点是支持多种编程语言, 多种云服务
- `sam <https://aws.amazon.com/serverless/sam/>`_: 特点是支持多种编程语言, 只支持 AWS
- `chalice <https://aws.github.io/chalice/>`_: 只支持 Python 和 AWS

显而易见, 你想同时支持的东西越多, 功能就不可避免的不够强大. 因为不是所有强大的功能都能在不同的编程语言和不同的云上实现. 而 AWS Chalice 则是将功能和便利性做到了极致, 不过只支持 Python 和 AWS


同一个 Code Base, Deploy 到多个账户, 多个 Region
------------------------------------------------------------------------------
**多个 Region**

这个比较简单, 在 Chalice 里有 stage 的概念, 其实就是一个 namespace, 你可以把 region name 作为 stage, 在不同的 stage 里用不同的 layer 即可. 然后每次运行 ``chalice deploy`` 命令的时候加上 ``--profile ${your_aws_cli_named_profile}``, 这些 named profile 的 config 里就定义了他们对应的是哪个 region.

**多个 Account**

这个也类似, 同样用 stage, 不过 stage 就得是 ``${account_name}-${region}`` 这样的形式, 然后同样用 ``--profile`` 不同的 profile 就对应着不同的 account 和 region


同一个 Lambda Function 支持多个 Trigger
------------------------------------------------------------------------------
从逻辑上, 这是不推荐的. 因为不同的 Trigger 有不同的 event JSON schema. 你很难用一套代码来适配. 但是有个特殊情况就是你有时候需要用同一种类型的 trigger, 比如都是 S3 bucket trigger, 但是有很多个 bucket 都能 trigger 同一个 Lambda. 这种情况下在 Console 里能做到. 但是 Chalice 并不支持. 你无法用多个 ``@on_s3_event`` decorate 标注同一个 Lambda 函数.


