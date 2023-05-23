Multi Environment Multi AWS Account Lambda App CI/CD
==============================================================================


What is the problem?
------------------------------------------------------------------------------
根据我在企业中的经验, 很多企业都是用多个 AWS Accounts (Workload oriented organizational unit), 例如 devops, sandbox, test, staging, prod 来部署 App 的. 每个 App 都需要按顺序一步步的部署到下一个 Account 上, 然后最后部署到 prod.

而我经常发现很多企业项目的 Data 项目中的 Git repo 里面有很多很多的 Lambda, Glue 等资源, 而他们都是通过一个 CloudFormation 命令来部署的. 仅仅修改了一行代码, 结果就部署了一堆东西, 完全没有机制进行隔离.

我自己是有一套框架能实现 multi environment 的部署以及 CI/CD 的. 但是这个框架是基于一个 deployment unit 就是一个 repo 的假设. 为了一个 repo 就要配套的配置一个 CodeBuild Project 以及一个 CodePipeline. 但是实际开发过程中很多时候都是一个 repo 里面有很多个本应属于不同的 deployment units 的 Lambda. 所以引发了我的思考, 有没有一种方法能尽量减少前期工作, 又能在一个 Git repo 中同时管理多个 deployment units, 即可分开部署, 也可以同时部署的架构呢?

这就是我想要解决的问题.

总结下来, 我想要设计的架构应该能解决以下问题:

- 一个 repo 中可以同时拥有多个 deployment units, 它们要能分开部署也能单独部署
OrganizationAccountAccessRole

https://signin.aws.amazon.com/switchrole?roleName=OrganizationAccountAccessRole&account=bmt-app-dev

::

/projects
/projects/project1/...
/projects/project2/...
/projects/project3/...
/README.rst

    /projects/
    /projects/project1/...
    /projects/project2/...
    /projects/project3/...
    /bin/
    /bin/automation/...


    # Layer artifacts
    s3://bucket/projects/${project_name}/lambda/layer/000001/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000001/requirements.zip

    s3://bucket/projects/${project_name}/lambda/layer/000002/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000002/requirements.zip

    s3://bucket/projects/${project_name}/lambda/layer/000003/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000003/requirements.zip

    # Source artifacts
    s3://bucket/projects/${project_name}/lambda/source/0.1.1/${project_name}-0.1.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.1.1/${project_name}-0.1.1.tar.gz

    s3://bucket/projects/${project_name}/lambda/source/0.2.1/${project_name}-0.2.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.2.1/${project_name}-0.2.1.tar.gz

    s3://bucket/projects/${project_name}/lambda/source/0.3.1/${project_name}-0.3.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.3.1/${project_name}-0.3.1.tar.gz

    /projects/project1/...
    /projects/project2/...
    /projects/project3/...
    /bin/
    /bin/automation/...

Reference:

- `AWS DevOps Blog - Multi-branch CodePipeline strategy with event-driven architecture <https://aws.amazon.com/blogs/devops/multi-branch-codepipeline-strategy-with-event-driven-architecture/>`_

我以前做过一个 CI/CD 的架构. 用 CodeStar Notification Event 来监控 Git 的操作, 然后将 Event 发给 SNS, 然后用 Lambda 来处理这些 Event, 然后来触发 CodeBuild Project. 这个架构的本质是让 Lambda 来承担分析 Event 并过滤的人物, 并用来 Invoke 后续的工作. 后来接触了 Event Bridge 之后发现这个过滤以及 Data Enrichment 的过程可以被 Event Bridge 来完成. 但是用来 Invoke 后续的工作的步骤还是要交给 Lambda 来做比较好, 因为我们可能需要一些 Customization. 所以这引发了我的思考.