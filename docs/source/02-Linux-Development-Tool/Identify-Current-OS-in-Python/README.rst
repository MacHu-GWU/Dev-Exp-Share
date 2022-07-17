.. _detect-current-os-in-python:

Identify Current OS In Python
==============================================================================
Keywords: Python, Detect / Identify, Linux Release Version, OS, Operation System

自动化运维的时候经常有需要 检测 当前 运行的 操作系统 的需求, 然后执行不同的命令来做某一件事. 例如安装依赖的时候 Redhat 是 yum, Ubuntu 则是 apt 等等.

下面这个 Python 脚本就是一个例子:

.. literalinclude:: ./example.py
   :language: python

Ref:

- 我正在运行的 Linux 是什么版本?: https://linux.cn/article-9760-1.html
- 查看 Linux 发行版名称和版本号的 8 种方法: https://linux.cn/article-9586-1.html
- os-release 中文手册: http://www.jinbuguo.com/systemd/os-release.html
