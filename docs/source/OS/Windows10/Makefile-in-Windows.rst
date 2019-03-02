.. contents::

Makefile in Windows
==============================================================================
在MacOS和Linux下都自带make工具, 能够轻易的完成软件的编译, 部署, 发布等工作。

`MinGW <http://www.mingw.org/>`_ 是一个开源的Windows下的C编译器, 也自带make工具。为了能使得能在Windows下向MacOS和Linux一样地使用Make, 只需要如下几部:

1. 到 http://www.mingw.org/ 下载binary installer安装MinGW, 在安装器里装MinGW Base。
2. 将 ``C:\MinGW\bin`` 添加到系统环境变量。
3. 将 ``mingw32-make.exe`` 复制一份并改名为 ``make.exe``, 使得和MacOS及Linux一致。