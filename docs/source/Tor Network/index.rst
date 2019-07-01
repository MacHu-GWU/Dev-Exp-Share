Tor Network
==============================================================================

- 如果你想使用洋葱浏览器进行匿名上网, 那么你要到 https://www.torproject.org/download/download-easy.html.en 下载洋葱浏览器软件. 洋葱浏览器会自动连上洋葱网络, 当浏览器关闭时会自动断开. 只有通过洋葱浏览器浏览时才是通过洋葱网络进行的匿名访问. 开着洋葱浏览器而用chrome浏览网页是没有效果的.
- 如果你想要在机器上运行洋葱网络的服务, 然后通过本机的一个端口去和外网通信, (这通常应用于你想用编程来对洋葱网络进行访问的情况). 那么请参考这个教程 https://www.torproject.org/docs/tor-doc-osx.html.en , 使用包管理软件安装tor, 然后使用以下三个命令 ``启动``, ``重启``, ``关闭`` 对洋葱网络进行操作.

    - ``brew services start tor``
    - ``brew services restart tor``
    - ``brew services stop tor``


在爬虫中使用 Tor Network 避免被 Ban IP
------------------------------------------------------------------------------

Tor Network 是一个在本地运行的服务, 你可以用 requests + pysocks, 将 http get url 发送到 Tor 的端口, Tor 会将你的请求经过几次路由后由洋葱网络上的朋友发出, 然后再将结果转发给你. **洋葱网络不适合需要登录的爬虫**.

相关的 Python 库

- requests + pysocks
- scrapy + pysocks
