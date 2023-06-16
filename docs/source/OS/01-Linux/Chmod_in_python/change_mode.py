# -*- coding: utf-8 -*-

"""
当我们需要将一个文件设置为可执行时, 在命令行界面我们一般要用 ``chmod +x filename`` 来设置.
其中 chmod 是 Linux 系统命令 change mode 的简写, 而 +x 表示可执行 (executable).
那么如何用 Python 将这一命令自动化呢?

Python 中的 os 模块是一个与操作系统交互的接口, 它提供了许多与操作系统相关的函数, 其中就包括
chmod. 而 stat 模块则提供了对文件状态的接口, 例如包括了对用户权限码的枚举. 请看下面示例代码.

Reference:

- https://docs.python.org/3/library/os.html#os.chmod
"""

import os
import stat
from pathlib import Path


def make_it_executable(p):
    """
    该函数可以将任意 Path 路径对象所指向的文件设置为可执行. 其原理是先用 os.stat 获得
    当前的文件模式码, 然后再用 | (相当于集合运算中的添加) 运算法添加上 stat.S_IEXEC, 即
    chmod +x 的权限 (这里的 + 就是添加的意思, 和 | 等效. x 则是 executable, 和 stat.S_IEXEC
    等效).
    """
    p = Path(p)
    if p.is_file() is False:
        raise TypeError(f"{p} is not a file!")
    st = os.stat(p)  # get current stat of the file
    os.chmod(p, st.st_mode | stat.S_IEXEC)  # add 'executable' bit (| is bitwise OR)


p_cli = Path(__file__).absolute().parent.joinpath("cli")
make_it_executable(p_cli)
