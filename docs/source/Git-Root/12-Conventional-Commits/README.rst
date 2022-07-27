.. _conventional-commits:

Conventional Commits
==============================================================================
Keywords: Conventional, Commit, Commits

Conventional Commits 是一种 Git Commit Message 的一种约定.

- ``fix``: 类型 为 fix 的提交表示在代码库中修复了一个 bug (这和语义化版本中的 ``PATCH`` 相对应).
- ``feat``: 类型 为 feat 的提交表示在代码库中新增了一个功能 (这和语义化版本中的 ``MINOR`` 相对应).
- ``BREAKING CHANGE``: 在脚注中包含 BREAKING CHANGE: 或 <类型>(范围) 后面有一个 ! 的提交, 表示引入了破坏性 API 变更 (这和语义化版本中的 MAJOR 相对应) .  破坏性变更可以是任意 类型 提交的一部分.
- 除 ``fix:`` 和 ``feat:`` 之外, 也可以使用其它提交 类型 , 例如 ``@commitlint/config-conventional`` (基于 Angular 约定) 中推荐的 ``build:``, ``chore:``, ``ci:``, ``docs:``, ``style:``, ``refactor:``, ``perf:``, ``test:`` 等等.
- 脚注中除了 BREAKING CHANGE: <description> , 其它条目应该采用类似 git trailer format 这样的惯例. 


Parse Conventional Commits
------------------------------------------------------------------------------
这里我写了一个基于 Python 3.7+ 的脚本, 可以用于解析 conventional commits.

.. literalinclude:: ./conventional_commits_parser.py
   :language: python

这是测试用例:

.. literalinclude:: ./conventional_commits_parser.py
   :language: python

社区还有其他的包实现了更强的功能:

- https://github.com/multimac/conventional
- https://github.com/commitizen-tools/commitizen


Reference
------------------------------------------------------------------------------
- https://www.conventionalcommits.org/en/v1.0.0/
