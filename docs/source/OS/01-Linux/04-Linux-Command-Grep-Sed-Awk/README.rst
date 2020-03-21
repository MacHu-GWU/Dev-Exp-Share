Linux Command Grep Sed Awk
==============================================================================

如何在命令行中实现字符串处理 (String Manipulation) 呢?

Linux 内置命令中有字符串处理 ``grep``, ``sed``, ``awk`` 三剑客. 当然还有万能黑科技 Python.

参考资料:

- Linux grep 命令: https://www.runoob.com/linux/linux-comm-grep.html
- Linux sed 命令: https://www.runoob.com/linux/linux-comm-sed.html
- Linux awk 命令: https://www.runoob.com/linux/linux-comm-awk.html


.. contents::
    :local:


``grep``
------------------------------------------------------------------------------


``sed``
------------------------------------------------------------------------------


``awk``
------------------------------------------------------------------------------

AWK 是将文本以行的方式遍历, 然后默认以空格为分隔符进行分割. 然后用 awk 的模式语言来对文本进行过滤, 处理的工具.

举例1, content of ``log.txt``::

    2 this is a test
    3 Do you like awk
    This's a test
    10 There are apple, banana, cherry

命令的输入输出为 (注意, 模式语言必须使用 单引号)::

    $ awk '{print $1,$4}' log.txt
    2 a
    3 like
    This's
    10 apple,

分析: print 是打印函数, $1, $4 定义了你所选择的元素. 每一行以空格为分隔符分割, 例如第一行中 ``2`` 是第一个元素, ``a`` 是第四个元素.


举例2, 还是 ``log.txt``, 这次的输入输出是::

    $  awk '{printf "%-8s %-10s\n",$1,$4}' log.txt
    2        a
    3        like
    This's
    10       apple,

分析: printf 是格式化打印函数, "%-8s %-10s\n" 定义了打印格式,


``python``
------------------------------------------------------------------------------

Python 作为通用编程语言, 在功能上比上面三个肯定是强大多了. 但是由于通用, 命令的效率, 优雅程度差远了. 但是好处是你可以自行实现任何功能, 而且免除了精通以上三个命令的学习投资.

首先我们要知道如何将字符串变量在 Python 和 Shell 命令之间传递. 方法有两种.

1. 使用 ${} injection::

    #!/bin/bash
    # content of example.sh

    NOW="2017-01-03 08:30:00"
    NOW_DATE=$(python -c "print('${NOW}'[:10])") # 由于我们需要使用 ${} 将变量值传递给 Python, 所以我们需要使用双引号 " 作为最外层的标记.
    echo $NOW_DATE

这里我们将 shell script 中的字符串 inject 到 python 字符串中. 而 ``python -c`` 命令可以将代码作为字符串执行. **可是你得注意了, 将字符串作为代码执行, 变量如果被黑客修改, 黑客可以利用这一点执行任何代码. 当然这里我们将 ${NOW} 放在了字符串中, 所以还是安全的**. 但此方法只适用于简单字符串, 如果字符串里面包含很多特殊符号的时候, 可能就不太好用了.

2. 使用文件作为缓冲, 以及使用 standard input (stdin).

然后, 还是那个 ``log.txt`` 文件, 我们希望输出包含有 apple 的所有行, 相当于 ``$ cat log.txt | grep apple``::

    2 this is a test
    3 Do you like awk
    This's a test
    10 There are apple, banana, cherry

这是我们的 Python 脚本::

    # -*- coding: utf-8 -*-
    # content of example.py

    import sys

    if __name__ == "__main__":
        lines = list()
        # 从 sys.stdin 中读取数据. 他是一个 file like object
        for line in sys.stdin.read().split("\n"):
            if "apple" in line:
                lines.append(line)
        print("\n".join(lines))

最终的命令是这样的::

    $ cat log.txt | python example.py

或者直接从变量::

    $ echo $BIG_TEXT | python example.py
