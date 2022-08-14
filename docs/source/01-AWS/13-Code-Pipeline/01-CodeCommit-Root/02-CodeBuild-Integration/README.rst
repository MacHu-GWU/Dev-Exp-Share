.. _aws-codecommit-codebuild-CICD-example:

AWS CodeCommit and CodeBuild CI/CD Example
==============================================================================
Keywords: AWS CodeCommit, Code Commit, CodeBuild, Code Build, CI, CD, CICD

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Summary
------------------------------------------------------------------------------
一套 CI/CD Pipeline 主要包含两个部分, 一个 Git 代码仓库, 一个 CI Job Run 环境.

- Git Repo:
    - 目的: 开发者在上面进行开发, 保存代码的历史记录. 所有对 Git 的操作, 包括 commit, branch, PR, comment, approve, merge 都会触发 Git Event, 根据这些 event 来决定是否, 如何进行后续的 CI Job Run.
    - 可选的产品: 市场上的 Git 托管产品很多, GitHub, GitLab, BitBucket, AWS CodeCommit 等, AWS CodeCommit 的好处是会将详细的 Git Event 给用户, 让用户自己决定如何对这些 event 做出响应.
- CI Job Run:
    - 目的: 提供一个轻量的代码运行环境, 能运行自动化脚本, 构建代码, 测试代码, 部署 APP. 这里有基于虚拟机 VM 的, 也有基于容器 Container 的.
    - 可选的产品: 有 GitHub action, CircleCI, AWS CodeBuild 等. AWS CodeBuild 的好处是跟 AWS 结合的比较紧密, 省去了配置跟 AWS 相关的权限的麻烦.

总结下来就是 AWS 的这两个服务的特点是自定义程度极高, 虽然配置起来稍微复杂了点, 但是你有最高的自由度.

本文主要介绍如何用 AWS CodeCommit 和 AWS CodeBuild 这两个产品搭建一个 CI/CD Pipeline.


Architecture
------------------------------------------------------------------------------
首先我们来看一下架构.

.. raw:: html
    :file: aws-codecommit-and-codebuild-cicd.drawio.html

1. **Trigger Build Job**: 目前 Git Event 和 Build Job 之间并没有打通. 在 GitHub 上这是通过服务器上的 Web `hook <https://git-scm.com/book/zh/v2/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-Git-%E9%92%A9%E5%AD%90>`_ 实现的. 原理上就是通过 GitHub 服务器上的 hook 自动化脚本, 将 git event 转化成用户友好的 JSON, 然后选择发送到其他外部系统上, 从而实现自动化. 而 AWS CodeCommit 的内置了 Notification Rule 功能, 能将 Git Event 发送到 SNS Topic, 然后 SNS Topic 触发 AWS Lambda, 由于 Lambda 可以是任何语言任何代码, 基本上能做到任何事情, 这就实现了 AWS CodeCommit 和任何外部系统的打通. 当然本文主要说的是与 CodeBuild 之间的打通.
2. **Post Build Job Automation**: CodeBuild Job 本身也有 Notification Rule 功能, 能将例如 Start, Failed, Success 以及每个 Phase 的开始结束的这些 event 发送到 SNS. 和之前一样, 我们可以用 AWS Lambda 对其进行处理, 从而实现自动通知, 报警等功能.
3. **Artifacts**: Build Job Run 的输出有 test report 结果. 这些结果可以被发送到办公聊天软件中自动通报. 并且 build 的成功失败消息也能被发送到聊天软件中. 另外 Build Job Run 的输出还包括 Artifacts, 以供后续的部署. 而这些 Artifacts 则可以保存到 S3 中.


当代码 Push 到 CodeCommit 时, 如何自动触发 CodeBuild?
------------------------------------------------------------------------------
AWS CodeBuild 是 AWS 提供的 CI 持续集成服务, 能从 Git 服务器上拉取代码执行自动构建 / 测试 / 部署. 你可能已经使用过 GitHub 以及各种免费的 CI 系统例如 travis ci, circle ci, github action. 这些 CI 和 GitHub 的集成原理是 Webhook, 也就是每次 GitHub 收到 Push, Merge, Commit, Create Branch, Create Pull Request 之后, 后台都会生成一个 Event, 然后通过 webhook 发送给这些 CI 系统的服务器. 这些 CI 系统把常用的这些 event 集成好了, 只需要用图形界面点几下就可以在 Push 代码后自动 Build 了.

