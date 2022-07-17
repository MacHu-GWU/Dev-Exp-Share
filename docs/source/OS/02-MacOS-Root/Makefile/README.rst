Makefile介绍和使用说明
==============================================================================

makefile是一个文件名就是 ``makefile`` 或 ``Makefile`` 的文件。原本用于解决Linux平台下C语言开发时的编译工程文件时，各个文件和项目之间的依赖问题。在开源社区，发现非常适合用于管理软件的Deployment, Distribution。简单来说，可以将一系列的Shell命令用类似于 ``函数`` (在Makefile中不叫函数，这里我们只是用于指代)的方式组织起来，一个函数包含多个命令，一个函数也可以包含另一个命令。通常第一个函数作为该Makefile的总函数。

请注意: **Makefile要求强制Tab, 而用Space代替会导致出错**。

下面我们看一个例子：

.. code-block:: makefiles

    # This is an example make file
    # content of ``makefile``

    .PHONY: all install clean

    all: install clean
        @echo "make all"

    install:
        @echo "make install"

    clean:
        @echo "make clean"

如果你CD到文件所在目录，输入 ``make``，make就会自动找到目录下的make文件，并执行主函数。你将会看到如下输出：

.. code-block:: **makefiles**

    make install
    make clean
    make all