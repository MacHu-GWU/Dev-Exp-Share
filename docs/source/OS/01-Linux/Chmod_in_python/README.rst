Chmod in Python
==============================================================================
Keywords: Change Mode, Chmod, Permissions, Python, os.

当我们需要将一个文件设置为可执行时, 在命令行界面我们一般要用 ``chmod +x filename`` 来设置.
其中 chmod 是 Linux 系统命令 change mode 的简写, 而 +x 表示可执行 (executable).
那么如何用 Python 将这一命令自动化呢?

Python 中的 os 模块是一个与操作系统交互的接口, 它提供了许多与操作系统相关的函数, 其中就包括
chmod. 而 stat 模块则提供了对文件状态的接口, 例如包括了对用户权限码的枚举.

在下面的例子中我们有一个 CLI 程序需要变为可执行的.

.. literalinclude:: ./cli
   :language: python
   :linenos:

下面这个 Python 自动化脚本可以实现这一点.

.. literalinclude:: ./change_mode.py
   :language: python
   :linenos:


Reference:

- https://docs.python.org/3/library/os.html#os.chmod