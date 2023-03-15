Multi-account model deployment with Amazon SageMaker Pipelines
==============================================================================
本文档是我精读并且实践这篇 `AWS Blog <https://aws.amazon.com/blogs/machine-learning/multi-account-model-deployment-with-amazon-sagemaker-pipelines/>`_ 的笔记.


AWS Account Setup
------------------------------------------------------------------------------
这篇博客中用到了三个 Account, 分别是:

- Data Scientist Account: 用来部署 SageMaker Domain 和 SageMaker Studio. 模型的开发, 训练, 评估, 注册, pipeline 都在这个 Account 上.
- Staging Account: 用来将 Data Scientist Account 中注册号的模型部署到 Staging Account 中的 SageMaker Endpoint 上. 相当于是做 Integration Test 的环境.
- Production Account: 模型在 Staging 中运行良好测试通过后, 就被部署到 Production Account 上.

这篇博客中的 AWS Organizations Structure 如下:

- **Root Account (management account)**: Data Scientist Account 是 root account. 在实际的企业场景中, 一般不可能用 Data Scientist Account 来做 Root Account, 通常 Root Account 上不应该 run 任何业务逻辑的, 甚至不该 run CloudFormation. 根据作者 Samir Araujo 给我的回复, 他的最佳实践中有一步用 CodePipeline 来 deploy CloudFormation StackSet. 正常情况下只要这个 CodePipeline 的 Account 被指定为 delegated administrator 即可. 可这里有个 Bug 导致 CodePipeline 的 Account 必须是 Root 才醒. 所以这个 Blog 中为了演示, 最终把 Data Scientist Account 当做 Root Account 用了.
- **Staging OU**: Staging Account 在这个 OU 里. 根据 `Recommended OUs and accounts <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/recommended-ous-and-accounts.html>`_ 和 `Organizing workload-oriented OUs <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-workload-oriented-ous.html>`_ 这两篇文档, 我们使用的算是 function-oriented OU Strategy, 而没有用 workload-oriented OU Strategy.

所有的部署都是由 Data Scientist 上的 Code Pipeline 发起的. 然后通过 StackSet 将模型部署到 Staging 和 Production Account 中.

**下面我们来介绍一下具体要做的事情**:

按照下面的 Organization Structure 配置你的 AWS Organization 和 AWS Accounts::

    root
    |--- data scientist account
    |--- staging OU
        |--- staging account
    |--- production OU
        |--- production account


Prepare SageMaker Studio Domain
------------------------------------------------------------------------------
这篇博客并没有给出具体步骤. 你就按照 SageMaker domain 的官方文档, 用默认的 default VPC setup 就可以. 当然在企业环境中通常要用 VPC Only Mode. 这里我们不展开讨论.

在第一次创建 SageMaker domain 的时候会要求你创建一个给 Domain, Studio, Canvas 用的 Role. 我一般选择让系统来创建而不是自己手动创建. 这个 Role 默认只有 ``AmazonSageMakerFullAccess`` 和 ``AmazonSageMakerCanvasFullAccess`` 两个 Policy. 你的 Domain 和 Studio 就是用这个 Role.

你创建好 SageMaker domain 之后, 会有如下这些 Role 自动地被创建出来. 这些都是 SageMaker studio 会用来调用其他服务的 Role. 你如果删除了这些 Role 对应的功能就用不了. 举例来说, SageMaker 可能运行 Glue job, 凡是由 SageMaker 发起的 Glue job 就会使用 ``AmazonSageMakerServiceCatalogProductsGlueRole`` 作为 Glue job execution 的权限.

