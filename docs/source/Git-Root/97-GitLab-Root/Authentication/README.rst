GitLab Authentication
==============================================================================
Keyword: Git, GitLab, Auth, Authentication, SSH, Personal Access Token.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


对于 Git 系统, Authentication 能做什么?
------------------------------------------------------------------------------
- 对于 public repository, 任何人都能 clone / pull, 但是只有 owner 和有权限的人才能 push.
- 对于 private repository, 只有有权限的人才能 clone / pull / push.


GitHub 和 GitLab 都提供了以下两种 Auth 方式:

- SSH
- Personal Access Token


SSH 方式原理
------------------------------------------------------------------------------
SSH 是利用了非对称 RSA 加密算法的一种通信协议. 通信双方都各自有一个 Private Key 和 Public Key. 自己的 Public Key 是可以给全世界任何人的, 有了这个 Public Key 就可以跟你通信. 简单来说你需要把你的 Public Key 上传到 GitLab, 然后每次你发起请求的时候 GitLab 就会生成一套 GitLab 拥有的 key, 然后自动把 GitLab 的 Public Key 给你, 从而你们就能安全的通信了.


Token 方式原理
------------------------------------------------------------------------------
Token 本质就是一个钥匙, 和密码类似. GitLab 会在服务器保存这个钥匙并每次在你发起请求时与之比对. 不同的是一个账户可以有很多 Token, 生命周期和权限各不相同, 并且账号主人可以随时禁用.


具体命令
------------------------------------------------------------------------------

- GitLab URL 构成: https://<my-user-id>:<my-pat>@gitlab.com/<my-account>/<my-project-name>

.. code-block:: bash

    # 拉取你在 GitLab 上的私有仓库
    GL_TOKEN="abcde-U-fgh1234abcdefg"
    GL_USER="MacHu-GWU"
    GL_REPO="gitlab-test"
    git clone "https://oauth2:${GL_TOKEN}@gitlab.com/${GL_USER}/${GL_REPO}.git"

    # 具体例子
    git clone https://oauth2:@gitlab.com/MacHu-GWU/gitlab-test.git
    git clone "https://oauth2:${GL_TOKEN}@gitlab.com/MacHu-GWU/gitlab-test.git"

.. code-block:: bash

    # 拉取企业云的 GitLab 上的私有仓库
    git clone ssh://git@mycompany.importantproject.com:5050/my_account_id/my_repo_name.git
