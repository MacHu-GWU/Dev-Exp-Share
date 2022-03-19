.. _aws-code-commit:

Code Commit
==============================================================================
Keywords: AWS Code Commit, CodeCommit, Git

什么是 Code Commit? Code Commit 其实就是 Git 服务器的实现, Code Commit Console 相当于一个用户界面远没有 GitHub 友好的 GitHub. 允许用户在 Console 里查看文件, 发起 Pull Request, 进行 Code Review.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


在 Mac 电脑上像平常使用 GitHub Desktop 一样使用 Code Commit
------------------------------------------------------------------------------


Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Code Commit 的验证是跟 IAM User 绑定的, 也就是通过 Credential 可以查到是哪个 IAM User 实施了 Pull, Push 等操作.

你需要到 IAM User 下找到 ``HTTPS Git credentials for AWS CodeCommit`` 一项, 并生成账号密码. 以下说到 ``账号密码``, 都指的是 ``Code Commit Git Credential``.


MacOS 上的大坑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
为什么要强调 Mac 电脑? 因为 Mac 电脑使用 Keychain Access 来管理你在命令行输入的账号密码. 如果为一个 AWS Account 上的 Code Commit Repo 设置过账号密码, 那么 Keychain Access 则会自动缓存该 Credential. 而你在换到别的 AWS Account 中的 Code Commit 的时候, 你的 Terminal 还会使用之前的 Credential, 因为 Code Commit 的服务器地址是一样的, 都是 https://git-codecommit.us-east-1.amazonaws.com. 而由于你换了 AWS Account, Code Commit Credential 肯定也不一样了, 所以会导致失败. 此时你需要手动删除 Keychain 上的缓存即可.

此段参考资料: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html


将 Code Commit Repo 拉取到本地
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当你创建新的 Repo 时, 你要在 Code Commit 中创建. 然后使用 ``git clone https://git-codecommit...`` 命令将 repo 拉取到本地. 此时 Terminal 会提示输入账号密码. 输入后 ``~/.gitconfig`` 文件和 MacOS Keychain Access 会被更新.


将 Code Commit Repo 的改动 Push 到服务器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
首先你可以用所有的 git 命令做这些工作.

其次对于熟悉 GitHub Desktop GUI 的用户同样可以继续使用之, 你只要用 GitHub Desktop 选择 Add Local Repository, 然后输入账号密码即可像使用 GitHub 上大的 Repo 一样.


把已经存在的 Git Repo 导入到 Code Commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
例如你想把 GitHub 上的 Git 仓库导入到 Code Commit. 注意你可不能说创建一个新的 Code Commit Repo, 然后直接把代码 Copy and Paste 过去, 这样会丢失你全部的 Commit 记录.

核心的两条命令是 ``git remote add origin https://git-codecommit.us-east-1.amazonaws.com/v1/repos/${repo_name}``, ``git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/${repo_name}``

此段参考资料: https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-connect.html


在 AWS EC2 或者其他 AWS 环境中拉取代码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 AWS 环境中虽然你完全可以使用上面介绍的账号密码的方式用原生 git 命令跟 code commit 通信. 但是 AWS 提供了用 IAM Role 的方式进行授权, 只需要添加 CodeCommit::Pull* IAM Policy 即可. 而免去了管理账号密码的麻烦. 但你需要安装 git-remote-codecommit 插件. 首先你要有系统级的 python 环境, 然后用 ``pip install git-remote-codecommit`` 安装. 需要注意大的是, 你不能用 https 的 uri, 而是要用 https GRC (git remote codecommit) 的 url 格式:

    git clone codecommit::${region_name}://${repo_name}

此段参考资料: https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-connect.html


在 Cloud 9 (Or EC2) + Jupyter Lab 上使用 Code Commit
------------------------------------------------------------------------------
大型企业管理 AWS Account 的方式和个人有很大不同, 通常使用企业内部的 Employee Account (email / password), 通过 Single Sign On 来管理 Sign In. 也就是说一般企业用户不会使用 IAM User 来 Sign In. 所以 Code Commit 中为 IAM User 配置 "HTTPS Git credentials for AWS CodeCommit" 账号密码的方法就不奏效了.