- ``AmazonSagemakerCanvasForecastRole-1678741978247``: forecast
- ``AmazonSageMakerServiceCatalogProductsApiGatewayRole``: apigateway
- ``AmazonSageMakerServiceCatalogProductsCloudformationRole``: cloudformation
- ``AmazonSageMakerServiceCatalogProductsCodeBuildRole``: codebuild
- ``AmazonSageMakerServiceCatalogProductsCodePipelineRole``: codepipeline
- ``AmazonSageMakerServiceCatalogProductsEventsRole``: events
- ``AmazonSageMakerServiceCatalogProductsExecutionRole``: sagemaker
- ``AmazonSageMakerServiceCatalogProductsFirehoseRole``: firehose
- ``AmazonSageMakerServiceCatalogProductsGlueRole``: glue
- ``AmazonSageMakerServiceCatalogProductsLambdaRole``: lambda
- ``AmazonSageMakerServiceCatalogProductsLaunchRole``: servicecatalog
- ``AmazonSageMakerServiceCatalogProductsUseRole``: sagemaker, cloudformation, glue, apigateway, lambda, states, events, firehose, codepipeline, codebuild.
- ``AWSServiceRoleForAmazonSageMakerNotebooks``: sagemaker (Service-Linked Role)

在本篇文章中比较重要的就两个 Role:

- ``AmazonSageMakerServiceCatalogProductsLaunchRole``: Service Catalog 要用这个 Role 来创建一些 AWS Resources.
- ``AmazonSageMakerServiceCatalogProductsUseRole``: 这些 AWS Service 要用这些 role 来干一些活. 例如 Codebuild 要用这个 role 来 run build job.

还有一个有用的工具值得注意, SageMaker 有个 getting started menu 有一个 ``Create Role`` wizard. 可以帮你为不同的 Personal 用图形化的方式创建 IAM Role. 创建出来的 Role 的名字像是 ``SageMaker-${suffix}`` 这种.

除了以上这些 Role, 还会有一个名字为 ``sagemaker-${aws_region}-${aws_account_id}`` 这样的 S3 Bucket 被自动创建. SageMaker studio 的 SDK 在创建 sagemaker session 的时候会默认使用这个 bucket 来 host 你在 Data Scientist Account 上训练好的模型 (的 Artifacts). 可以预见, 你的 Staging Account 和 Production Account 也会用到这些 Artifacts. 所以我们要在 Bucket Policy 中定义好访问权限::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::${staging_account_id}:root",
                        "arn:aws:iam::${production_account_id}:root"
                    ]
                },
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::sagemaker-${aws_region}-${aws_account_id}",
                    "arn:aws:s3:::sagemaker-${aws_region}-${aws_account_id}/*"
                ]
            }
        ]
    }

接下来要给 ``AmazonSageMakerServiceCatalogProductsUseRole`` 一些权限. 这个 Role 是给 Service Catalog 来 deploy CloudFormation StackSet 用的, 所以你需要一些 CloudFormation 的权限. 我们给它创建一个 inline policy::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "cloudformation:Delete*",
                    "cloudformation:Get*",
                    "cloudformation:Create*",
                    "cloudformation:Update*",
                    "cloudformation:List*",
                    "cloudformation:Describe*"
                ],
                "Resource": [
                    "arn:aws:cloudformation:*:*:stack/sagemaker-*",
                    "arn:aws:cloudformation:*:*:stackset/sagemaker-*",
                    "arn:aws:cloudformation:*:*:type/resource/*",
                    "arn:aws:cloudformation:*:*:stackset-target/sagemaker-*"
                ]
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": [
                    "cloudformation:GetTemplate",
                    "cloudformation:GetTemplateSummary",
                    "cloudformation:TagResource"
                ],
                "Resource": "*"
            },
            {
                "Sid": "VisualEditor2",
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Resource": ["arn:aws:iam::*:role/sagemaker-*"]
            },
            {
                "Sid": "VisualEditor3",
                "Effect": "Allow",
                "Action": [
                    "organizations:DescribeOrganizationalUnit",
                    "organizations:ListAccountsForParent"
                ],
                "Resource": [
                    "arn:aws:organizations::*:ou/o-*/ou-*"
                ]
            }
        ]
    }


