Code Commit
==============================================================================

什么是 Code Commit? Code Commit 其实就是 Git 服务器的实现, Code Commit Repository 相当于一个用户界面远没有 GitHub 友好的 GitHub.


在 Mac 电脑上像平常使用 GitHub Desktop 一样使用 Code Commiit
------------------------------------------------------------------------------


Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Code Commit 的验证是跟 IAM User 绑定的, 也就是通过 Credential 可以查到是哪个 IAM User 实施了 Pull, Push 等操作.

你需要到 IAM User 下找到 ``HTTPS Git credentials for AWS CodeCommit`` 一项, 并生成账号密码. 以下说到账号密码, 都指的是 Code Commit Git Credential.



MacOS 上的大坑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
为什么要强调 Mac 电脑. 因为 Mac 电脑使用 Keychain Access 来管理你在命令行输入的账号密码. 如果为一个 AWS Account 上的 Code Commit Repo 设置过账号密码, 那么 Keychain Access 则会自动缓存该 Credential. 而你在换到别的 AWS Account 中的 Code Commit 的时候, 你的 Teminal 还会使用之前的 Credential, 因为 Code Commmit 的服务器地址是一样的, 都是 https://git-codecommit.us-east-1.amazonaws.com. 而由于你换了 AWS Account, Code Commit Credential 肯定也不一样了, 所以会导致失败. 此时你需要手动删除 Keychain 上的缓存即可.

此段参考资料: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html


使用 Code Commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当你创建新的 Repo 时, 你要在 Code Commit 中创建. 然后使用 ``git clone https://git-codecommit...`` 命令拉取 repo. 此时 Terminal 会提示输入账号密码. 输入后 ``~/.gitconfig`` 文件和 MacOS Keychain Access 会被更新.

然后你可以使用 GitHub Desktop 选择 Add Local Repository, 然后输入账号密码即可.


把已经存在的 Git Repo 导入到 Code Commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

例如你想把 GitHub 上的 Git 仓库导入到 Code Commit. 注意你可不能说创建一个新的 Code Commit Repo, 然后直接把代码 Copy and Paste 过去, 这样会丢失你全部的 Commit 记录.

此段参考资料: https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-connect.html

核心的两条命令是 ``git remote add origin https://git-codecommit.us-east-1.amazonaws.com/v1/repos/${repo_name}``, ``git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/${repo_name}``