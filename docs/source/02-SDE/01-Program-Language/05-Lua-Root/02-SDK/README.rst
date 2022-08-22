.. _lua-sdk:

Lua SDK
==============================================================================


简介
------------------------------------------------------------------------------
Lua 的源码是 C 写的. Lua 解释器 (可执行文件) 在不同的平台 (操作系统, 嵌入式) 需要编译后才能使用. 当然官方已经有不同的平台下的预编译版本了. 在 http://luabinaries.sourceforge.net/download.html 这里可以找到 Window 和 Linux 平台下的下载. 当然在 Linux 下你可以直接用 ``yum / apt / ... install lua`` 来进行安装. 而在 MacOS 下你可以用 Homebrew 上的 formula https://formulae.brew.sh/formula/lua, 用 ``brew install lua`` 命令进行安装.

下面我们以 MacOS 为主来介绍如何准备 Lua 的开发环境.


在 MacOS 上配置 Lua 的开发环境
------------------------------------------------------------------------------
1. 安装 Homebrew: https://brew.sh/
2. 用 Homebrew 安装 Lua: ``brew install lua``
3. 用 ``which lua`` 找到 lua 的解释器的位置, 然后试一试 ``lua -v`` 命令看看是否安装成功了
4. 创建一个 ``test.lua`` 纯文本文件, 然后复制粘贴以下脚本, 然后用 ``lua test.lua`` 命令试试运行

.. code-block:: lua

    #!/usr/bin/env lua

    print("Hello World!")


**Lua 的 IDE**

我个人不是 Lua 专家, 目前我是用 JetBrain 家的 IDEA + EmmyLua 插件 (https://plugins.jetbrains.com/plugin/9768-emmylua) 来开发. 运行文件使用 Terminal.

**Lua 的包管理**

Lua 也是有包的概念

- https://luarocks.org/