**首先你需要确保 Cloud 9 / EC2 以及 Jupyter Notebook 上的 IAM Role 有足够的 Code Commit 权限**. 所需要的 IAM Policy 是:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "codecommit:CreateApprovalRuleTemplate",
                    "codecommit:DeleteApprovalRuleTemplate",
                    "codecommit:GetApprovalRuleTemplate",
                    "codecommit:ListApprovalRuleTemplates",
                    "codecommit:ListRepositories",
                    "codecommit:ListRepositoriesForApprovalRuleTemplate",
                    "codecommit:UpdateApprovalRuleTemplateContent",
                    "codecommit:UpdateApprovalRuleTemplateDescription",
                    "codecommit:UpdateApprovalRuleTemplateName"
                ],
                "Resource": "*"
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": "codecommit:*",
                "Resource": "arn:aws:codecommit:${region}:${account_id}:${repo_name}"
            }
        ]
    }

Ref:

- Connect to an AWS CodeCommit repository: https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-connect.html


使用 Cloud 9
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 在 Cloud 9 IDE 里的 Terminal 里安装 ``git-remote-codecommit`` 插件. 然后用 ``pip install git-remote-codecommit``.
2. 使用如下命令 clone 你的 repo: ``git clone codecommit::${region_name}://${repo_name}``
3. 在 Cloud 9 IDE 里的 Git Integration 里找到你的 repo, 有任何更改之后 ``add change`` 以及 ``commit``, 然后右键点击 repo 点 push.


使用 Jupyter Lab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. 在 Jupyter Lab 中点击 Git 的图标点击 clone repo. 然后到 code commit console 里找到 clone repo 里 https 方式的 URL. 格式长这个样子 ``https://git-codecommit.${region}.amazonaws.com/v1/repos/${repo_name}``.
2. 有任何更改之后 ``add change`` 以及 ``commit``, 然后点击 push 即可.


跨 AWS Account Pull / Push 到 Code Commit
------------------------------------------------------------------------------
请参考这篇文档: https://docs.aws.amazon.com/codecommit/latest/userguide/cross-account.html

简单来说就是三步:

1. Actions for the Administrator in AccountA (repo 在这个 Acc 上). 在 AccA 上创建 IAM Policy / Role, 我们称之为 RoleA, 这 RoleA 是能读写 repo 的.
2. Actions for the Administrator in AccountB (user 在这个 Acc 上). 在 AccB 上创建 IAM Policy / Role, 我们称之为 RoleB. 我们的 IAM User 可以 assume RoleB, 而 RoleB 也要能 assume RoleA, RoleA 也要允许 RoleB assume 它自己.
3. Actions for the repository user in AccountB. 接下来就跟跨 AWS Account assume role 一样, 用户 B 先 login, assume RoleB, 然后 assume RoleA, 最后对 Git 进行操作.

注意, 你无法使用 Codebuild built-in integration 跨 Account Pull CodeCommit repo. 你只能手动在 buildspec file 里写 shell script 来 clone repo.


Code Commit Trigger AWS Lambda
------------------------------------------------------------------------------
很多流行的 Git 系统例如 GitHub, GitLab 都有 Webhook 的功能. 也就是通过监控 Git 的 event, 包括各种 pull, push, merge request 等, 然后把事件信息的 JSON 数据发送给 Webhook 连接的后台, 实现自动化运行一些后续功能. 而 AWS CodeCommit 则可以用这些 event 触发 AWS Lambda, 以实现几乎任何你想实现的功能. 例如一些著名的 CI/CD 的 SAAS 服务的本质就是用 webhook 监控时间, 从而触发 build / deploy. 而你完全可以用 Lambda 监控, 并触发 Code build 的 build 从而做到更神奇的事.

- https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-notify-lambda.html
- https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-notify-lambda-cc.html


Code Commit Approval Rule
------------------------------------------------------------------------------
Approval Rule 是一个简单的功能, 可以实现对于不同的 branch, 指定一些 IAM User / Role, 只有他们 Approve 了之后才能 Merge.

- https://docs.aws.amazon.com/codecommit/latest/userguide/approval-rule-templates.html


Code Commit Code Owner
------------------------------------------------------------------------------
在 GitHub 中有个功能叫做 Code Owner. 也就是说对于某个文件夹下的文件, 必须得到 Code Owner Approve Pull Request 之后才能够 Merge. 在 Code Commit 中是通过 IAM 管理权限的. 所以你可以通过 IAM Policy 管理: 谁, 可以对哪些文件, 做什么. 比 GitHub 的 CodeOwner 功能更强大, 但是设置起来更复杂.

- https://docs.aws.amazon.com/codecommit/latest/userguide/auth-and-access-control-permissions-reference.html#aa-files
