Learn AWS CDK Pipeline
================================================================================


1. 什么是 AWS CDK Pipeline
------------------------------------------------------------------------------
AWS CDK Pipeline 是一个 CDK 的功能, 它可以让我们用 CDK 来定义一个 CI/CD Pipeline. 通常 CI/CD 都需要定义 Pipeline, 定义执行的 Terminal Command 的流程, 并且需要自己管理用于 CI/CD 的资源. 是有一些前期工作的.

而 CDK Pipeline 则是用 IAC 的方式自动生成这些用于 CI/CD 的 CodePipeline, CodeBuild Project 等资源. 通常的 CI/CD 工具允许开发者在 YAML 文件中修改 CI/CD 的逻辑, 但如果要修改用于 CI/CD 的 Infrastructure 本身还需要自己再部署一次. CDK 的牛逼之处的是它还能对用于 CI/CD 的资源进行自我更新.

CDK Pipeline 的理念是, 一切的部署都是 Infrastructure as Code. 由于 CDK 对很多原生的 CloudFormation 做了增强, 很多原生 CF 做不到的事情, 例如发布一个软件的新版本, 都可以通过 CDK 来实现. 在 CDK Pipeline 中, 它用一个 CodeBuild Project 来 build artifacts, 以及生成最终的 CloudFormation Template, 然后就直接调用 AWS CloudFormation 来部署了. 之后就再也不需要用 CodeBuild 了, 实现了部署阶段的并行执行.

由于 CDK Pipeline 不是一个传统意义上的 CI/CD 系统, 它不提供 Terminal Command 的编排, 运行时的编排等, 这些工作都是在 CodeBuild 中进行, 但是 CDK Pipeline 提供了一套语法允许你定义 CodeBuild 中的编排. 然后 CDK Pipeline 会自动更新这个 CodeBuild Project 然后在里面运行.


2. 什么时候该用 CDK Pipeline
------------------------------------------------------------------------------
如果你的部署任务可以通过 CDK 来完成, 例如发布一个 Lambda 版本, 发布一个 ECS Task 的版本等, 那么完全可以用 CDK Pipeline.


3. CDK Pipeline 的工作原理
------------------------------------------------------------------------------
这里我们来看一个使用 CDK Pipeline 从 CodeCommit 中拉取代码, 部署 Lambda Function 的例子. 本例的源代码都在 `GitHub <https://github.com/MacHu-GWU/Dev-Exp-Share/tree/master/docs/source/02-SDE/01-Program-Language/02-Python-Root/Awesome-Python-Library-for-Software-Development/aws_cdk/learn_cdk_pipeline-project>`_ 上.

首先, 我们来了解一下 CDK Pipeline 作为一个 IAC 工具是如何实现 CI/CD 的. 前面我们介绍了 CI/CD 系统包括两个部分:

1. CI/CD 系统的基础设施, 包括 CodeBuild Project 用于提供运行环境, CodePipeline 用于提供编排, S3 Bucket 用于存放 Artifacts, Event Rule 用来定义触发规则, 以及一些 IAM Role Policy 来管理权限.
2. CI/CD 系统的具体运行逻辑, 由一堆 Terminal Command 和 CodePipeline Stage / Action 组成.

CDK Pipeline 能自动的创建 #1, 并且允许用户自定义 #2. 由于 CDK 本身使用 TypeScript 实现的, #1 的创建是由一堆 If Else 逻辑来自动生成的. 而 #2 的自定义是通过 CodePipeline 中的 Stage Action, 以及 CodeBuild Job 中的 Command 来实现的. 基本上实现了用户在其他 CI/CD 系统中使用的任何 Terminal Command 都可以在 CDK Pipeline 中实现.

然后我们来看一个标准的用 CDK Pipeline 开发和部署的流程, 示例代码我们之后再分析:

1. 首先你需要用 CDK Pipeline 定义一个 ``Pipeline`` Construct, 然后用 ``cdk deploy`` 命令部署一次. 该次部署会将所有的 CI/CD 所需的基础设施都部署好. 这一步是必须的, 而且要在你部署真正的 App 应用之前做. 一旦部署好, 你对 Pipeline 本身的基础设施的定义的修改都会被这个 Pipeline 自己所更新.
2. 接下来你就可以专注于开发你的 App 了, 然后你只要 push 代码到 CodeCommit, 这个 CodePipeline 都会自动运行来部署. 当然我们这里只用到了一个 branch, 仅仅是一个示例. 生产环境中会有很多个 branch, 这个我们在本文中不做讨论.

下面是一个 CDK Pipeline 的示例代码, 请仔细阅读里面的注释部分:

.. literalinclude:: ./app.py
   :language: python
   :linenos:

