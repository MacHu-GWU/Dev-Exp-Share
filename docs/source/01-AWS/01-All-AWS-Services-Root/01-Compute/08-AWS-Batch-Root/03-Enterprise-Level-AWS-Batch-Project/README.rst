.. _enterprise-level-aws-batch-project:

Enterprise Level AWS Batch Project
==============================================================================
Keywords: AWS Batch, Job, Enterprise, Multi, Multiple, Env, Environment, DevOps, Architecture.

一个极简的 AWS Batch 项目至少包含了了以下资源.

- 一个 Computer Environment (CE), 定义了网络, Subnet, Security Group, 最大算力.
- 一个 Job Queue (JQ), Job 会被丢到这个 Queue 里, 然后按照优先级决定先运行谁后运行谁.
- 一个 ECR Repository (ECR Repo) 用来保存你的镜像.
- 一个被 Push 到 ECR Repo 中的 Container Image, 里面包含了你的 Application 代码.
- 一个 Job Definition (JD), 里面定义了使用你的 container image 来计算的细节, 包括 CPU, Memory, Command, Parameter, Environment Variables 等等.
- 在最简单的情况下是直接根据 JD Submit 一个 Job 到 JQ 中, 然后交给 CE 来运行.
- 复杂一点的情况下是使用编排工具例如 StepFunction 跟其他计算单元如 Lambda, Glue 一起完成一个任务.

而一个公司可能有非常多个这样的项目. 这些资源里有些适合跟着每个项目单独部署, 有些适合统一管理. 有些适合每个环境 (Sandbox, Test, Prod) 中各一个, 有的适合所有环境都共享一个. 有的适合每个 AWS Account Region 部署一个, 有的适合多个 AWS Account 共享一个. 本文我们给出了一个适合企业级的 AWS Batch 项目的架构图, 并且详细分析了为什么这样设计.

.. raw:: html
    :file: ./enterprise-level-aws-batch-job-project.drawio.html
