.. _container-technique-history:

Container Technique History
==============================================================================
Keywords: Docker Container History

本文对容器技术的历史做一个简短的介绍.

通常谈到容器技术都指的是 Linux 容器技术. Linux 容器技术始于 2000 年, 虽然从 2016 年其 Windows 2016 Server 开始支持 Windows 容器, 但是 Linux 容器仍然是市场主流, 所以本文谈到的容器技术都值得是 Linux 容器技术.


2000 年 FreeBSD Jain 时代
------------------------------------------------------------------------------
我们现在称为容器技术的概念最初出现在 2000 年, 当时称为 FreeBSD jail, 这种技术可将 FreeBSD 系统分区为多个子系统 (也称为 Jail). Jail 是作为安全环境而开发的, 系统管理员可与企业内部或外部的多个用户共享这些 Jail.

2001 年, 通过 Jacques Gélinas 的 VServer 项目, 隔离环境的实施进入了 Linux 领域. 在完成了这项针对 Linux 中多个受控制用户空间的基础性工作后, Linux 容器开始逐渐成形并最终发展成了现在的模样. 

很快, 更多技术结合进来, 让这种隔离方法从构想变为现实. 控制组 (cgroups)是一项内核功能, 能够控制和限制一个进程或多组进程的资源使用. 而 systemd 初始化系统可设置用户空间, 并且管理它们的进程, cgroups 使用该系统来更严密地控制这些隔离进程. 这两种技术在增加对 Linux 的整体控制的同时, 也成为了保持环境隔离的重要框架. 


2008 LXC (Linux Container Runtime) 技术
------------------------------------------------------------------------------
终于, 在2008年, LXC横空出世, LXC作为集大成者, 采集众家之所长, 有了前期的N多铺垫, 终于有了容器技术的雏形. LXC的主要两大依托就是namespace和Cgroups, 一个做资源隔离, 解决进程可以用什么资源的问题；一个做资源控制, 解决进程可以用多少资源的问题. 

进程在运行时, 除了CPU和内存外, 其实还需要很多其他资源, 为了将其隔离, 需要将资源一并隔离, 如网络、文件系统、IPC等, 什么是namespace？

    A namespace wraps a global system resource in an abstraction that  makes it appear to the processes within the namespace that they have their own isolated instance of the global resource.  Changes to the global resource are visible to other processes that are members of the namespace, but are invisible to other processes. One use of namespaces is to implement containers.

namespace的存在, 使得每个进程都以为自己是单独的存在, 拥有独享的必要资源, 其实是被划分到一个单独的隔离区域. 


2013 年 进入 Docker 技术时代
------------------------------------------------------------------------------
2008 年, Docker 公司凭借与公司同名的容器技术通过 dotCloud 登上了舞台. Docker 技术带来了很多新的概念和工具, 包括可运行和构建新的分层镜像的简单命令行界面、服务器守护进程、含有预构建容器镜像的库以及注册表服务器概念. 通过综合运用这些技术, 用户可以快速构建新的分层容器, 并轻松地与他人共享这些容器.

`2013-03-23 <https://docs.docker.com/engine/release-notes/prior-releases/#010-2013-03-23>`_ Docker 公司发布了 Docker 引擎的第一个版本. Docker优秀的设计使得它非常流行, 像 Warden 一样, 期初也是基于 LXC 的, 后来就以自己的 libcontainer 来替代了, Docker 之所以如此流行, 一个重要的原因就是提供了一个完整的解决方案生态系统, 使得易用, 简单, 这是它的前辈们所做不到的, 历史上的解决方案看起来都有 Docker 的影子, 但是都有各种各样的不足, Docker 几乎解决了所有的痛点, 变得非常易用.


2014 K8S (Kubernetes) 技术
------------------------------------------------------------------------------
Docker 引爆了容器技术, 加上微服务的加持, 使得二者发展迅速, 但是容器更像是一个好玩的玩具, 如何在产线上工业化的使用起来? 网络问题, 负载均衡问题, 监控, 部署, 更新, 镜像管理, 发布... 需要解决很多很多问题, 因此容器的编排应运而生, k8s 在 2014 年横空出世, 说横空出世或许有点夸张, 因为它是基于谷歌内部建设了十几年的 Borg 构建的开源版本, 实践出真知, 因此很快就成为容器编排事实上的标准.

