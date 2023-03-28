.. _aws-batch-root:

AWS Batch Root
==============================================================================
Keywords: AWS

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is AWS Batch
------------------------------------------------------------------------------
AWS Batch 是为了解决一次性调用大量计算资源而存在的. 传统做法是你要配置好 EC2 集群, 然后定义 Job, 然后将 Job 分发到 EC2 上. AWS Batch 则是将这些步骤抽象化了.


AWS Batch Concept
------------------------------------------------------------------------------

- Compute Environment: 你的运行环境. 目前支持 Fargate, Fargate Spot, On Demand EC2, Spot EC2 四种. 可以选择让 AWS Manage Scale 还是你自己 Manage. 然后就是一些 VPC 的设置.
- Job Definition: 定义你的 Job.
    - 有 Single node 和 Multi node parallel 两种模式
    - Platform 计算平台, 有 Fargate 和 EC2 两种
    - Job Configuration 就是具体运行的命令, 就是一个 bash 命令而已
    - CPU 和 Memory
    - Retry setting
    - Parameter
- Job: 一个根据 Job Definition 启动的, 真正运行的 Job 实例.
- Job Queue: 一个 Priority Queue 优先队列.


aws ecr describe-repositories --repository-id https://public.ecr.aws/v2/amazonlinux/amazonlinux/manifests/latest: