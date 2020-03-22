Shell Script - Redirection
==============================================================================


``>`` and ``>>``
------------------------------------------------------------------------------

``>`` 尖括号在 Bash Script 中表示重定向.

例如::

    # 将 alice 内容写入 log.txt 如果已经存在, 则会覆盖之
    echo "alice" > log.txt

    # 将 bob 内容写入 log.txt 尾部, 如果不存在, 则跟 > 效果一样, 如果已经存在, 则写入尾部
    echo "bob" >> log.txt

参考资料:

- https://www.tldp.org/LDP/abs/html/special-chars.html, 搜索 ``>>``
- https://www.tldp.org/LDP/abs/html/io-redirection.html#IOREDIRREF


``/dev/null`` and ``/dev/zero``
------------------------------------------------------------------------------

参考资料:

- Linux 下的两个特殊的文件 /dev/null 和 /dev/zero 简介及对比: https://blog.csdn.net/longerzone/article/details/12948925