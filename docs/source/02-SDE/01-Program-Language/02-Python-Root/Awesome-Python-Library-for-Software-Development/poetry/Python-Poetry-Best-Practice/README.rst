Python Poetry Best Practice
==============================================================================
本文是我自己在使用 poetry 的过程中总结的最佳实践.


Install Poetry
------------------------------------------------------------------------------
我们在开发 Python 项目的时候, 通常会涉及这么几个 Python 环境:

- System Python, 也就是的操作系统自带的 Python. 通常在这里 ``/usr/bin/python3``. 我们不会往这里安装任何东西. 所以之后的讨论我们就当这个不存在.
- Pyenv Python, 也就是你用 `pyenv <https://github.com/pyenv/pyenv>`_ 安装的 Python. 通常在这里 ``~/.pyenv/shims/python``.
- Virtualenv Python, 也就是你开发项目的时候创建的虚拟环境, 可以在任何地方.

Poetry 本身是一个 CLI 工具, 它可以被安装到 pyenv Python 或是 Virtualenv Python 中. 当你敲 ``poetry`` 命令的时候, 有这么两种情况:

- 你在 virtualenv 里, 如果你的 virtualenv 里装了 poetry, 那么就会用 ``/path-to-venv/bin/poetry``. 如果没装, 那么就会用 pyenv Python 中的 poetry.
- 而如果你不在 virtualenv 里, 那么则是安装 pyenv 的 global 配置按照顺序一个一个检索.

这个行为无论是你直接在命令行中敲命令还是通过 Python 脚本中的 ``subprocess.run(["poetry", "..."])``, 逻辑都是一样的.

.. important::

    由以上的讨论我们可以得知, 作为一个命令行工具, 就像 Virtualenv 类似, **你只要在 pyenv 的某一个 Python 版本中安装了 poetry 就可以了** (记得安装后打 ``pyenv rehash``). **你没有必要再在 Virtualenv 中安装 poetry** (poetry 本身需要的依赖也不少呢), **也没有必要再在其它版本中安装了** (例如你用 python3.8 安装了, 就没有必要再给 python3.9, 3.10, ... 安装).
