.. _aws-cli-tutorial:

AWS CLI Tutorial
==============================================================================

AWS 命令行介绍.


Configure AWS CLI
------------------------------------------------------------------------------

- ``~/.aws/config``: 主要是配置不同的 AWS Profile.
- ``~/.aws/credentials``: 主要解决的是 credentials 相关的信息, 比如 ACCESS KEY, SESSION TOKEN 等.


**Configuration settings and precedence**

由于 AWS CLI 会从多个地方读取参数, 主要是哪些权限的参数, 当一个参数在多个地方同时存在时, 会按照如下的顺序优先使用靠前的值.

1. Common line option, such as ``--profile``
2. Environment Variable
3. CLI credential file: ``~/.aws/credentials``
4. CLI config file: ``~/.aws/config``
5. Container Credential: ECS IAM Role
6. Instance Profile Credential: EC2 IAM Role

**Reference**

- Environment variables to configure the AWS CLI, 可用的 环境变量: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
- Using an IAM role in the AWS CLI, 在 aws cli 中使用 IAM Role 而不是 IAM User: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html
- CLI Configuration: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
