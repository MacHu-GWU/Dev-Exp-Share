.. _aws-codecommit-authentication:

AWS CodeCommit Authentication
==============================================================================
Keywords: AWS CodeCommit, Git Remote Commit, GRC, Authentication, Access

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

.. sectnum::


Summary
------------------------------------------------------------------------------
There are three major methods you can securely connect to CodeCommit repo:

1. HTTPS with username / password: 传统的用户密码方式, 这个密码是在 Iam User 下的 Security Credential 菜单中的 HTTPS Git credentials for AWS CodeCommit
 一栏里创建的.
2. SSH: 自己生成 SSH Key Pair, 然后把公钥上传到 Iam User 下的 Security Credential 菜单中的 SSH keys for AWS CodeCommit 一栏.
3. Git Remote Commit (GRC) with IAM Role: 是一个 AWS 维护的命令行工具, 也是一个 git 插件, 实现了基于 IAM 的权限管理.

最推荐的是 #3, #1 和 #2 适合已经对 GitHub GitLab 这些很熟悉, 但对 AWS 不熟悉的人快速上手使用. 长期来看需要维护的东西太多, 也不适合给 EC2, Lambda, CodeBuild 等运行环境授权, 因为你需要手动上传 username password, 或是 SSH key.


GRC 方法
------------------------------------------------------------------------------
GRC 方法的本质是用你本机的 AWS CLI credential, 临时生成一个 token, 然后自动生成 git 相应的命令.

``git-remote-commit`` 是一个 Python 命令行工具, 你需要用 ``pip install git-remote-commit`` 安装, 并使得这个命令在当前 shell 环境下生效. 例如你用 ``pyenv`` 管理你的 Python, 你用特定的 Python 版本例如 python3.8 安装了 grc, 那么你要记得 ``pyenv rehash`` 使得这个命令生效. 不然 ``git clone ...`` 就无法自动感知到 ``git-remote-commit`` 的存在.

使用 GRC 的 Git Clone 命令有多种方式:

.. code-block:: bash

    # use default aws cli profile
    git clone codecommit::{region}://{repo_name}

    # use specific aws cli profile
    # ``.git/config`` 文件会记录你的 profile name, 如果你修改了 profile name, 记得来这里改
    git clone codecommit::{region}://{aws_cli_profile}@{repo_name}

    # clone specific branch
    git clone codecommit::{region}://{repo_name} --branch {branch_name}

    # clone specific commit
    git clone codecommit::{region}://{repo_name} --branch {branch_name} # you have to know the branch
    git checkout 1a2b3c4d # then check out specific commit

- git-remote-commit Release Announcement: https://aws.amazon.com/about-aws/whats-new/2020/03/aws-codecommit-introduces-open-source-remote-helper/
- Basic Git: https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-basic-git.html
- For HTTPS connections with git-remote-codecommit: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html


Https with Username and Password
------------------------------------------------------------------------------
- https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html


SSH
------------------------------------------------------------------------------
- Without AWS CLI: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-without-cli.html
- Setup SSH on Unix: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html
