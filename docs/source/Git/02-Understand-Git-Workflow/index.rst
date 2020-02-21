.. _understand-git-workflow:

Understand Git Workflow (理解 Git 工作流)
==============================================================================

.. contents:: Table of Content
    :depth: 1
    :local:


What is Workflow? (什么是工作流)
------------------------------------------------------------------------------

Workflow 是指在我们带着某种目的, (通常是增加功能, 优化性能, 修复 bug, 或是发布版本, 进行部署), 想要对代码库进行修改的一个标准化流程.

例如对于增加功能, 优化性能, 修复 bug, 的标准流程是:

1. 从 master 上 branch 一个分支, 叫做 feature-a (或是 improve-a, fix-a)
2. 在 feature-a 上进行修改, 测试通过后 commit
3. 从 feature-a 发起一个 pull request (pr), 进行 code review
4. code review 通过, 将 feature-a merge 到 master, 然后删除 feature-a.

例如对于发布代码的标准流程:

1. 从 master 上 branch 一个 release 分支, 叫做 release-1.
2. 在生产环境的镜像中进行测试.
3. 只修复 bug, 添加文档, 不对功能做任何变化.
4. 如果因故需要对 release-1 进行修改, 则按照 修复 bug 的工作流 从 master 上 branch 一个 fix-a 分支, 然后 修改, commit, code review, merge. 最后在 release-1 上进行 cherry pick.


How to learn Workflow by doing? (如何动手体验工作流)
------------------------------------------------------------------------------

对于Git新手, 在没有学会 Git 命令行的情况下, 想要最快上手, 并且完整体验工作流中碰到的各种情况, 建议在两台不同的计算机上同时安装图形界面 `Github Desktop <https://desktop.github.com/>`_, 用于模拟多人合作开发.

如果没有两台电脑, 则建议安装两个不同的图形界面软件: `Github Desktop <https://desktop.github.com/>`_ 和 `GitKraken <https://www.gitkraken.com/>`_, 用两个工作目录克隆同一个仓库进行试验。


The Branch Workflow (常用工作流之 Branch Workflow)
------------------------------------------------------------------------------

所有团队成员都在一个 repository 上工作, 使用 branch 的方式来完成 feature 的开发. 各个成员的权限各不相同, 有代码的owner, reviewer, developer, 等等.

每次开会决定各人的任务, 然后各人为自己的任务建立一个 branch, 然后开发完毕后各自提交pr, 等待 reviewer 审核通过或者修改后 merge 到 master branch。

通常用于一个成员互相都认识的团队为同一个项目工作的情况, 常用于公司环境中.

以上只是一个简化版本, 根据项目的性质和复杂度, 会有不同的 branch 策略.


The Fork Workflow (常用工作流之 Fork Workflow)
------------------------------------------------------------------------------

开源项目常常将代码库 host 在 GitHub 上, 当有公众开发者想贡献代码时, repo 的拥有者并不希望直接给其他人 写权限. 那其他开发者怎么贡献代码呢?

GitHub 有一个 ``fork`` 功能, 也就是相当于创建一个 由某个公众开发者所有, 和源 repo 一摸一样的镜像, 包含所有历史记录和 branch 的信息. 然后公众开发者只要在这个 ``fork`` 上创建一个新的开发 branch, 完成开发和测试后提交 pr 就好了.


Workflow Principle (工作流的内在原理)
------------------------------------------------------------------------------


原则1: 不要在master branch上进行开发
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

master 是生产环境的事实标准, 也是一个状态良好的代码库的 "备份". 换言之, 你自己的 branch 被搞得乱七八糟也没有关系, 打不了推翻从来, 只要有 master 在, 恢复的难度不大. 但是如果 master 被弄乱了, 恢复就不容易了. 即使 revert 到之前的 commit, 也会导致期间别人创建的 branch 都包含了你的 脏代码, 导致所有人都要跟着一起清理, 非常麻烦.


原则2：要尽量避免多个成员在各自的Pull Request中对同一个文件进行修改
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
简单来说就是, 多个成员各自的branch的工作文件要分离, 而不能有重叠.

在此原则下, 我们来看一个例子:

1. 1-1日, A 和 B 都克隆了整个仓库, 并且从 master 分支上分别 branch 了一个fa, fb分支.
2. 1-2日, A 完成了修改, 添加了文件 a.txt, 提交了一个 pr, 要求将fa分支merge到master, 并且当天就通过了.
3. 1-3日, B 完成了修改, 添加了文件 b.txt, 提交了一个 pr, 要求将fb分支merge到master, 此时 **由于fb分支和fa分支没有任何冲突**, pull request提交的实际上是branch与master之间的差异, 而这个fb的差异和fa的差异毫无冲突, 所以可以 **顺利Merge**。
4. 在A, B都完成了修改之后, A 的 master 缺少 b.txt 文件, B 的 master 缺少 a.txt 文件, 此时在 GitHub 客户端只要点一下 ``sync`` 按钮, 就会自动将远程服务器上的 Master 的改变 Merge 到本地, 也就是更新到最新状态。此时如果有新的开发任务, 只要从 **当前的master** 上再创建一个新的开发branch即可。

如果违反此原则, 会发生什么:

1. 1-1日, A和B都克隆了整个仓库, 此时项目中有一个文件 ``readme.txt``, 并且从master分支上分别branch了一个fa, fb分支.
2. 1-2日, A将 ``readme.txt`` 内容修改为 a, 并提交了一个 pr, 当天就 merge 了.
3. 1-3日, B将 ``readme.txt`` 内容修改为 b, 并提交了一个 pr, 此 pr 就会触发一个conflict, 必须将冲突解决之后才能成功 merge.
4. 如果两人要在此基础上进行新的开发, 同理只要 ``sync`` 远程仓库的改动, 就可以创建branch进行新的开发了.


Reference (参考资料)
------------------------------------------------------------------------------
- `起步 - 关于版本控制 <https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%85%B3%E4%BA%8E%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6>`_
