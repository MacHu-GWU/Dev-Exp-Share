Tor Network Docs
==============================================================================

.. contents::
    :depth: 1
    :local:

洋葱网络的作用

洋葱网络本身并不是一个网络, 而是一个通讯协议, 任何在互联网上同意洋葱协议, 并安装并运行着洋葱客户端的电脑互相之间连接在一起, 就组成了洋葱网络.

简单来说, 如果我想

- 如果你想使用洋葱浏览器进行匿名上网, 那么你要到 https://www.torproject.org/download/download-easy.html.en 下载洋葱浏览器软件. 洋葱浏览器会自动连上洋葱网络, 当浏览器关闭时会自动断开. 只有通过洋葱浏览器浏览时才是通过洋葱网络进行的匿名访问. 开着洋葱浏览器而用chrome浏览网页是没有效果的.
- 如果你想要在机器上运行洋葱网络的服务, 然后通过本机的一个端口去和外网通信, (这通常应用于你想用编程来对洋葱网络进行访问的情况). 那么请参考这个教程 https://www.torproject.org/docs/tor-doc-osx.html.en , 使用包管理软件安装tor, 然后使用以下三个命令 ``启动``, ``重启``, ``关闭`` 对洋葱网络进行操作.

    - ``brew services start tor``
    - ``brew services restart tor``
    - ``brew services stop tor``


在爬虫中使用 Tor Network 避免被 Ban IP
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

``tor`` 是一个在 Windows, Mac, Linux (Windows 上的配置很复杂, 不推荐) 上的后台服务. 将你的机器连入洋葱网络, 给你分配一个临时的链路 (也就是从你的 IP, 到中间的跳转机器, 到最终发出真正 HTTP 请求的机器的链路), 在此期间, 你如果查询你的公网 IP, 会得到最终发出真正请求的机器的 IP. 这个链路会根据设置保持一段时间, 并自动更换. 你也可以手动更新. 然后你的 Http 请求不直接走默认 HTTP/HTTPS 端口, 而是通过 tor proxy 代理端口发出.

在爬虫中, 你希望你能够随时切换 IP. 由于 ``tor`` 服务不支持自动更换 IP, 你只能通过手动向其发送 SIGNAL 要求他重新连接, 来获得新的链路.

下面我们来介绍如何实现自动在 Python 爬虫中自动切换 IP.

你需要安装 ``tor`` (洋葱网络主程序), ``privoxy`` (无缓存代理) 两个系统包, 在 MacOS 和 Linux 中的安装略有不同. 以及在 Python 中需要安装 ``requests`` (进行 HTTP 请求), ``pysocks`` (通过 socks 端口通信), ``stem`` (跟 ``tor`` 互动, 发送 reconnect 信号)


Mac 系统
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # 安装 tor, privoxy
    brew install tor
    brew install privoxy

修改 tor 配置文件:

选择一个密码, 用于防止外部程序使用 tor 端口. 例如 "mypassword", 然后使用 ``tor --hash-password mypassword`` (请自行替换你的密码) 计算出 hash 值 (你不会把密码明文保存吧!), 例如 mypassword 的哈希值是 ``16:81A060A2BC85DA2A60D4D81BFD3A8701E99B275CC6C1E7E711B9F1363F``. 然后修改 tor 的配置文件 ``/usr/local/etc/tor/torrc`` (如果没有, 备份 ``/usr/local/etc/tor/torrc.sample`` 并改名即可). 在其中加入以下三个配置 (请自行检查是否有重复, ``#`` 后面的都是注释)::

    ControlPort 9051
    HashedControlPassword 16:81A060A2BC85DA2A60D4D81BFD3A8701E99B275CC6C1E7E711B9F1363F
    CookieAuthentication 1

修改 privoxy 配置文件:

打开 privoxy 的配置文件 ``/usr/local/etc/privoxy/config``. 在其中加入以下配置::

    forward-socks5t / 127.0.0.1:9050 . # the dot at the end is important

然后在后台启动 tor, privoxy. 每次重启电脑后你都需要使用这个命令来启动洋葱网络:

.. code-block:: bash

    brew services start tor
    brew services start privoxy

使用 Python 通过洋葱网络访问网络并切换 IP:

首先安装依赖包:

.. code-block:: bash

    pip install requests
    pip install pysocks
    pip install stem

然后使用下面的代码, 你会看到当重新连接之后, ip 会改变:

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
    Install these packages first:

    .. code-block:: python

        pip install requests
        pip install pysocks
        pip install stem
    """

    import time

    import requests
    from stem import Signal
    from stem.control import Controller

    RENEW_CONNECTION_WAIT_TIME = 5


    def renew_connection():
        """
        Renew tor network connection (change route).
        """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="mypassword")
            controller.signal(Signal.NEWNYM)
            controller.close()
        time.sleep(RENEW_CONNECTION_WAIT_TIME)


    def make_session():
        """
        Make a session to keep connect
        """
        session = requests.session()
        session.proxies = {}
        session.proxies["http"] = "socks5h://localhost:9050"
        session.proxies["https"] = "socks5h://localhost:9050"
        return session


    def check_ip():
        """
        Use Amazon Web Service to check your public IP.
        """
        session = make_session()
        url = "http://checkip.amazonaws.com/"
        return session.get(url).text


    print(check_ip())
    renew_connection()
    print(check_ip())


参考资料:

- Running Tor on Mac OS X: https://2019.www.torproject.org/docs/tor-doc-osx.html


Linux 系统
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linux 有许多主流的发行版, 比如 CentOS, Redhat, Debian, Ubuntu, 以及 Amazon 为云定制的 Amazon Linux. 而 Tor 的安装在 Debian 和 Ubuntu 上最为简单, 可以使用系统自带的包管理工具 apt 安装. 而其他的 Linux 发行版则要么需要配置安装源, 要么需要编译源码安装, 步骤非常繁琐. 所以这里我们以 Ubuntu 为例进行安装.


Ubuntu 系统
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Ubuntu 上的步骤跟在 Mac 上的步骤基本一致, 只有以下几个区别:

- Mac 上的安装命令是 ``brew install tor``, Ubuntu 择有 ``sudo apt install -y tor privoxy``. 在安装前记得运行 ``sudo apt update`` 更新索引.
- Mac 上的配置文件的位置是 ``/usr/local/etc/tor/torrc`` 和 ``/usr/local/etc/privoxy/config``, Ubuntu 则是 ``/etc/tor/torrc`` 和 ``/etc/privoxy/config``.
- Mac 上的启动服务的命令是 ``brew services start tor``, ``brew services start privoxy``, 而 Ubuntu 则是 ``sudo service tor start``, ``sudo service privoxy start`` (可以用 restart 命令替换 start 是的应用最新更改的配置文件).

在 Ubuntu 上的 Python3 是系统所用的 Python, 不建议将一大堆库安装到系统中, 建议使用 virtualenv. 而自带的 Python3 没有 pip, 而 ``python3 get-pip.py`` 会因为缺少 ``distutils`` 而导致失败, 所以要先运行 ``sudo apt install python3-distutils``, 再运行 ``python3 get-pip.py``.


Amazon Linux (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Amazon Linux 默认使用 yum 包管理工具, 但是 Amazon Linux 的 repo 中并没有 tor, 所以你只能从源代码 Build. Build 过程参考官方文档 (本文内容也是根据这篇文档总结的) http://www.torproject.org/docs/tor-doc-unix.html.

1. 下载源代码:

为了避免从非官方渠道下载到带病毒的软件, 请严格根据官方文档中的指引从官方下载.

- 官方下载文档: https://www.torproject.org/download/tor/
- 下载页面 (下载链接在这个页面上找): https://www.torproject.org/download/tor/

.. code-block:: bash

    wget https://dist.torproject.org/tor-0.4.2.5.tar.gz

2. 安装 Build 依赖.

.. code-block:: bash

    sudo yum install -y libevent libevent-devel openssl zlib

3. 进行 Build.

.. code-block:: bash

    tar xzf tor-0.4.2.5.tar.gz # 解压源代码
    cd tor-0.4.2.5 # 进入 $HOME/tor-0.4.2.5

    # 在 $HOME/tor-0.4.2.5/src/app.tor 处 Build, 只能当前的用户使用
    ./configure && make

Build 之后的 tor 命令以及 配置文件的路径分别是::

    ~/tor-0.4.2.5/src/app/tor
    ~/tor-0.4.2.5/src/config/torrc

从源码安装的 tor 没有 service 文件, 所以无法使用 sudo vi /usr/lib/systemd/system/tor.service::

    [Unit]
    Description=Anonymizing Overlay Network
    After=network.target

    [Service]
    User=tor
    Type=simple
    ExecStart=/home/ec2-user/tor-0.4.2.5/src/app/tor -f /home/ec2-user/tor-0.4.2.5/src/config/torrc
    ExecReload=/usr/bin/kill -HUP $MAINPID
    KillSignal=SIGINT
    LimitNOFILE=8192
    PrivateDevices=yes

    [Install]
    WantedBy=multi-user.target


参考资料:

- Crawling the web with TOR: https://medium.com/@amine.btt/a-crawler-that-beats-bot-detection-879888f470eb
- Tor IP Rotation with Python Example: https://github.com/baatout/tor-ip-rotation-python-example