最后来看一下 CDK Pipeline 中关于 #1 的基础设施部分 (被自动创建的部分) 包含哪些内容:

    这个是 CDK 的 Metadata, 不用管.

    - CDKMetadata (AWS::CDK::Metadata)

    这个是 CodePipeline 以及它的 Service Role 的定义.

    - Pipeline9850B417 (AWS::CodePipeline::Pipeline)
    - PipelineRoleB27FAA37 (AWS::IAM::Role)
    - PipelineRoleDefaultPolicy7BDC1ABB (AWS::IAM::Policy)

    这个是第一个 CodeBuild Project, 用来构建最终所需的 CloudFormation template. 这个 CodeBuild Project 最为重要, 你所需要的 CI/CD 的逻辑, 权限都在这里被定义. 跟其他 CI/CD 不同的事

    - PipelineBuildSynthCdkBuildProject6BEFA8E6 (AWS::CodeBuild::Project)
    - PipelineBuildSynthCdkBuildProjectRole231EEA2A (AWS::IAM::Role)
    - PipelineBuildSynthCdkBuildProjectRoleDefaultPolicyFB6C941C (AWS::IAM::Policy)

    这个是第二个 CodeBuild Project, 用来更新这个 CodePipeline 本身.

    - PipelineUpdatePipelineSelfMutationDAA41400 (AWS::CodeBuild::Project)
    - PipelineUpdatePipelineSelfMutationRole57E559E8 (AWS::IAM::Role)
    - PipelineUpdatePipelineSelfMutationRoleDefaultPolicyA225DA4E (AWS::IAM::Policy)

    这是一个用来给 Pipeline Role 来 Assume 的 Role, 使得 Pipeline 能调用 CodeBuild 的 API 来运行 Build Job Run.

    - PipelineCodeBuildActionRole226DB0CB (AWS::IAM::Role)
    - PipelineCodeBuildActionRoleDefaultPolicy1D62A6FE (AWS::IAM::Policy)

    这是一个用来给 AWS Account 来 Assume, 允许从 CodeCommit check out 源代码的 Role:

    - PipelineSourcelearncdkcodepipelineprojectCodePipelineActionRole3D2ABC00 (AWS::IAM::Role)
    - PipelineSourcelearncdkcodepipelineprojectCodePipelineActionRoleDefaultPolicy9C23C694 (AWS::IAM::Policy)

    这是一个用来给 CodePipeline Approval Action 的 Role, 我研究不深, 还不是很清楚:

    - PipelineDeployLambdaFunctionApprovalCodePipelineActionRoleFA32B3F2 (AWS::IAM::Role)

    这是 CodePipeline 用来监控 CodeCommit 的 Event Rule:

    - RepoMyPipelineStackPipeline61E383C6mainEventRule0B20E01C (AWS::Events::Rule)
    - PipelineEventsRole96280D9B (AWS::IAM::Role)
    - PipelineEventsRoleDefaultPolicy62809D8F (AWS::IAM::Policy)

    这是用来保存 Artifacts 的 S3 Bucket:

    - PipelineArtifactsBucketAEA9A052 (AWS::S3::Bucket)
    - PipelineArtifactsBucketPolicyF53CCC52 (AWS::S3::BucketPolicy)


4. Multi Branch 情况下如何使用 CDK Pipeline
------------------------------------------------------------------------------
1. 由于一个 CodePipeline 只能监控一个 Branch, 所以如果你想要为许多名字不可预测的 Branch 来创建 CDK Pipeline, 那么我们在本地第一次运行 ``cdk deploy "*"`` 这个动作就需要在每次创建新的符合规则的 Branch 时进行. 我们可以为 CodeCommit 创建一个 Event Rule, 然后监控创建和删除特定的 Branch 的事件, 然后用 Lambda Function 来执行 ``cdk deploy "*"`` 命令.
2. 由于每个 Branch 所对应的 CDK Pipeline 都会创建 20 多个的资源, 很容易让 Bucket, CodeProject, CodePipeline 的数量爆炸. 所以在 Branch 被删除后, 如何清理掉 App Stack 以及 Pipeline Stack 就需要小心设计. 这个 Lambda 需要先删除 App Stack, 然后再删除 Pipeline Stack.



Reference
------------------------------------------------------------------------------
- `Continuous integration and delivery (CI/CD) using CDK Pipelines <https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html>`_: AWS CDK Pipeline 的官方文档, 介绍了如何使用 CDK Pipeline 来实现 CI/CD.
- `CDK Pipelines <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html>`_: CDK Python 中的 ``aws_cdk.pipelines.CodePipeline`` 类相关的 API 文档.
- `CDK Pipelines: Continuous delivery for AWS CDK applications <https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/>`_: 一篇介绍 CDK Pipeline 的 AWS 博客文章.
- `Parallel and dynamic SaaS deployments with AWS CDK Pipelines <https://aws.amazon.com/blogs/devops/parallel-and-dynamic-saas-deployments-with-cdk-pipelines/>`_: 一篇介绍如何让 CDK Pipeline 支持动态的, 参数化的部署的 AWS 博客文章. 最好对 AWS CDK Pipeline 有一定了解之后再看.
- `Multi-branch pipeline management and infrastructure deployment using AWS CDK Pipelines <https://aws.amazon.com/blogs/devops/multi-branch-pipeline-management-and-infrastructure-deployment-using-aws-cdk-pipelines/>`_: 一篇介绍多个 Branch 的情况下如何用 CDK Pipeline 来部署应用的 AWS 博客文章. 最好对 AWS CDK Pipeline 有一定了解之后再看.