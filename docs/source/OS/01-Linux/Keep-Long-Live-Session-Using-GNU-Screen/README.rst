.. _keep-long-live-session-using-gnu-screen:

Keep-Long-Live-Session-Using-GNU-Screen
==============================================================================
Keywords: GNU, Screen, Terminal, Session, Long Live Living, Linux.


需要解决的问题
------------------------------------------------------------------------------
有时候我们远程 SSH 登录服务器以后要运行一个耗时很长, 甚至永久运行的脚本. 又或者有些 Session 做到一半你要离开 (甚至离开一天), 然后你希望回来以后能恢复这个 Session. 但你一旦关闭了 Terminal, 或是连接超时, 这个负责运行脚本的 Session 也会被杀死. 当然 Linux 服务就是为了永久运行的后台服务所设计的, 但是这需要你的程序符合一些标准. 这意味着你需要做很多额外工作, 并且不是每个脚本都符合这些标准的. 所以我们需要一个能长期运行任意脚本, 并且保持 Session 的解决方案. 这个解决方案就是 GNU Screen.

在了解了需求之后, 我们来简单分析一下难点. 每次我们用 Terminal 登录远程服务器的时候, 就会创建一个 Terminal Session. 这个 Session 可以超时, 断开等. 如果你关闭了 Terminal, 那么这个 Terminal 下的所有 Session 也会被断开. 而我们的本地机器别说 Terminal 了, 很可能因为任何问题而关机, 可不像服务器能长期运行. 所以我们需要的其实是一个将 Session 的状态维持在服务器上的一个工具. 而 GNU Screen 就是为这一目的设计的.


GNU screen 工具以及解决方案
------------------------------------------------------------------------------
Screen 是一个命令行工具. 它提供了从多个终端窗口连接到同一个 shell 会话 (会话共享). 当网络中断, 或终端窗口意外关闭是, 中 screen 中运行的程序任然可以运行. 相比之下当系统自带的终端窗口意外关闭时, 在该终端窗口中运行的程序也会终止. 从逻辑上 Screen 相当于能把任何脚本, 命令转为后台运行, 并且允许你随时切换到这个后台运行的 session, 也就是你用起来跟你在 shell 里一样, 但实际上它还在后台. 不过 Screen 的实现原理跟 System Service 完全不一样, 它也不要求你的程序要符合 Service 的标准.


实战案例
------------------------------------------------------------------------------
.. literalinclude:: ./long_running_script.sh
   :language: bash
   :linenos:


.. literalinclude:: ./manager.py
   :language: bash
   :linenos:






简介
------------------------------------------------------------------------------
此文档介绍了当你用 Linux (最好是 Ubuntu) 来部署服务器时, 如何保持服务器 24 小时在线的方法.

**我们会面临以下挑战**

1. 在本地单机上你的机器不可能 24 小时开机, 而且你有可能误操作关闭了游戏服务器命令行窗口.
2. 对于云端部署的情况你通常是用 SSH 连接到远程服务器上然后运行的 authserver / worldserver, 一旦你的 SSH 断开, 远端运行的服务也会断开. 就算你在本地将 SSH 窗口保持不断开, 但你本地机器总是有可能要关机的, 到时候还是会导致服务器被关闭 (参考 1).
3. 游戏服务器 authserver / worldserver 进程有可能会挂掉, 你不可能每次挂掉就立刻 SSH 到服务器上重启.

下面我们来解决这些问题.


GNU screen 工具
------------------------------------------------------------------------------
Screen 是一个命令行工具. 它提供了从多个终端窗口连接到同一个 shell 会话 (会话共享). 当网络中断, 或终端窗口意外关闭是, 中 screen 中运行的程序任然可以运行. 相比之下当系统自带的终端窗口意外关闭时, 在该终端窗口中运行的程序也会终止.

从逻辑上 Screen 相当于能把任何脚本, 命令转为后台运行, 并且允许你随时切换到这个后台运行的 session, 也就是你用起来跟你在 shell 里一样, 但实际上它还在后台. 不过 Screen 的实现原理跟 System Service 完全不一样, 它也不要求你的程序要符合 Service 的标准.

检查 Screen 的版本::

    screen --version

参考资料:

