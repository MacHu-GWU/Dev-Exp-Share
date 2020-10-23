Linux Daemon
==============================================================================

Daemon 也叫 守护进程, 是 Linux 中一种特殊的进程, 不会被普通的 signal 给 terminate 掉, 只能被 Kill. 常用于运行后台服务. 但 守护进程 不是 后台服务, 后台服务 会包含多个 守护进程.


前台运行 和 后台运行 (Daemon) 的区别
------------------------------------------------------------------------------

**从终端的角度看的区别**:

我们以 MongoDB 的 mongod (https://docs.mongodb.com/manual/reference/program/mongod/#bin.mongod) 为例.

``mongod`` 是一个 bin tool, 可以在本地运行 MongoDB. 但是如果你在终端中输入该命令, 一旦运行, 该终端窗口就无法再做其他事情了.

而如果你在终端里用 ``brew services start mongodb-community@4.4`` (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) 命令运行, 他会在后台启动一个服务. 而你可以在该终端里继续做其他事情.

所以从终端的角度看, 前台运行就是 **会占用终端**, 后台运行就是 **不会占用终端**.


如何用 Python 运行守护进程
------------------------------------------------------------------------------

Python 社区最好的 daemon 包应该是 python-daemon, 作者得到了社区的认可, 并有计划将其加入到标准库.

- https://pypi.org/project/python-daemon
- https://www.python.org/dev/peps/pep-3143