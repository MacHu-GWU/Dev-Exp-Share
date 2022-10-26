Shell Scripting (Script) in Bash Docs
==============================================================================

Shell, Terminal, Bash 这些词语经常被同时使用且混用. 但是通常我们值得是 在命令行 界面 通过敲命令 与系统交互. 而把一系列命令组合起来, 使用 变量, 循环 等方式将复杂的逻辑复合在一起, 这就是 shell scripting.

这里我们需要区分并搞清楚 Shell, Terminal, Bash 之间的关系.

- Terminal (终端): 是一个用于接收用户输入, 返回输出的工具. CMD, ITerm, Terminal 都是终端.
- Shell (壳): 是将操作系统内核进行封装抽象, 使得用户可以通过在 Shell 中打命令操作系统内核. bash, sh 都是 Shell.

bash 和 sh 都是 Unix 系统上兼容性较好的终端. 其中 bash 功能比较强大, 兼容性较好. 但是要注意的是 bash 也有一些不兼容的语法, 请尽量避免使用这些. **以后我们说 Shell Scripting 或是 Bash Scripting, 主要指的是 Bash Scripting**.

值得一提的是 Windows 下的 batch file, power shell 是 Windows 专属的.

学习资料:

- `Shell编程30分钟入门 <https://github.com/qinjx/30min_guides/blob/master/shell.md>`_
- `Advance Bash-Scripting Guide <http://tldp.org/LDP/abs/html/>`_
- `Unix Shell Programming <http://www.tutorialspoint.com/unix/unix-shell.htm>`_
- `Linux Shell Scripting Tutorial - A Beginner's handbook <https://bash.cyberciti.biz/guide/Main_Page>`_

.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
