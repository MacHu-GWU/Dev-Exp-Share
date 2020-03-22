Command Line (CLI) and Shell Script
==============================================================================


命令检索的顺序
------------------------------------------------------------------------------
MacOS下也有跟Windows中的Environment Variable类似的环境变量$PATH, 可以在命令行中输入 ``$PATH`` 查看。可以参考 `Understand Path <https://github.com/pyenv/pyenv#understanding-path>`_.


Default Path Order::

    /usr/local/bin
    /usr/bin
    /bin


Special Character in Bash
------------------------------------------------------------------------------
- ``@``: 取消回显。也就是说如果直接用 ``echo Hello``，控制台除了显示 ``Hello`` 之外，还会显示 ``echo Hello``。而 ``@echo Hello`` 则只显示 ``Hello``

