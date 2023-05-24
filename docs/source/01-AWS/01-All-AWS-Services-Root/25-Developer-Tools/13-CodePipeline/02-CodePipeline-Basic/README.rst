CodePipeline Basic
==============================================================================


What is CodePipeline
------------------------------------------------------------------------------
市场上 CI/CD 的产品太多了 J刚开始接触 CodePipeline 的时候, 一个很常见的问题就是

- https://circleci.com/docs/jobs-steps/
- https://docs.github.com/en/actions/using-workflows/about-workflows


Start a CodePipeline
------------------------------------------------------------------------------
首先我们要理解 CodePipeline 的运行是如何被触发的. 通常有两种方式:

1. 特定的事件发生时, 通常是 Git Source 发生变更时, 自动运行 CodePipeline.
2. 人工通过 API 运行 CodePipeline.

这里我们重点介绍第一种:

CodePipeline 中的 CodeCommit Action (Source Type) 只能用 RepoName + BranchName 的方式指定 Source. Cloudwatch 会监控这一事件, 如果发现 Branch 上发生了变更, 就会触发 CodePipeline.

那如果我注册了两个 CodeCommit Action, 一个监控 main branch, 一个监控 dev branch 会发生什么呢? 这会导致这两个 branch 中的任何一个发生变更, 就会运行 CodePipeline. 而由于你定义了两个 CodeCommit, 那么就会自动同时从两个 branch 拉取代码. 这样虽然是可以运行的, 但是逻辑上是不成立的. 你应该为两个 Branch 分别创建 CodePipeline. 哪个发生了变更就运行哪个.

要注意运行 CodePipeline 是没有参数的, 它就会按照定义的 Source 是哪个 branch, 就从哪里拉取代码. 之所以设计成运行 Pipeline 没有参数是因为它本质上不是 StepFunction 那种计算编排工具. 就像 GitHub Action workflow, 也没有包含运行 Workflow 的动态参数.


Working with CodePipeline Variables
------------------------------------------------------------------------------
**CodePipeline Variables 是什么? 有什么用?**

CodePipeline 的编排的最小单位是 Action, 这些 Action 之间是可以通过 Variables 进行传递数据的. 有部分 Action 在运行结束后会生成一些 Variable. 举例来说 CodeCommit Action (Source Type) 是用来从 CodeCommit checkout 源码的, 这个动作会生成一个叫 ``CommitId`` 的 Variable. 你需要给他一个 NameSpace, 例如就叫 ``SourceVariables`` 好了. 然后你可以在下一个的 CodeBuild Action 中加入一个 Key 为 ``SOURCE_VARIABLES_COMMIT_ID``, Value 为 ``#{SourceVariables.CommitId}`` (这里的 #{...} 和前面的 NameSpace 以及 Variable 的名字要匹配, 而 ``SOURCE_VARIABLES_COMMIT_ID`` 则是你自己随便取). 然后你就可以在 CodeBuild 中看到这个环境变量了.

根据我的经验, 有下面几点需要注意:

- 只有 AWS 支持的这些 Action 会有 built in Variables. 而且可用的 Variables 列表是固定的. 可以在 `Variables available for pipeline actions <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html#reference-variables-list>`_ 文档中查到. 有一些特殊的 Action 例如 CloudFormation, CodeBuild 和 Lambda 是允许你自定义 Variables 的, 不受限于这个列表.
- ``#{codepipeline.PipelineExecutionId}`` 是一个全局可用的 Variable, 用来表示当前的 Pipeline 的 Execution ID. 这就意味着你完全可以在任何具有运算功能的地方, 例如 CodeBuild, Lambda 利用这个 ID 在 S3 生成一个 Object, 然后把当前 Action 中的任何数据保存在 S3 上, 然后再在之后的运算单元根据 Execution ID 从 S3 中读这个数据. 这意味着你可以脱离 Variables 的限制在任何运算单元之间传递数据.
- 前面生成的 Variables 可以在之后的任意一个 Action 中引用, 无需是下一个 Action.
- 不要用 CodeCommit CommitMessage, 由于 CodePipeline 的原因, 直接将它放到 Environment Variable 中会导致出错, 因为 Commit Message 是有多行的, 而且里面的字符可能不符合 EnvVar 的要求. 建议你用 CodePipeline 的 list pipeline executions 的 API 或是用 CodeCommit 的 get commit 的 API 来获取 CommitMessage.

Reference:

- `Working with variables <https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-variables.html>`_
- `Variables available for pipeline actions <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html#reference-variables-list>`_
- `Environment variables in build environments <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html>`_

