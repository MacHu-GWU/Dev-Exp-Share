.. _python-standard-lib-subprocess:

Python Standard Library - ``subprocess``
==============================================================================
Keywords: Python Standard Library subprocess, Shell Command, DevOps, Automation


Summary
------------------------------------------------------------------------------
作为 DevOps Engineer, 写 Shell Script 可以说是家常便饭. 但是 Shell Script 并不是一个易于学习, 易于维护的语言. 很多 FAANG 之类大厂的 Senior DevOps Engineer 都经常在 shell script 中犯错. Python 作为一个通用脚本语言, Shell Script 能做到的事情 Python 肯定都能做到, 而 Python 还能做很多 Shell Script 做不到的事情. 特别是对于文件系统的操作, 数字和字符串的处理, Python 有着不是一点点的先天优势. 虽然很多 Unix 自动化工具都是以命令行的形式使用的, 可 Python 可以无缝调用各种 CLI 命令以及对 输入输出, 返回码, 错误 更好的处理.

作为 DevOps 工程师写自动化脚本, 用 Python 全面替代 Shell Script 是一条光明之路. 无需精通超级复杂的 Shell Script 技巧, 但仍然能写出 Shell Script 大牛才能实现的自动化脚本. 从投入和产出的角度来说, 用 Python 代替 Shell Script 也是明智之举.

Python 标准库中的 `subprocess <https://docs.python.org/3/library/subprocess.html>`_ 是 Python 调用 CLI 命令的核心. 也是学习用 Python 写自动化脚本的重点.

Examples:

.. toctree::
   :maxdepth: 2

   examples.ipynb