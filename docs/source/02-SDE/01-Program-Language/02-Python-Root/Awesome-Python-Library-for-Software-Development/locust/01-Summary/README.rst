.. _python-locust-summary:

Locust - Summary
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Python 实现的一款分布式, 压力测试工具.


How it Works
------------------------------------------------------------------------------


基础
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Locust 的底层是一个基于协程, 异步的高并发框架. 而 Application Level 则是提供了方便的 decorator 语法, 允许你定义 User, 用于模拟一个真实的用户. 以及 task 用户模拟用户的行为, 通常是发起 http request 请求, 当然你也可以用来做数据库 IO.

然后 Locust 提供了两个使用方式. 杀手级的是一个用 flask 做的运行在本地的 web GUI, 也是一个控制台和监控面板. 只需要几个点击就可以选择要模拟多少个用户并发, 以及给出实时的并发 request 数, 最大, 最小, 平均响应时间等信息. 点击结束时则会把数据汇总, 生成统计报告. 只能说一个牛逼了得. 第二个工具则是命令行, 没有 GUI 但是用 ASCII Table 的形式生成 dashboard, Ctrl C 结束后则生成汇总数据.

所以这里的核心概念有:

- User
- task
- Locust Web GUI
- CLI

Locust 由于使用的是协程, 所以完全可以单机达到每秒 1000 的并发量. 同时它还支持集群部署, 比如 AWS EC2 以进一步提高测试性能. 这个话题很大就不展开了.


非 HTTP Load Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Locust 最常用的当然是用作 Http Load Test, 比如网站的响应, API 的响应. 但是很多 Load Test 是跟 HTTP 无关的, 例如数据库系统. Locust 对 Request / Response 做了一层抽象, 并且能将任何 Python 函数变成支持用协程异步执行, 所以用户可以自己显示 Request / Response 的行为, 并生成统计信息 (主要是时间), 然后把这些信息发送给特定的 Locust 主循环 events 使得 Locust 可以对其进行统计. 下面我们详细讲一下我们如何实现 Custom Test:

这里涉及两个概念:

1. ``from locust import events``, 这是 Locust 内置的 event listener, 你自己实现的 task 函数的结果需要发送给这个 event.
2. ``request_meta``, 这是一个 dict 数据, 包含了 dashboard 上你能看到的一些统计数据. 用自带的 HTTPUser 是可以自动生成 ``request_meta`` 的, 而你用自己实现的 User 则需要自己负责生成这个数据. ``request_meta`` 长这个样子::

    request_meta = {
        "name": name, # 就是一个 identifier
        "request_type": "grpc", # 标记这个 request type 是什么
        "context": None, # 上下文, 环境信息
        "exception": None, # 抛出的异常
        "start_time": time.time(),
        "response": None, # 响应
        "response_length": 0, # 响应的数据包大小
        "response_time": 0, # 响应的耗时, 浮点数, 单位秒
    }

最终你的 task 函数里只需要有这么一行, Locust 就能获得该次 Request 的统计数据了::

    events.request.fire(**request_meta)


分布式部署
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
所谓 Locust 集群的本质就是多台能够通过网络互相通信的虚拟机. 一台作为 master, 其他作为 worker. master 不 run 任何 task, 只负责通知 slack 启动 task, 并接受统计数据, 以及提供 web UI. 配置集群的步骤是这样的:

1. 配置网络以及 1 个 Master + N 个虚拟机.
2. 所有的机器上都装了 Python, Locust, 以及 User, task 的测试代码和 requirements.txt 依赖.
3. 先用 CLI 启动 master, master 默认监听 5557 端口. 并记录下 master 的私网 IP
4. 再用 CLI 启动 worker, 并把 master 的 IP 作为启动参数. worker 不会有 UI, worker 用这个 IP 与 master 通信.

你在 master 启动测试的时候可以设置至少有几个 worker connect 上了才开工. 所以这些空闲资源是可以被复用的, 也就是一个集群可以供很多个项目分享使用.

详情请参考官方文档: https://docs.locust.io/en/stable/running-locust-distributed.html#

分布式部署
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


简介
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


以 VM 虚拟机的形式部署
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以 Docker 容器的形式部署
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://docs.locust.io/en/stable/running-in-docker.html


Quick Links
------------------------------------------------------------------------------
Locust 的文档质量很高, 很值得一读:

- 如何写 Locustfile: http://docs.locust.io/en/stable/writing-a-locustfile.html
- 不用 Web GUI, 而用 CLI 启动并统计: http://docs.locust.io/en/stable/running-without-web-ui.html
- 非 HTTP 服务器的测试, 例如数据库测试: http://docs.locust.io/en/stable/testing-other-systems.html?highlight=RPC#
- 分布式部署: https://docs.locust.io/en/stable/running-locust-distributed.html#