我们可通过 3 个主要标准, 来确保各种容器技术间的互操作性, 即 OCI 镜像、分发和运行时规范. 通过遵循上述规范, 社区项目、商用产品和云技术提供商可以构建可互操作的容器技术 (可将您自行构建的镜像, 推送至云技术提供商的注册表服务器——完成这一操作后, 镜像才能正常工作). 当前, 红帽和 Docker 等公司都是开放容器计划 (OCI) 的成员, 致力于实现容器技术的开放行业标准化.


Docker 在商业市场的陨落以及跟巨头们的纷争
------------------------------------------------------------------------------
2.1 发展

随着 Docker 的日益成熟, 一些人开始在 Docker 之上创造更加强大的工具, 一些人开始在 Docker 之下为其提供更稳定的运行环境.

其中一个叫作 Google 的公司在 Docker 之上创建了名为 "Kubernetes" 的工具，Kubernetes 操纵 Docker 完成更加复杂的任务; Kubernetes 的出现更加印证了 Docker 的强大, 以及 "容器纪元" 的发展正确性.

2.2 野心

当然这是一个充满利益的世界, Google 公司创造 Kubernetes 是可以为他们带来利益的, 比如他们可以让 Kubernetes 深度适配他们的云平台, 以此来增加云平台的销量等; 此时 Docker 创始人也成立了一个公司, 提供 Docker 的付费服务以及深度定制等; 不过值得一提的是 Docker 公司提供的付费服务始终没有 Kubernetes 为 Google 公司带来的利益高, 所以在利益的驱使下, Docker 公司开始动起了歪心思: 创造一个 Kubernetes 的替代品, 利用用户粘度复制 Kubernetes 的成功, 从 Google 嘴里抢下这块蛋糕! 此时 Docker 公司只想把蛋糕抢过来, 但是他们根本没有在意到暗中一群人创造了一个叫 "rkt" 的东西也在妄图夺走他们嘴里的蛋糕.

2.3 冲突

在一段时间的沉默后, Docker 公司又创造了 "Swarm" 这个工具, 妄图夺走 Google 公司利用 Kubernetes 赢来的蛋糕; 当然, Google 这个公司极其庞大, 人数众多, 而且在这个社会有很大的影响地位.

终于, 巨人苏醒了, Google 联合了 Redhat, Microsoft, IBM, Intel, Cisco 等公司决定对这个爱动歪脑筋的 Docker 公司进行制裁; 当然制裁的手段不能过于暴力, 那样会让别人落下把柄, 成为别人的笑料, 被人所不耻; 最总他们决定制订规范, 成立组织, 明确规定 Docker 的角色, 以及它应当拥有的能力, 这些规范包括但不限于 CRI, CNI 等; 自此之后各大公司宣布他们容器相关的工具只兼容 CRI 等相关标准, 无论是 Docker 还是 rkt 等工具, 只要实现了这些标准, 就可以配合这些容器工具进行使用.

2.4 结局

自此之后，Docker 跌下神坛, 各路大神纷纷创造满足 CRI 等规范的工具用来取代 Docker, Docker 丢失了往日一家独大的场面, 最终为了顺应时代发展, 拆分自己成为模块化组件; 这些模块化组件被放置在 `mobyproject <https://mobyproject.org/>`_ 中方便其他人重复利用.

时至今日, 虽然 Docker 已经不负以前, 但是仍然是容器化首选工具, 因为 Docker 是一个完整的产品, 它可以提供除了满足 CRI 等标准以外更加方便的功能; 但是制裁并非没有结果, Google 公司借此创造了 cri-o 用来满足 CRI 标准, 其他公司也相应创建了对应的 CRI 实现; 为了进一步分化 Docker 势力, 一个叫作 Podman 的工具被创建, 它以 cri-o 为基础, 兼容大部份 Docker 命令的方式开始抢夺 Dcoker 用户; 到目前为止 Podman 已经可以在大部份功能上替代 Docker.


Reference
------------------------------------------------------------------------------
- `什么是 Linux 容器？ <https://www.redhat.com/zh/topics/containers/whats-a-linux-container>`_: Redhat 官网对 Linux 容器的介绍.
- `容器技术发展简史 <https://zhuanlan.zhihu.com/p/358548091>`_: 知乎上的技术博文.
- `Podman 初试 - 容器发展史 <https://mritd.com/2019/06/26/podman-history-of-container/>`_: 一篇 Kovacs 写的博文.
