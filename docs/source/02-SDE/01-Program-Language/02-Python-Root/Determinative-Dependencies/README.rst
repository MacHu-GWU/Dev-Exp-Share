Determinative Dependencies
==============================================================================
Keywords: Python, Pip, Requirements, Determinative Dependencies, Poetry

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


什么是 Determinative Dependencies
------------------------------------------------------------------------------
传统的 Python ``requirements.txt`` 文件有个问题就是里面的依赖可能会互相冲突, 特别是依赖的依赖之间互相冲突. 这会导致在不同的机器上不同的时间安装依赖会导致不同的结果. Python 社区有个项目 `poetry <https://python-poetry.org/>`_ 实现了determinative dependency management, 是的你在不同的机器, 不同时间, 安装的环境永远是一摸一样的.

但是很多项目没有那么 fancy, 可能还是主要使用 pip 来做依赖管理. 这里我们用一些比较笨但是有效的方法实现了类似的功能, 所以有必要做出一些说明.


如何用 pip 实现 Determinative Dependencies
------------------------------------------------------------------------------
``requirements-main.txt`` 这个文件里记录了我们的代码中凡是真正需要 import 的包. 当然这些包会依赖其他包. 每次我们重新创建一个 venv 环境, 然后安装这些包, 然后将所有依赖的固定版本用 ``pip freeze`` 命令导出, 最后运行单元测试测试一下, 如果通过说明这个依赖是可以用的. 但这样做有个问题, 如果你的 ``requirements-main.txt`` 里的包之间就是有冲突的, 那么你得自己去把有冲突的包的版本提高和降低, 手动解决冲突. 如果只用 pip, 这是没有办法的事情. 这也是 ``poetry`` 这一类的项目存在的意义.

完整的流程看起来是这样:

1. 创建虚拟环境
2. 安装 ``requirements-main.txt`` 中的依赖
3. 将安装好的依赖的确定版本导出到 ``requirements.txt``
4. 安装你的项目的 python 包本身, 以及测试用的依赖
5. 运行单元测试, 确保这些依赖没问题


自动化脚本
------------------------------------------------------------------------------
我们有一个自动化脚本自动化了以上的全过程, 在 ``./bin/resolve_requirements.py`` 这个地方. 这个脚本本身只需要 Python3.6+ 标准库, 无需任何依赖 (当然你要提前装好 pygitrepo).

.. literalinclude:: ./resolve_requirements.py
   :language: python

可以看到 ``requirements-main.txt`` 里面只有一个 ``requests``. 具体版本不明.

.. literalinclude:: ./requirements-main.txt

我们安装了里面的包之后, 跑了一下测试发现没问题, 于是就将安装好的依赖导出了. 导出后会发现增加了几个其他的依赖.

.. literalinclude:: ./requirements.txt

而后续的测试部分我们就不管了, 请自行完成.
