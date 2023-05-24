#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    CodeBuildStep,
    ManualApprovalStep,
)
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_codecommit as codecommit
from constructs import Construct


# 定义了你的 Application Stack, 这里我们是一个 Lambda Function.
class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.my_lambda_function = lambda_.Function(
            self,
            "LambdaFunction",
            function_name="learn_cdk_pipeline-my_lambda_function",
            runtime=lambda_.Runtime.NODEJS_18_X,
            handler="index.handler",
            # 这是一个 POC, 所以为了方便起见我们直接 Hard code 源代码
            code=lambda_.InlineCode("exports.handler = _ => 'Hello, CDK';"),
        )


# 将 Application Stack 包装成一个 Pipeline 中的 Stage
# 将 Application Stack 包装成一个 Pipeline 中的 Stage
# 这个 Stage 需要用 MyPipelineStack.CodePipeline.CodeBuildStep 里面创建的
# CloudFormation Template asset 来作为输入, 不过这个 CDK Pipeline 会帮你 handle
class MyPipelineAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.my_lambda_stack = MyLambdaStack(
            self,
            "LambdaStack",
            stack_name="learn-cdk-pipeline-my-lambda-stack",
        )


# 这就是 CDK Pipeline 的 Stack
class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 这个 aws_cdk.pipelines.CodePipeline 跟 aws_cdk.aws_codepipeline.Pipeline 不同
        # 它是一个 CDK 团队开发的 Construct 里面包含了 Pipeline 运行所需的 Infrastructure
        self.pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name="learn-cdk-pipeline-my-pipeline",
            # 这一步最为关键, 它定义了构建部署所需的全部 CloudFormation 的逻辑
            # 为了灵活性, 我们一般在 CodeBuild 中来运行这些逻辑
            synth=CodeBuildStep(
                "Synth",
                project_name="learn-cdk-pipeline-my-pipeline-synth",
                # 这里定义了从哪里拉取源代码
                input=CodePipelineSource.code_commit(
                    codecommit.Repository.from_repository_name(
                        self,
                        "Repo",
                        repository_name="learn_cdk_codepipeline-project",
                    ),
                    branch="main",
                ),
                # 这里定义了 CodeBuild 的 IAM Role 需要的额外 Permission
                role_policy_statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["*"],
                        resources=["*"],
                    )
                ],
                # 这里定义了 CodeBuild 的构建逻辑, 其中最关键的是 cdk synth
                # 你可以在它之前或者之后添加任意的构建逻辑
                install_commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                ],
                commands=[
                    "cdk synth",
                ],
                # 这个步骤会是会将 cdk 生成的 CloudFormation 打包成 Artifacts 的
                # 默认是 cdk.out 目录, 你也可以修改这个路径
                # primary_output_directory="/path/to/cdk.out",
            ),
        )

        # 这一步定义了 Application Deployment 的 Stage 的逻辑, 其内容是我们之前用
        # Stage 包装好的 AppStack
        # 注意, 这里的 my_pipeline_app_stage_deployment 返回值不是 Stage 本身
        # 而是一个 StageDeployment 对象, 它有 add_pre, add_post 方法.
        self.my_pipeline_app_stage_deployment = self.pipeline.add_stage(
            MyPipelineAppStage(
                self,
                "MyPipelineAppStage",
                stage_name="Deploy-Lambda-Function",
            )
        )

        # 你可以通过 add_pre, add_post 方法来添加任意的构建逻辑
        # 我推荐使用 CodeBuildStep 来添加构建逻辑, 而不要用 ShellStep,
        # 因为 ShellStep 本身也会被包装成 CodeBuildStep 来执行
        # 注意每当你定义一个 CodeBuildStep 就会让 CodePipeline 创建一个新的 CodeBuild Project
        # 这些 CodeBuild Project 的 Build job run 之间相互独立
        # 如果你需要传递数据的话, 你需要用 CodePipeline 的 Artifact 来传递
        self.my_pipeline_app_stage_deployment.add_pre(
            CodeBuildStep(
                "PreAppStageStep",
                project_name="learn-cdk-pipeline-my-pipeline-pre-app-stage-step",
                commands=[
                    "echo 'PreAppStageStep'",
                    "env",
                ],
            )
        )
        self.my_pipeline_app_stage_deployment.add_post(
            ManualApprovalStep("Approval"),
        )


app = cdk.App()
MyPipelineStack(app, "MyPipelineStack", stack_name="my-pipeline-stack")
app.synth()
