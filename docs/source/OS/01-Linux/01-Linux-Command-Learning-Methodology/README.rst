Linux Command Learning Methodology
==============================================================================

Linux 有几百个内置命令, 常用的也有几十个. 要想熟练掌握所有命令的前提是你经常使用这些命令. 如果你不经常使用, 一段时间很快你就会忘掉. 如果你只是 Linux 命令的低频用户, 那么我建议你将你常用的命令用法, 例子, 写成文档, 并为这篇文档建立书签, 例如这是我自己的 :ref:`Linux Command Cheatsheet <linux-command-cheat-sheet>`.

在学习Linux命令时, 一定要记住一个最有用的命令: ``man`` (manual), 可以用于查看任何命令的文档.

- 作用: 查看 ``{command}`` 命令的手册, 语法, 选项信息.
- 语法: ``man {command}`` 命令

学习命令的流程应该是这样的:

1. 了解命令的主要功能, 以及在什么情况下使用它.
2. 命令一般都有选项, 参数, 了解几个最重要的即可.

例如 ``ls`` 列出文件列表命令:

- ``ls``
- ``ls -l``: list file info in long format.
- ``ls -lh``: in long and human readable format.

例如 ``du`` 查看磁盘用量:

- ``du`` (Disk Usage): 查看磁盘用量.
- ``du -sh``: 查看当前目录的磁盘用量.
