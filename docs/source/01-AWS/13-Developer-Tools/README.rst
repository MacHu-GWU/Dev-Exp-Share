AWS - Developer Tools Root
==============================================================================
Keywords:


Summary
------------------------------------------------------------------------------
该类的 Service 主要是服务于 Developer. 全部的 Service 列表可以在 AWS 官网上看.

以下是我个人对这些服务的简短解读:

- AWS CodeCommit: 全托管的 Git 仓库, 类似于 GitHub, 不过功能没有那么全. 例如有 Pull Request 和 Code Review, 但是没有 issues. 对于企业内部合作我觉得足够了. 跟 GitHub 一样也有一套 API 可以对文件进行各种操作. 好处是你可以用 IAM Role 来访问 CodeCommit 而无需像 GitHub 一样管理你的 Personal Access Token.
- AWS CodeBuild: 全托管的 CI build runtime. 类似于 GitHub action 和 CircleCI. 它专注于运行程序进行 build. 它的配置文件也是 yaml, 和 GitHub CircleCI 类似. 没有 Jenkins 里的 Stage 功能. 但是 AWS 的另一个服务 CodePipeline 可以提供 Jenkins 里的 Stage 功能, 并且更强大.
- AWS CodePipeline: 全托管的 CI/CD orchestration. 类似于 Jenkins 里的 Stage 功能. 把一个个的 CodeCommit repo, CodeBuild project, CloudFormation, Lambda 等步骤 orchestrate 到一起.
- AWS CodeDeploy: 针对 AWS EC2, Lambda, ECS 的全托管 deployment. 自动化了 blue green deployment, rolling updates, canary deployment 部署流程.
- AWS Cloud9: 基于 EC2 的 IDE, 可以理解为在 EC2 上的 VS Code. 我个人非常喜欢, 用来实验一些东西非常好, 不会影响到我自己电脑的硬盘. 而且可以用 IAM Role 来访问 AWS 资源, 不需要管理 Access Key 和 Secret Key. 自带自动关机功能, 非常方便.
- AWS CloudShell: 基于 EC2 的 bash shell, 上面自带 1GB 的存储空间, 保存在 $HOME 下的文件不会丢. 而且可以用 IAM Role 来访问 AWS 资源, 不需要管理 Access Key 和 Secret Key. 非常方便.
- AWS CodeStart: 一个全托管的开发项目环境管理工具. 说白了就是一个面板, 把上面的 CodeCommit / CodeBuild / CodePipeline / Cloud9 / CloudShell 放在一起按照项目, 团队, 人员管理起来. 初创公司可以用用.

下面是从 AWS 官方复制过来的 Service 列表 (as of 2023-03-14):

- Amazon CodeCatalyst (Preview): Unified software development service for faster development and delivery on AWS
- Amazon CodeGuru: Find your most expensive lines of code
- Amazon Corretto: Production-ready distribution of OpenJDK
- AWS Cloud Control API: Manage cloud infrastructure with unified APIs
- AWS Cloud Development Kit (CDK): Model cloud infrastructure using code
- AWS Cloud9: Write, run, and debug code on a cloud IDE
- AWS CloudShell: Browser-based shell environment
- AWS CodeArtifact: Secure, scalable, and cost-effective artifact management for software development
- AWS CodeBuild: Build and test code
- AWS CodeCommit: Store code in private Git repositories
- AWS CodeDeploy: Automate code deployments
- AWS CodePipeline: Release software using continuous delivery
- AWS CodeStar: Develop and deploy AWS applications
- AWS Command Line Interface: Unified tool to manage AWS services
- AWS Device Farm: Test Android, iOS, and web apps on real devices in the AWS cloud
- AWS Fault Injection Simulator: Fully managed fault injection service
- AWS Tools and SDKs: Tools and SDKs for AWS
- AWS X-Ray: Analyze and debug your applications


Table of Content
------------------------------------------------------------------------------
.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
