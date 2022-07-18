Poetry
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Poetry
------------------------------------------------------------------------------
官网上的一句话很好的说明了 Poetry 的独特之处: "Poetry comes with all the tools you might need to manage your projects in a deterministic way."

**确定性依赖**

Poetry 致力于让你的环境依赖具有确定性. 也就是说无论在什么机器上, 我们的依赖环境都是严格一致的. 下面我用几个例子来说明一下 我们平时用 ``requirements.txt`` 管理项目的时候, 里面定义的通常是我们需要的什么包, 有一个大致的版本依赖. 而运行 ``pip install -r requirements.txt`` 之后, 这些包的以及它们依赖的包, 以及它们依赖的包的依赖的包也会被安装. 而这些底层的依赖的版本是不断更新的, 很可能你今天 build 的依赖是 1.0, 明天就成了 2.0 了, 这对于要求稳定的生产环境是不可接受的.

业界的做法是, 当所有程序跑通之后, 我们通常会用 ``pip freeze > requirements-freeze.txt`` 命令将所有包的确定版本输出到 ``requirements-freeze.txt 文件中``. 以后在部署的时候就根据里面的固定版本 build 和 deploy. 简而言之就是 ``requirements.txt`` 的用户是人类, 专注于项目需要的核心依赖. ``requirements-freeze.txt`` 的用户是机器, 详细的列出了所有依赖.

对于这点 Poetry 使用了 `pyproject.toml PEP-518 <https://peps.python.org/pep-0518/>`_ 来替代 requirements.txt 文件. 而在每次运行了 ``poetry install`` 命令后, 会根据成功安装的包生成一个 ``poetry.lock`` 文件, 记录了所有被安装的包的具体版本, 以及一些其他信息. 本质上就是 ``requirements-freeze.txt`` 文件的替代. 这两个文件都是要被 check in 到 Git 中的. ``pyproject.toml`` 明显要比 ``requirements.txt`` 更强大, 可维护性更好.

以上做法还是存在一个问题, 你用 pip install requirements.txt 时如果出现了包 A, B 都依赖 C, 而依赖的 C 的版本互相之间没有交集, 这时就会出现冲突. 而 pip 只会尝试安装 A, 然后在安装 B 的时候报错. 然后留下一个只安装了部分依赖的烂摊子. 逻辑上正确的做法显然是在安装前就把这些依赖都进行对比计算, 如果出现冲突就报错, 压根不安装任何东西.

对于这点 Poetry 会先分析你的需求, 把依赖解析清楚, 如果有冲突则报错, 没冲突才会安装.

**安全问题**

PyPi 曾经出现过多次有人恶意上传带有恶意代码的包, 你一 import 就中招了. 有时候一个优秀的项目被 hack 了, 黑客发布了带有恶意代码的新版本. 而你的依赖里指定的是包的一个范围, 比如大于等于 1.0. 这样就有可能安装到带有恶意的代码. 而 Poetry 会在 lock 文件中维护你曾经成功的包的版本以及 check sum. 以后在别的机器上 build 的时候, 如果下载下来的包 check  sum 不对是不会安装的, 这样就避免了安全问题.

Ref:

- https://python-poetry.org/


Python 依赖管理软件比较
------------------------------------------------------------------------------

- PDM https://dev.to/frostming/a-review-pipenv-vs-poetry-vs-pdm-39b4#:~:text=Pipenv%20uses%20a%20very%20different,with%20the%20lock%20file%20existing.


Poetry
------------------------------------------------------------------------------



Poetry Command - Manage Environment
------------------------------------------------------------------------------
本节介绍与虚拟环境相关的 poetry 命令

**Create Virtualenv**:

.. code-block:: bash

    poetry env use /full/path/to/python
    poetry env use python3.7
    poetry env use 3.7
    poetry env use system

Display Venv Info:

.. code-block:: bash

    # 列出当前环境的详细信息, 如果你是用 virtualenv 手动创建的环境, poetry 依然能找到
    poetry env info

    # 只列出当前环境的路径
    poetry env info --path

    # 可以利用上一个命令自动找到对应的路径, 然后 source 进入虚拟环境
    source "$(poetry env info --path)/bin/activate"

    # 列出由 poetry 管理着的的环境列表
    poetry env list

Delete Venv:

.. code-block:: bash

    poetry env remove /full/path/to/python
    poetry env remove python3.7
    poetry env remove 3.7
    poetry env remove test-O3eWbxRl-py3.7

Add and Install