接下来我们要给 ``AmazonSageMakerServiceCatalogProductsLaunchRole`` 一些权限, 使得它能从 AWS Blog 用来 host artifacts 的 bucket 上下载东西. 我们给它创建一个 inline policy::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::aws-ml-blog/artifacts/sagemaker-pipeline-blog-resources/*"
            }
        ]
    }

至此 Data Scientist Account 的准备工作已经做的差不多了, 还有一些工作我们需要之后做. 接下来就是要切换到 Staging Account 和 Prod Account 上做事情了


Setup IAM Role in Staging and Prod Account
------------------------------------------------------------------------------
这一步要在 Staging 和 Prod Account 上创建 IAM Role. 这篇博客是用的 CloudFormation 的方式来创建 IAM Role 的, 当然你也可以手动创建. 下面是 Staging 和 Production Account 所需要运行的 CloudFormation Template 的内容. 阅读定义可知里面只定义了 1 个 IAM Role ``sagemaker-role-${SageMakerRoleSuffix}``. 这个 Role 是给位于 Data Scientist Account 上的 pipeline execution role, 也就是前一节里的 ``AmazonSageMakerServiceCatalogProductsUseRole`` 来使用的. 而 pipeline 要做的事情有 Deploy Model, Endpoint 等等, 所以你可以看到这个 Template 里给的权限主要是 Deploy 相关的权限. 还有一个 S3 Read Only 的权限, 这个权限是用来从 Data Scientist Account 上的 S3 Bucket 里读取 Artifacts 的. 前一节里的 S3 Bucket Policy 中已经做了定义了.

.. code-block:: yml

    Parameters:
        SageMakerRoleSuffix:
            Type: String
            Description: Suffix of the SageMaker Execution role
            MinLength: 1
            MaxLength: 15
            AllowedPattern: ^[a-zA-Z](-*[a-zA-Z0-9])*
        PipelineExecutionRoleArn:
            Type: String
            Description: Id of the main account
    Resources:
        SageMakerCrossRole:
            Type: AWS::IAM::Role
            Properties:
                RoleName: !Sub "sagemaker-role-${SageMakerRoleSuffix}"
                AssumeRolePolicyDocument:
                    Version: "2012-10-17"
                    Statement:
                        -
                            Effect: "Allow"
                            Principal:
                                Service:
                                    - "sagemaker.amazonaws.com"
                            Action:
                                - "sts:AssumeRole"
                        -
                            Effect: "Allow"
                            Principal:
                                AWS: !Sub ${PipelineExecutionRoleArn}
                            Action:
                                - "sts:AssumeRole"
                Path: "/"
                ManagedPolicyArns:
                    - arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
                Policies:
                    -
                        PolicyName: !Sub "sagemaker-policy-${SageMakerRoleSuffix}"
                        PolicyDocument:
                            Version: "2012-10-17"
                            Statement:
                                -
                                    Effect: "Allow"
                                    Action:
                                        - "sagemaker:*Model"
                                        - "sagemaker:*EndpointConfig"
                                        - "sagemaker:*Endpoint"
                                    Resource:
                                        - !Sub "arn:aws:sagemaker:*:${AWS::AccountId}:endpoint/*"
                                        - !Sub "arn:aws:sagemaker:*:${AWS::AccountId}:endpoint-config/*"
                                        - !Sub "arn:aws:sagemaker:*:${AWS::AccountId}:model/*"


Importing the custom SageMaker Studio project template
------------------------------------------------------------------------------
我们之后要为 Data Scientist 创建一个标准化的 Project Template. 而所谓 SageMaker Project Template 本质上是 AWS Service Catalog 里的一个 Product. 如果你不了解 Service Catalog 这个服务, 你得先去 `Overview of Service Catalog <https://docs.aws.amazon.com/servicecatalog/latest/adminguide/what-is_concepts.html>`_ 了解一下基本概念. 本质上 Service Catalog 就是对 CloudFormation 的封装, 把 CloudFormation 包装成一个个的 Product, 然后 多个 Product 组成一个 Portfolio, 这里面加上了版本管理, 权限管理等等功能, 就变成了 Service Catalog.

所以所谓 Importing the custom SageMaker Studio project template 就是在 Data Scientist Account 的 Service Catalog 中创建一个 Product, 里面包含了一个 SageMaker project 所需要的一切东西.

这一段步骤比较简单, 但是里面的 CloudFormation Template 值得好好研究. 下面是 Template 的内容 (很长). 这里我不在文档里做解释了, 直接在 Template 里面写注释来解说好了::

    Description: Toolchain template which provides the resources needed to represent infrastructure as code.
      This template specifically creates a CI/CD pipeline to deploy a given inference image and pretrained Model to two stages in CD -- staging and production.

    Parameters:
      SageMakerProjectName:
        Type: String
        Description: Name of the project
        MinLength: 1
        MaxLength: 32
        AllowedPattern: ^[a-zA-Z](-*[a-zA-Z0-9])*

      SageMakerProjectId:
        Type: String
        Description: Service generated Id of the project.

      SageMakerExecutionRoleStagingName:
        Type: String
        Description: Name of the role created in the Staging account used by SageMaker to deploy the model
        MinLength: 1
        MaxLength: 64
        AllowedPattern: ^[a-zA-Z](-*[a-zA-Z0-9])*
      SageMakerExecutionRoleProdName:
        Type: String
        Description: Name of the role created in the Prod account used by SageMaker to deploy the model
        MinLength: 1
        MaxLength: 64
        AllowedPattern: ^[a-zA-Z](-*[a-zA-Z0-9])*

      OrganizationalUnitStagingId:
        Type: String
        Description: Id of the organizational unit that holds the staging account
      OrganizationalUnitProdId:
        Type: String
        Description: Id of the organizational unit that holds the prod account


    Resources:
      # 给每一个 SageMaker project 创建一个单独的 S3 bucket, 用来存放 artifacts
      # 我个人不喜欢这么做, 因为如果项目很多的化很容易到达 S3 bucket 的上线. 这么做
      # 当然有它的好处, 比如每个 bucket 的权限分离, 避免一个 ML 项目的人影响其他项目的人.
      # 我个人喜欢给一个 S3 bucket 下面创建很多 folder. 然后 IAM 里面自动生成一些
      # 访问 folder 所需的权限. 各有利弊, 你可以自己决定.
      MlOpsArtifactsBucket:
        Type: AWS::S3::Bucket
        DeletionPolicy: Retain
        Properties:
          BucketName: !Sub sagemaker-project-${SageMakerProjectId} # 58 chars max/ 64 allowed

      # 这是一个 Event Rule, 定义了每当 SageMaker Model Package 有变化的时候 (release 了新版本)
      # 就自动运行 CodePipeline 来将新的版本 push 到 stage 进而 push 到 prod.
      ModelDeploySageMakerEventRule:
        Type: AWS::Events::Rule
        Properties:
          # Max length allowed: 64
          Name: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-model # max: 10+33+15+5=63 chars
          Description: "Rule to trigger a deployment when SageMaker Model registry is updated with a new model package. For example, a new model package is registered with Registry"
          EventPattern:
            source:
              - "aws.sagemaker"
            detail-type:
              - "SageMaker Model Package State Change"
            detail:
              ModelPackageGroupName:
                - !Ref SageMakerProjectName
          State: "ENABLED"
          Targets:
            -
              Arn:
                !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'codepipeline', !Ref 'AWS::Region', !Ref 'AWS::AccountId', !Ref ModelDeployPipeline ] ]
              RoleArn:
                !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'iam:', !Ref 'AWS::AccountId', 'role/service-role/AmazonSageMakerServiceCatalogProductsUseRole'] ]
              Id: !Sub sagemaker-${SageMakerProjectName}-trigger

      # 这是一个 Event Rule, 定义了每当 CodeCommit repo 的 main branch 有变化的时候
      # 就自动运行 CodePipeline 来将的版本 push 到 stage 进而 push 到 prod.
      ModelDeployCodeCommitEventRule:
        Type: AWS::Events::Rule
        Properties:
          # Max length allowed: 64
          Name: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-code # max: 10+33+15+4=62 chars
          Description: "Rule to trigger a deployment when CodeCommit is updated with a commit"
          EventPattern:
            source:
              - "aws.codecommit"
            detail-type:
              - "CodeCommit Repository State Change"
            resources:
              - !GetAtt ModelDeployCodeCommitRepository.Arn
            detail:
              referenceType:
                - "branch"
              referenceName:
                - "main"
          State: "ENABLED"
          Targets:
            -
              Arn:
                !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'codepipeline', !Ref 'AWS::Region', !Ref 'AWS::AccountId', !Ref ModelDeployPipeline ] ]
              RoleArn:
                !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'iam:', !Ref 'AWS::AccountId', 'role/service-role/AmazonSageMakerServiceCatalogProductsUseRole'] ]
              Id: !Sub codecommit-${SageMakerProjectName}-trigger

      # 创建一个 CodeCommit repo, 用来存放 ModelDeploy 和 CI/CD 的代码
      # 这个代码库是 host 在 ``aws-ml-blog`` 这个 bucket 上的. 你可以自己 download 代码下来看一下
      # 这里不详细解读, 到后面再详细说代码. 简单来说就是具体的 build, test, deploy shell script
      # 都是在这个代码库里面实现的. 这个也是一个比较好的实践, 你能用这个方法初始化一个 AWS CodeCommit Repo
      # 结合 python cookiecutter, 可以玩出花来
      ModelDeployCodeCommitRepository:
        Type: AWS::CodeCommit::Repository
        Properties:
          # Max allowed length: 100 chars
          RepositoryName: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-modeldeploy # max: 10+33+15+11=69
          RepositoryDescription: !Sub SageMaker Endpoint deployment infrastructure as code for the Project ${SageMakerProjectName}
          Code:
            S3:
              Bucket: aws-ml-blog
              Key: artifacts/sagemaker-pipeline-blog-resources/multi-account-deployment-v1.0.zip
            BranchName: main

      # 这是一个 Code Build Project, 每个 SageMaker Project 有两个 Projects
      # 这个是用来 build 输出 artifacts 以供下一个 Build Project 使用的
      # 具体的逻辑在 buildspec.yml 里面. 我们之后再详细说. 简单来说这个就是生成一个
      # Cfn template, 以及各 staging 和 prod 的 config json 文件
      ModelDeployBuildProject:
        Type: AWS::CodeBuild::Project
        Properties:
          # Max length: 255 chars
          Name: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-modeldeploy # max: 10+33+15+11=69
          Description: Builds the Cfn template which defines the Endpoint with specified configuration
          ServiceRole:
            !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'iam:', !Ref 'AWS::AccountId', 'role/service-role/AmazonSageMakerServiceCatalogProductsUseRole'] ]
          Artifacts:
            Type: CODEPIPELINE
          Environment:
            Type: LINUX_CONTAINER
            ComputeType: BUILD_GENERAL1_SMALL
            Image: aws/codebuild/amazonlinux2-x86_64-standard:3.0
            EnvironmentVariables:
             - Name: SAGEMAKER_PROJECT_NAME
               Value: !Ref SageMakerProjectName
             - Name: SAGEMAKER_PROJECT_ID
               Value: !Ref SageMakerProjectId
             - Name: ARTIFACT_BUCKET
               Value: !Ref MlOpsArtifactsBucket
             - Name: SOURCE_MODEL_PACKAGE_GROUP_NAME
               Value: !Ref SageMakerProjectName
             - Name: AWS_REGION
               Value: !Ref AWS::Region
             # these values are used by the build system to output to the output artifacts.
             # further down, we use these names in the Cfn deployment steps
             - Name: EXPORT_TEMPLATE_NAME
               Value: template-export.yml
             - Name: EXPORT_TEMPLATE_STAGING_CONFIG
               Value: staging-config-export.json
             - Name: EXPORT_TEMPLATE_PROD_CONFIG
               Value: prod-config-export.json
             - Name: SAGEMAKER_EXECUTION_ROLE_STAGING_NAME
               Value: !Ref SageMakerExecutionRoleStagingName
             - Name: SAGEMAKER_EXECUTION_ROLE_PROD_NAME
               Value: !Ref SageMakerExecutionRoleProdName
             - Name: ORGANIZATIONAL_UNIT_STAGING_ID
               Value: !Ref OrganizationalUnitStagingId
             - Name: ORGANIZATIONAL_UNIT_PROD_ID
               Value: !Ref OrganizationalUnitProdId

          Source:
            Type: CODEPIPELINE
            BuildSpec: buildspec.yml
          TimeoutInMinutes: 30

      # 这是一个 Code Build Project, 每个 SageMaker Project 有两个 Projects
      # 这个是基于前一个 build job 输出的 artifacts, 来将 model deploy 到
      # staging 和 prod 中去的
      ModelDeployTestProject:
        Type: AWS::CodeBuild::Project
        Properties:
          # Max length: 255 chars
          Name: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-testing # max: 10+33+15+7=65
          Description: Test the deployment endpoint
          ServiceRole:
            !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'iam:', !Ref 'AWS::AccountId', 'role/service-role/AmazonSageMakerServiceCatalogProductsUseRole'] ]
          Artifacts:
            Type: CODEPIPELINE
          Environment:
            Type: LINUX_CONTAINER
            ComputeType: BUILD_GENERAL1_SMALL
            Image: "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
            EnvironmentVariables:
              - Name: SAGEMAKER_PROJECT_NAME
                Value: !Ref SageMakerProjectName
              - Name: SAGEMAKER_PROJECT_ID
                Value: !Ref SageMakerProjectId
              - Name: AWS_REGION
                Value: !Ref "AWS::Region"
              - Name: BUILD_CONFIG
                Value: staging-config-export.json
              - Name: EXPORT_TEST_RESULTS
                Value: test-results.json
              - Name: SAGEMAKER_EXECUTION_ROLE_NAME
                Value: !Ref SageMakerExecutionRoleStagingName
              - Name: ORGANIZATIONAL_UNIT_ID
                Value: !Ref OrganizationalUnitStagingId
          Source:
            Type: CODEPIPELINE
            BuildSpec: test/buildspec.yml
          TimeoutInMinutes: 30

      # 这是这个 Solution 的重中之重, 也是最复杂的部分
      # 这是 AWS CodePipeline 的定义, 里面包含了多个步骤
      # 我们来详细看一看每个步骤
      ModelDeployPipeline:
        Type: AWS::CodePipeline::Pipeline
        DependsOn: MlOpsArtifactsBucket
        Properties:
          # Max length: 100 chars
          Name: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-modeldeploy # max: 10+33+15+11=69
          RoleArn:
            !Join [ ':', [ 'arn', !Ref 'AWS::Partition', 'iam:', !Ref 'AWS::AccountId', 'role/service-role/AmazonSageMakerServiceCatalogProductsUseRole'] ]
          ArtifactStore:
            Type: S3
            Location:
              !Ref MlOpsArtifactsBucket
          Stages:
            # 这是第一步, check out source
            - Name: Source
              Actions:
                - Name: ModelDeployInfraCode
                  ActionTypeId:
                    Category: Source
                    Owner: AWS
                    Provider: CodeCommit
                    Version: 1
                  Configuration:
                    # need to explicitly set this to false per https://docs.aws.amazon.com/codepipeline/latest/userguide/update-change-detection.html
                    PollForSourceChanges: false
                    RepositoryName: !GetAtt ModelDeployCodeCommitRepository.Name
                    BranchName: main
                  OutputArtifacts:
                    - Name: SourceArtifact
            # 这一步是运行 ModelDeployBuildProject, 也就是第一个 CodeBuild Project
            - Name: Build
              Actions:
                - Name: BuildDeploymentTemplates
                  ActionTypeId:
                    Category: Build
                    Owner: AWS
                    Provider: CodeBuild
                    Version: 1
                  InputArtifacts:
                    - Name: SourceArtifact
                  OutputArtifacts:
                    - Name: BuildArtifact
                  Configuration:
                    ProjectName: !Ref ModelDeployBuildProject
                  RunOrder: 1

            # 这一步是将 ModelDeployBuildProject 输出的 Artifacts, 也就是 Cfn Template
            # 和 staging config file 用 CloudFormation StackSet 的形式
            # 部署到 staging 上. 这一步是用 CodePipeline 来 run CloudFormation API
            # 只不过你不用写代码了
            - Name: DeployResourcesStaging
              Actions:
                # action 1, deploy cfn StackSet
                - Name: DeployStaging
                  InputArtifacts:
                    - Name: BuildArtifact
                  ActionTypeId:
                    Category: Deploy
                    Owner: AWS
                    Version: 1
                    Provider: CloudFormationStackSet
                  Configuration:
                    Capabilities: CAPABILITY_NAMED_IAM
                    PermissionModel: SERVICE_MANAGED
                    OrganizationsAutoDeployment: Disabled
                    StackSetName: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-deploy-staging  #10+33+15+14=72 out of 128 max
                    Parameters: BuildArtifact::staging-config-export.json
                    # The buildspec.yml in the application stack uses this file name,
                    TemplatePath: BuildArtifact::template-export.yml
                    DeploymentTargets: !Ref OrganizationalUnitStagingId
                    Regions: !Ref 'AWS::Region'
                  RunOrder: 1
                # action 2, 运行 ModelDeployTestProject, 也就是第二个 CodeBuild Project
                - Name: TestStaging
                  ActionTypeId:
                    Category: Build
                    Owner: AWS
                    Provider: CodeBuild
                    Version: 1
                  InputArtifacts:
                    - Name: SourceArtifact
                    - Name: BuildArtifact
                  OutputArtifacts:
                    - Name: TestArtifact
                  Configuration:
                    ProjectName: !Ref ModelDeployTestProject
                    PrimarySource: SourceArtifact
                  RunOrder: 2
                # action 3, 等待人工 approval, 只有 approval 了之后才会部署到 prod
                - Name: ApproveDeployment
                  ActionTypeId:
                    Category: Approval
                    Owner: AWS
                    Version: 1
                    Provider: Manual
                  Configuration:
                    CustomData: "Approve this model for Production"
                  RunOrder: 3
            # 这一步是将 ModelDeployBuildProject 输出的 Artifacts, 也就是 Cfn Template
            # 和 prod config file 用 CloudFormation StackSet 的形式
            # 部署到 prod 上. 这一步是用 CodePipeline 来 run CloudFormation API
            # 只不过你不用写代码了
            - Name: DeployResourcesProd
              Actions:
                - Name: DeployProd
                  InputArtifacts:
                    - Name: BuildArtifact
                  ActionTypeId:
                    Category: Deploy
                    Owner: AWS
                    Version: 1
                    Provider: CloudFormationStackSet
                  Configuration:
                    Capabilities: CAPABILITY_NAMED_IAM
                    PermissionModel: SERVICE_MANAGED
                    OrganizationsAutoDeployment: Disabled
                    StackSetName: !Sub sagemaker-${SageMakerProjectName}-${SageMakerProjectId}-deploy-prod  #10+33+15+14=72 out of 128 max
                    Parameters: BuildArtifact::prod-config-export.json
                    TemplatePath: BuildArtifact::template-export.yml
                    DeploymentTargets: !Ref OrganizationalUnitProdId
                    Regions: !Ref 'AWS::Region'
                  RunOrder: 1


Conclusion
------------------------------------------------------------------------------
TODO