AWS CodeCommit 也有 event, 你在 Console -> CodeCommit -> Repositories -> Notify -> Create Notification Rule 下面可以看到所支持的 Event 的列表.

- Comments
    - On commits
    - On pull requests Approvals
- Status changed
    - Rule override
    - Pull request
- Source updated
    - Created
    - Status changed
    - Merged
- Branches and tags
    - Created
    - Deleted
    - Updated

你可以将这些 Event 发送到 SNS topic, 然后用 SNS topic trigger AWS Lambda, 对这些 event 进行分析过滤, 看到符合条件的 event 就用它来 trigger 一个 AWS CodeBuild 即可. 这里要注意的是, 你的 SNS topic 的 access policy 里 Policy 需要是 ``"Service": "codestar-notifications.amazonaws.com"``, 还有因为 SNS 自动创建的 Access Policy 会根据你创建 Topic 的时候用的 IAM User/Role 自动给予你自己权限, 所以会有一段 ``"Condition": ...`` 的定义, 这将阻止 codestar-notification 调用 ``SNS:Publish`` API, 所以一定要去掉. 下面有一个例子:

.. literalinclude:: ./sns-topic-access-policy.json
   :language: javascript

本质上来说这个 Trigger 的规则是由 AWS 用户自己实现的, 而不是像 circle ci 等一样由 ci 平台托管的. 虽然带来了额外工作, 但是给予了用户最大的权限和开放度能自定义想要的 CI 流程. 可以适应任何复杂的企业级项目管理流程.

这里列出了常见的 Event 所对应的 SNS Notification Message (不是 Lambda event, 只是 notification 的 string message 被 json 解析后的形式)

``approval-message.json``:

.. literalinclude:: ./notification-event/approval-message.json
    :language: javascript

``comment-to-pull-request-message.json``:

.. literalinclude:: ./notification-event/comment-to-pull-request-message.json
    :language: javascript

``commit-to-branch-message.json``:

.. literalinclude:: ./notification-event/commit-to-branch-message.json
    :language: javascript

``commit-to-master-message.json``:

.. literalinclude:: ./notification-event/commit-to-master-message.json
    :language: javascript

``commit-to-pull-request-branch-message.json``:

.. literalinclude:: ./notification-event/commit-to-pull-request-branch-message.json
    :language: javascript

``create-branch-message.json``:

.. literalinclude:: ./notification-event/create-branch-message.json
    :language: javascript

``create-pull-request-message.json``:

.. literalinclude:: ./notification-event/create-pull-request-message.json
    :language: javascript

``merge-to-master-message.json``:

.. literalinclude:: ./notification-event/merge-to-master-message.json
    :language: javascript

``reply-to-comment-message.json``:

.. literalinclude:: ./notification-event/reply-to-comment-message.json
    :language: javascript

``rule-override-message.json``:

.. literalinclude:: ./notification-event/rule-override-message.json
    :language: javascript


AWS CodeCommit Lambda Trigger
------------------------------------------------------------------------------
熟悉 Lambda Trigger 的开发者可能会发现 AWS Lambda 的 Trigger 里有 CodeCommit 的选项. 里面只支持三种 event:

- Create branch or tag
- Push to existing branch
- Delete branch or tag

这可以理解为一个简化版的 event trigger. 只有在代码实实在在发生改变, 产生了新的 commit 或是 tag 的时候才会触发. 而像是工作流: create Pull Request 则是不会触发 build 的. 这适合个人开发者单独维护一个代码库的情况.

不同的 event 以及对应的 json 的参考:

``commit-to-branch.json``:

.. literalinclude:: ./lambda-trigger/commit-to-branch.json
    :language: javascript

``commit-to-master.json``:

.. literalinclude:: ./lambda-trigger/commit-to-master.json
    :language: javascript

``create-branch.json``:

.. literalinclude:: ./lambda-trigger/create-branch.json
    :language: javascript

``merge-to-master.json``:

.. literalinclude:: ./lambda-trigger/merge-to-master.json
    :language: javascript


Use boto3 to start CodeBuild Job
------------------------------------------------------------------------------
示例代码请参考 :ref:`aws-codebuild-trigger-build-job-with-boto3`

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build

