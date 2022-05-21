.. _aws-codecommit-codebuild-integration:

CodeBuild Integration
==============================================================================
Keywords: AWS CodeCommit, Code Commit, CodeBuild, Code Build, Integration

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


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

.. literalinclude:: ./commit-to-branch.json
    :language: javascript

``commit-to-master.json``:

.. literalinclude:: ./commit-to-master.json
    :language: javascript

``create-branch.json``:

.. literalinclude:: ./create-branch.json
    :language: javascript

``merge-to-master.json``:

.. literalinclude:: ./merge-to-master.json
    :language: javascript
