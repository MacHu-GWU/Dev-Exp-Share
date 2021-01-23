Code Commit
==============================================================================

什么是 Code Commit? Code Commit 其实就是 Git 服务器的实现, Code Commit Console 相当于一个用户界面远没有 GitHub 友好的 GitHub. 允许用户在 Console 里查看文件, 发起 Pull Request, 进行 Code Review.


在 Mac 电脑上像平常使用 GitHub Desktop 一样使用 Code Commiit
------------------------------------------------------------------------------


Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Code Commit 的验证是跟 IAM User 绑定的, 也就是通过 Credential 可以查到是哪个 IAM User 实施了 Pull, Push 等操作.

你需要到 IAM User 下找到 ``HTTPS Git credentials for AWS CodeCommit`` 一项, 并生成账号密码. 以下说到 "账号密码", 都指的是 Code Commit Git Credential.


MacOS 上的大坑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
为什么要强调 Mac 电脑. 因为 Mac 电脑使用 Keychain Access 来管理你在命令行输入的账号密码. 如果为一个 AWS Account 上的 Code Commit Repo 设置过账号密码, 那么 Keychain Access 则会自动缓存该 Credential. 而你在换到别的 AWS Account 中的 Code Commit 的时候, 你的 Teminal 还会使用之前的 Credential, 因为 Code Commmit 的服务器地址是一样的, 都是 https://git-codecommit.us-east-1.amazonaws.com. 而由于你换了 AWS Account, Code Commit Credential 肯定也不一样了, 所以会导致失败. 此时你需要手动删除 Keychain 上的缓存即可.

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
