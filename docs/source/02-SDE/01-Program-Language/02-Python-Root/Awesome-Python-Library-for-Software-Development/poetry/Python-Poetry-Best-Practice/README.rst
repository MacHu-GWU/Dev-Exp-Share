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


Poetry CLI Command Overview
------------------------------------------------------------------------------
这一节我们快速的过一遍所有的顶级命令, 了解它们各自的功能.

项目初始化相关:

- new: 创建一个新文件夹作为你的项目目录, 并且初始化所需要的文件.
- init: 通过问你一些问题来帮你初始化 ``pyproject.toml`` 文件.

**安装依赖相关**:

- lock: 对 ``pyproject.toml`` 中的信息进行分析, 解析出一个依赖列表.
- install: 读取 ``pyproject.toml`` 中的信息, 安装项目依赖. 如果 ``poetry.lock`` 文件不存在 (你从来没有解析过依赖), 那么就进行安装并生成 ``poetry.lock`` 文件. 反之则基于 ``poetry.lock`` 中的结果安装依赖.
- update: 读取 ``pyproject.toml`` 中的信息, 更新依赖的版本并安装, 并更新 ``poetry.lock`` 文件. 这个常见于你前一次 install 或是 lock 的时候软件版本是 A, 几天后它更新了, 而你的定义是用的形如 ``^x.y.z`` 或是 ``*`` 的格式, 那么它就会自动更新.
- add: 将依赖添加到 ``pyproject.toml`` 中 (会修改它) 并安装, 并更新 ``poetry-lock``.
- remove: 将依赖从 ``pyproject.toml`` 中移除 (会修改它) 并安装, 并更新 ``poetry-lock``.
- search: 对 PyPi (或私有的) repository 进行搜索.

跟 ``pyproject.toml`` 的编写相关:

- show: 显示你的依赖信息.
- check: 用来检查 ``pyproject.toml`` 的格式和错误.
- version: 用来修改 ``pyproject.toml`` 中的 version. 比如 major, minor, patch +1.

构建和发布到 repository 相关:

- build: 构建你的 zip, wheel 包.
- publish: 将你的包发布到 PyPI.
- source: 用来管理额外的第三方 repository.

虚拟环境相关:

- env: 跟虚拟环境的创建与管理相关的命令.
- run: 使用虚拟环境运行某个命令.
- shell: 仅需虚拟环境的 shell, 和 ``source .venv/bin/activate`` 不同, 这是一个 subshell, 也就是说 env var 会从主 shell 继承而来, 但是在 subshell 中的修改不会影响主 shell.

跟 poetry 自己相关:

- config: 对 poetry CLI 本身进行配置.
- cache: 对 poetry 缓存进行管理.
- about: 打印 poetry 自己的信息.
- help: 显示帮助菜单.
- list: 显示所有可用的命令.
- self: 管理跟 poetry 自己的安装相关的事情, 例如管理插件等.

Reference:

- `poetry Commands <https://python-poetry.org/docs/cli/>`_


Dependency Specification
------------------------------------------------------------------------------
这一节我们来学习一下定义依赖版本区间相关的语法.

其中核心的几种语法分别是:

- 以 ``^`` 开头的, 主要针对版本的上限, 要求更新时的新版本不得超过定义中最左边的非零数字.
- 以 ``~`` 开头的, 主要针对版本的下限, 要求更新时的新版本至少是某个版本.
- 包含 ``*`` 的通配符语法, 针对于各种最新版本.
- 包含 ``>=<`` 不等式的语法, 针对于显式定义版本区间.
- 用逗号分隔, 将以上的几种语法用逻辑 AND 组合起来的定义.

Reference:

- `Dependency Specification <https://python-poetry.org/docs/dependency-specification/>`_


The ``pyproject.toml`` File
------------------------------------------------------------------------------
这一节主要介绍 ``pyproject.toml`` 中跟 ``poetry`` 相关的语法.

Reference:

- `The pyproject.toml File <https://python-poetry.org/docs/pyproject/>`_
