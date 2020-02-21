.. _git-workflow-tutorial:

Git Workflow Tutorial (Git 工作流)
==============================================================================

Git Workflow是一个特指, 是一个具体的工作流的名字, 而不是泛指所有的 Workflow.

.. note::

    Git Workflow 源自于 Linux 项目本身. 业界经验证明, 该工作流只适合 复杂度高, 发布周期长在 3 - 6 个月, 开发者平均素质高的开源项目. 各个大工作例如 Google, Facebook, Amazon 主要用 Trunk Base Workflow. **但是学习 Git Workflow 非常有意义, 能够了解到一个软件开发到发布的过程中的痛点**

    Git Workflow 的流行主要因为在 Google 搜索引擎中, 一篇 Comparing Workflows 的博文非常 流行, 所以知名度较高.

.. contents:: Table of Content
    :depth: 1
    :local:


集中式工作流
------------------------------------------------------------------------------

- 所有人都在Master分支上工作.
- 适合只有一个开发者的项目.


功能分支工作流
------------------------------------------------------------------------------

- 每个人在不同的分支上为不同的功能特性工作.
- 使用Pull Request进行Code Review和讨论.
- 功能开发完成通过后Merge到Master分支.
- 非常灵活, 适合中小型团队.


Gitflow 工作流
------------------------------------------------------------------------------

- Gitflow工作流 = Master + Hotfix + Release + Develop + 功能分支工作流.
- 所有的功能分支都是从Develop分支上分出去的.
- 更加严谨, 适合大型项目, 比如Python项目本身.


Forking 工作流
------------------------------------------------------------------------------

- 只有代码维护者能够Push到正式仓库.
- 代码贡献者只能Fork一个镜像, 在贡献者自己的镜像上开发后, 提交给代码维护者要求Merge到正式仓库.
- 常用于开源项目, 能接受不信任贡献者的提交.


Reference
------------------------------------------------------------------------------

- Git Workflow Tutorial 中文: https://github.com/xirong/my-git/blob/master/git-workflow-tutorial.md
- Comparing Workflows: https://www.atlassian.com/git/tutorials/comparing-workflows
- Comparing Workflows 翻译: https://github.com/oldratlee/translations/blob/master/git-workflows-and-tutorials/README.md