- GNU Screen 官网: https://www.gnu.org/software/screen/manual/screen.html
- GNU Screen 中文维基: https://zh.wikipedia.org/wiki/GNU_Screen


解决方案
------------------------------------------------------------------------------
先找到你构建的 Azeroth Server 的位置. ``cd`` 到 ``bin`` 目录.

然后在该目录下创建 4 个文件, 创建的时候请读一下里面的内容:

- ``auth.sh``: 用于每 20 秒一次如果检测到 authserver 挂了就自动重启:

.. code-block:: bash

    #!/bin/sh
    # content of auth.sh
    # try to run authserver every 20 seconds, if already run, do nothing

    while :; do
    ~/azeroth-server/bin/authserver
    sleep 20
    done

- ``world.sh``: 用于每 20 秒一次如果检测到 worldserver 挂了就自动重启

.. code-block:: bash

    #!/bin/sh
    # content of world.sh
    # try to run worldserver every 20 seconds, if already run, do nothing

    while :; do
    ~/azeroth-server/bin/worldserver
    sleep 20
    done

- ``restarter.sh``: 用 screen 命令对 ``auth.sh``, ``world.sh`` 进行封装, 将这两脚本以 screen session 的方式再后台运行.

.. code-block:: bash

    #!/bin/bash
    # content of restarter.sh
    # this is just an example for usage of screen, it is not used in automation script

    dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    screen -AmdS auth "${dir_here}/auth.sh"
    screen -AmdS world "${dir_here}/world.sh"

- ``shutdown.sh``: 检测运行中的 screen session, 如果找到了就将其杀死

.. code-block:: bash

    #!/bin/bash
    # content of shutdown.sh
    # this is just an example for usage of screen, it is not used in automation script

    screen -X -S "world" quit
    screen -X -S "auth" quit

你可以用任何终端文本编辑器来创建这些脚本, 比如 `vim <https://www.vim.org/>`_ 或者 `nano <https://www.nano-editor.org/>`_.

默认情况下创建的脚本只能被创建者 (也就是你) 执行. 而我们需要让 ``restarter.sh`` 去调用 ``auth.sh`` 就不行了. 你需要打 ``chmod +x auth.sh``, ``chmod +x world.sh`` 将这两个脚本变成可执行的. 不然 ``restarter.sh`` 能够被成功运行, 但实际上没有成功 (后面的 auth / world 服务器没有被运行)

**管理服务器**

启动服务器, 但没有 world console 界面::

    ./restarter.sh

进入 world console session 界面, 如果你按 ctrl + d 退出, 那么这个 session 就被杀死了, 你可以按下 Ctrl + A, 然后按 D (按下 Ctrl + A 之后系统不会给你任何反馈, 你就按 D 就好了) 这样 session 还在::

    screen -r world

启动服务器并且进入 world console session 界面::

     ./restarter.sh; screen -r world

关闭服务器::

    ./shutdown.sh

现在我们理解了解决方案的原理, **但这个方案还是不够好**. 因为如果你连续运行两次 ``restarter.sh``, 就会导致出现多个 auth / world server 的 session 共存. 所以我们需要在运行 ``restarter.sh`` 之前检查一下是不是已经有正在运行着的 session. 但是这个逻辑在 bash script 中比较难实现, 所以我们创建了 ``lib/__init__.py``, 用 Python 来实现这一功能.


终极解决方案
------------------------------------------------------------------------------
``lib/__init__.py`` 用 Python 实现了常用的管理服务器的功能. 然后我们创建了很多小脚本如 ``run_server.py``, ``stop_server.py`` 来调用 ``lib/__init__.py`` 库中的函数, 这些小脚本里面仅仅是 import 然后调用函数.

现在我们可以直接运行这些脚本来达到管理服务器的目的:

- ``python ./chmod.py``: 修改 auth.sh, world.sh 的可执行权限
- ``python ./run_server.py``: 运行游戏服务器
- ``python ./stop_server.py``: 关闭游戏服务器
- ``python ./list_session.py``: 列出正在运行的游戏服务器 session
- ``python ./enter_worldserver.py``: 进入 worldserver 的交互界面, 来输入 GM 命令


参考资料
------------------------------------------------------------------------------
- AzerothCore 项目的服务器自动重启脚本教程: https://www.azerothcore.org/wiki/linux-restarter
