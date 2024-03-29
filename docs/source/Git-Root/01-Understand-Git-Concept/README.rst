.. _understand-git-concept:

Understand Git Concept (理解 Git 的 概念)
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


什么是 版本控制系统
------------------------------------------------------------------------------
Git 是一种 Source Code Version Control System (VCS 版本控制系统). 版本控制系统的核心功能是:

1. 能够将代码库回滚到任意一个之前的状态.
2. 允许多人合作, 在同一个代码库上工作, 并轻松的合并大家的工作. 特别是多个人对同一个文件的修改.

Git 不仅仅可以用来做代码版本控制, 还可以用来作任何系统的版本控制. 因为代码大多数是纯文本文件, 是一行一行的. 体积小, 可以用增量来表示修改. 而对于图片, Word, Excel 这一类的文件, 为了保存修改, 需要保存每一个版本的备份, 会导致文件体积很容易变得很大. Git 只是比较适合用于代码版本控制. 用来写书, 写博客, 管理新闻媒体稿件都很合适.


什么是 Git
------------------------------------------------------------------------------
Git 是一个 VCS, 也是目前最流行的 VCS. Git 本身包含两个组件:

1. 安装在本地机器上的 git 和 git 命令行工具. 用户可以选择性的安装 GUI 图形界面攻击. 我们用它来 添加, 修改, 删除 我们的代码文件.
2. 安装在远程服务器上的 git server. 用于永久保存在云端并有多个备份, 为多位开发者提高代码的下载和提交服务.


什么是 Repo (代码库)
------------------------------------------------------------------------------
版本控制的对象叫做 Repository. 由许多文件和文件夹组成.


Git 是怎么实现 版本控制 的? (commit 又名 提交)
------------------------------------------------------------------------------
对 ``repo`` 的修改操作有 ``add`` 增加, ``update`` 修改, ``delete`` 删除 三种. 其他的例如 重命名, 移动都是以上三种操作的排列组合. 这三种 最小操作 叫做 原子操作.

每一次对 repo 的修改都是一系列的三种原子操作的集合. 将这些原子操作打包成为一次 提交, 又名 ``commit``. 每次 ``commit`` 都会改变 ``repo`` 的版本. 也就是说, ``repo`` 的改变的最小单位是 是 ``commit``.

每一个 ``commit`` 有一个 sha1 hash, 是全世界唯一的, 简称 ``hash``. git 可以用 ``hash`` 来精准定位到某一个具体的版本.

之后我们说 "某一个 ``commit``" 同时也指的是 "该次 ``commit`` 所做的所有更改".


Git 是怎么实现多人合作的? (branch 又名 分支)
------------------------------------------------------------------------------
你可以基于任何具体的版本创建一个 ``branch``, 然后你新的 ``commit`` 就会在这个 ``branch`` 上进行. 每一个 ``branch`` 有一个名字. 通常一个代码库的第一个, 也是默认的 ``branch`` 名字叫 ``master``. 每一个 ``branch`` 都有一个 base branch, 通常开发中我们会从 ``master`` 进行 ``branching``. 当然我们也可以以其他的 ``branch`` 作为 base 进行 ``branching``.

``branch`` 是名词, 指一个具体的分支. 而 ``branching`` 是动词, 指从某个 ``commit`` 进行分支的动作.

多个开发者可以各自创建自己的 ``branch``, 分别负责不同的修改, 然后将这些修改合并到 ``master`` 上. 如果两个人对同一个文件的一段代码进行了修改, 那么就会产生 ``conflict``, 此时就要 人工 resolve conflict 才能合并. 这个合并的操作叫做 ``merge``.

在 ``merge`` 之前, 通常要由 ``branch`` 的作者之外的人进行审核. 这个审核的过程叫做 ``code review``.


Git 服务器的作用是什么
------------------------------------------------------------------------------
服务器是代码库的事实标准. 由于有多人参与了开发, 所以我们需要一个公认的事实标准.

Git 允许你将所有代码下载到本地, 这个操作叫 ``clone`` 或 ``pull`` (两者有不同). 然后你可以在断网的情况下进行开发. 等有网的时候再将修改推送到服务器, 这个操作叫 ``push``.

通常你需要将 Git 服务器部署到一台或多台虚拟机上 (多台是用来做冗余备份的), 然后你的个人电脑要能联网到服务器才能使用 Git. 而 GitHub 就是世界上最大的 Git 服务器托管服务提供商, 无需设置服务器就可以使用 Git.


总结
------------------------------------------------------------------------------
以上就是 Git 的核心概念.
