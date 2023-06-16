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
这里我们有一个每三秒打印一次系统时间的程序, 我们希望永久运行该程序.

.. literalinclude:: ./long_running_script.sh
   :language: bash
   :linenos:

下面是实现永久运行该程序的代码. 请按照顺序依次取消注释, 每次只保持有一行被运行, 来一步步的, 启动脚本, 查看脚本, 进入会话, 关闭脚本. 其中 **进入会话** 这一步必须在 Terminal 中进行. 不能用 IDE.

- ``run_script(path_long_running_script_sh, name)``
- ``list_session()``
- ``enter_session(name)``
- ``stop_script(name)``

.. literalinclude:: ./manager.py
   :language: bash
   :linenos:


参考资料
------------------------------------------------------------------------------
- GNU Screen 官网: https://www.gnu.org/software/screen/manual/screen.html
- AzerothCore 项目的服务器自动重启脚本教程: https://www.azerothcore.org/wiki/linux-restarter
