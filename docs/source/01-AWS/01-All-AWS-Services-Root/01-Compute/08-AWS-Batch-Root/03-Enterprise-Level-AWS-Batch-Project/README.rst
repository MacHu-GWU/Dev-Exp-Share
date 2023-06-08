.. _enterprise-level-aws-batch-project:

Enterprise Level AWS Batch Project
==============================================================================
Keywords: AWS Batch, Job, Enterprise, DevOps, Architecture.

一个极简的 AWS Batch 项目至少包含了了以下资源:

- 一个 Computer Environment (CE), 定义了网络, Subnet, Security Group, 最大算力.
- 一个 Job Queue (JQ), 用来给 Job 排序.
- 一个 ECR Repo 用来保存你的镜像.
- 一个构建好的 Container Image
- 一个 Job Definition (JD), 里面定义了使用你的 container image 来计算的细节, 包括 CPU, Memory, Command, Parameter, Environment Variables 等等.
- 还有一些由 StepFunction, Lambda 组成的 Job 编排工具将 JD Submit 到 JQ 中, 然后交给 CE 来运行. 并对计算状态进行监控, 对计算结果进行检查.

而一个公司可能有非常多个这样的项目. 这些资源里有些适合跟着每个项目单独部署, 有些适合统一管理. 由于没有银弹, 能满足所有需求的架构设计是不存在的. 而本 Solution 则给出了一个经过时间考验的相对最优解.

简单来说, 我们以一个 AWS Account 中的一个 Region 为最小单位. 在每一个 Region 中 Computer Environment 和 Job Queue 由一个 CloudFormation Stack (或是 Deployment Unit) 来单独管理. 然后每个具体的 Batch Job 业务对应着以下资源:

- 一个 ECR Repo
- 一个打包了 Application Code 的 Container Image
- 一个 Job Execution Role
- 一堆 Job Definition 的版本
- 可能还有一些编排工具, 比如 StepFunction, Lambda 等等.

其中 ECR Repo, IAM Role 由 CloudFormation Stack 来管理. Container Image 由 CodeBuild Job Run 来构建并发布. 而 Job Definition 则是用 AWS SDK 来调用 API 来创建. 然后再在 CI Job 中去进行 Integration Test. 这一套东西组成了一个 Deployment Unit.

因为编排项目可能会涉及到多个 Job Definition 和其他的 Lambda 等资源, 适合单独开一个项目 (Deployment Unit) 来管理.

下面是一个设计架构图:

.. raw:: html
    :file: ./enterprise-level-aws-batch-job-project.drawio.html
