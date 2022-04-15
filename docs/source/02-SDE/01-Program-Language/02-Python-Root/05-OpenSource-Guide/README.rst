.. _python-open-source-project-guide:

如何在 GitHub 上开发并维护一个 Python 开源项目?
==============================================================================
Keywords: Open Source, OpenSource, 开源, 开源项目, Python, GitHub

Open Source 项目并不简简单的是写一些 Code 并发布到 GitHub 上. 让我们 **把视角切换到 开源项目 用户的角度, 看一看他们到底是怎么想的**

**用户的想法**

1. 我有一个问题, 我希望找到一个开源项目能解决我的问题.
2. 这个开源项目是否有文档, 能够教会我如何使用这个项目解决我的问题?
    - 我希望用 10 分钟大致了解怎么用
    - 针对不同的问题, 这个项目提供了什么解决方案
    - 针对具体的 API, 我希望看看 Input / Output 的接口, 以及它的具体实现
3. 我是否能信任这个项目, 并在我的生产环境中使用?
    - 核心功能是否能正常工作? 核心功能被充分测试过了么? 特殊情况考虑到了吗?
    - 非核心功能是否能正常工作? 会不会由于各种奇怪的问题导致我的程序出错? 有 代码覆盖测试 把非核心功能的代码也测过了吗?
    - 这个项目支持 我的 OS 操作系统以及 Python 的版本吗?
4. 我如何安装这个软件?
5. 我是否能信任这个项目的开发者?
    - 他们是否有 CI (持续集成) 来保证代码质量和测试覆盖?
    - 他们的 Code Style 好不好? 这反映了开发者的水平和素质.
6. 如果我遇到了问题, 我能否快速的找到帮助?
7. 我有特殊的需求, 我有具体方案能添加这个功能满足我的需求, 我如何能够给这个项目贡献代码? 下一个版本我就可以用上这些功能了.

**基于用户的想法, 一个开源项目要做这些工作. 每少一项工作, 用户使用你的开源项目的信心就会少一点**.

1. 你的代码需要能解决问题, 达到了你的目标.
2. 要有文档, 教会用户如何使用你的开源项目.
    - basic: README files
    - advance: delegated doc website, tutorial, by example, by API
3. 要有单元测试, 保证你的代码功能上没有问题.
4. 要有覆盖测试, 给用户信心使用你的开源项目. 保证你的测试覆盖率达到了 90%+.
5. 要有矩阵测试, 覆盖 Windows / Mac / Linux 以及 Python3.6, 3.7, 3.8, +. 因为 Python 的用户可能使用任意平台.
6. 要有代码风格标准化, 自动化格式代码风格, 确保无论谁提交的代码, 最后代码风格都是一样的.
7. 要有 CI/CD, 每当代码 push 到仓库, 就要进行一些测试, build 文档 等工作, 提高自动化程度.
8. 要有 Publish, 你的开源项目要 Publish 到 PyPI 上供人方便的安装.
9. 要有开源社区沟通工具. 允许用户提交 Bug, Feature Request, Ask for Help.
    - basic: GitHub issue
    - advance: public slack / gitter channel, stackoverflow tag
10. 要有 Badge, 把以上的这些组件例如测试状态, 文档状态, 版本信息以 Badge 的形式方便地展示给用户.
11. 要有 Contribution Guide, 让用户能方便的参与到贡献代码中来. 通常是通过 GitHub Folk Workflow 来进行.
12. 要有 Release History, 标注每个版本的改动.
    - basic: one readme file
    - advanced: use ``.. versionadded::``, ``.. deprecated:: verion`` in your doc string


Coverage Test (覆盖测试)
------------------------------------------------------------------------------
在 Python 中的覆盖测试行业标准是 `coverage.py <https://coverage.readthedocs.io/en/latest/>`_ 这个库. 它提供了配置文件供你定义其行为; 命令行工具以执行测试, 以及展示报告; 与主流测试框架如 ``pytest, unittest, nosetest`` 的集成插件. 简单来说他的原理就是在运行测试的时候, 监视每一行代码是否被调用过. 运行完测试后就会把收集到的数据保存为一个叫 ``.coverage`` 的 Sqlite 文件. 这个文件人类不可读, 但是可以用 ``coverage report`` 等命令行工具读取并以人类友好的方式显示. 目前对于人类最友好的方式是以 HTML 显示, 最终会在项目目录下生成一个叫 ``htmlcov`` 的目录, 里面自带 ``.gitignore`` 文件以防止你不小心 ``git commit`` 到 git repo 中. 由于 ``pytest`` 是 Python 中单元测试的事实标准, ``pytest-cov`` 则是 ``pytest + coverage.py`` 的集成插件.

这里有一个脚本能用 pytest 运行测试, 并生成本地 html 报告:

.. literalinclude:: ./bin/06-run-coverage-test.sh
   :language: bash

还有一些题外话. https://www.codecov.io/, https://coveralls.io/ 都是比较流行的覆盖测试的 CI 平台. 可以和 coverage.py 深度集成, 每次 CI 测试完之后自动将报告发送给这些 CI 平台, 并生成人类友好的界面供检查. 还能生成 badge 以供你随时监视.

Ref:

- Coverage 文档官网: https://coverage.readthedocs.io/en/latest/