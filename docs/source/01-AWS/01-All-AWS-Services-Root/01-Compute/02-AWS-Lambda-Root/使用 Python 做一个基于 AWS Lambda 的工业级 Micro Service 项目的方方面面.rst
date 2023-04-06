使用 Python 做一个基于 AWS Lambda 的工业级 Micro Service 项目的方方面面
==============================================================================

工具链:

- CircleCI: CI / CD, 持续测试, 部署.
- CloudFormation: 用于自动化构建 VPC, S3, IAM, API Gateway 等部件.
- Serverless Framework: 用于构建 Lambda.


常见的坑:

- 将 Service 部署在已经存在的 VPC 里.
- 为 Service 创建新的 VPC.

Serverless Framework 实际上是根据 ``serverless.yml``, 生成 CloudFormation Template. 所以本质上还是 CloudFormation (CF). 在 CF 中, 删除一个 Stack 会同时删除所有相应的资源. 创建.


CI / CD
------------------------------------------------------------------------------

当有代码被 Merge 到 Master 后, 到最终代码部署到 prod 之间, 需要这么几个步骤:

1. 在 CI 环境中运行单元测试.
2. 测试通过后将 Service 部署到 Test Stage 环境中.
3. 部署到 Test Stage 成功后, 在 Test 环境中运行 Integration Test.
4. 如果测试成功, 则将 Service 部署到 Stage 环境中.
5. 当 Stage 环境运行较为稳定后, 将其部署到 Test 环境中.



在本机运行

pylbd deploy

