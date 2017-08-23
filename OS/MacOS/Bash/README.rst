Bash
==============================================================================
Bash文件就是MacOS下的等价于Linux的Shell Script和Windows下的Batch File。

学习资料:

- `Shell编程30分钟入门 <https://github.com/qinjx/30min_guides/blob/master/shell.md>`_
- `Advance Bash-Scripting Guide <http://tldp.org/LDP/abs/html/>`_
- `Unix Shell Programming <http://www.tutorialspoint.com/unix/unix-shell.htm>`_
- `Linux Shell Scripting Tutorial - A Beginner's handbook <https://bash.cyberciti.biz/guide/Main_Page>`_


命令检索的顺序
------------------------------------------------------------------------------
MacOS下也有跟Windows中的Environment Variable类似的环境变量$PATH, 可以在命令行中输入 ``$PATH`` 查看。可以参考 `Understand Path <https://github.com/pyenv/pyenv#understanding-path>`_。


Default Path Order::

    /usr/local/bin
    /usr/bin
    /bin


Special Character in Bash
------------------------------------------------------------------------------
- ``@``: 取消回显。也就是说如果直接用 ``echo Hello``，控制台除了显示 ``Hello`` 之外，还会显示 ``echo Hello``。而 ``@echo Hello`` 则只显示 ``Hello``
