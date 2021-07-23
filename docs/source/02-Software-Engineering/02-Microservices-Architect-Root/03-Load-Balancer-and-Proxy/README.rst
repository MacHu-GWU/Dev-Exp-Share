.. _load-balance-and-proxy:

负载均衡 与 代理
==============================================================================

在探索 AWS 的 微服务网格 服务 AWS App Mesh 时, 发现 AWS 使用的是大名鼎鼎的开源高性能分布式代理 Envoy. 而进一步看 Envoy 博文时, 发现了一篇非常精品的博文, 以及他的翻译版本. 阅读过后, 我把其精华部分摘抄了出来.


什么是负载均衡和代理？
------------------------------------------------------------------------------
Wikipedia 是这么定义的：

在计算世界中，负载均衡通过使用多个计算资源来提高负载的分布。计算资源包括计算机，计算集群，网络链接，CPU，或者硬盘等。负载均衡的目标是优化资源的使用，最大化吞吐量，最小化响应延时，同时避免任何单一资源超载。负载均衡通过冗余，使用多个而不是一个组件提高可靠和可用性。负载均衡器通常包括专门的软件或者硬件，比如一个多层的交换机或者一个 DNS 服务进程。

以上定义适用所有各种计算，不仅仅是网络。操作系统使用负载均衡在物理处理器之间调度任务；容器编排系统（如 Kubernetes）使用负载均衡在计算集群之间调度任务；网络负载均衡器使用负载均衡在不同的后端实例调度网络任务。这篇文章接下来的部分只讨论网络负载均衡。

.. code-block::

    Client <---> Load Balancer <---> Server

Figure 1 显示了一个高度概括的网络负载均衡。Client 从 Backend 请求资源。负载均衡器位于 Client 和 Backend 之间，主要执行以下关键任务：

- 服务发现：哪些 Backend 在系统中是可用的？他们的地址是什么？（比如，负载均衡器如何与 Backend 通信？）
- 健康检查：当前哪些 Backend 是健康的，可以接受请求的？
- 负载均衡：使用什么算法在健康的 Backend 之间调度每一个请求？
- 在分布式系统中，正确使用负载均衡有以下好处：

- 命名抽象：Client 不需要知道每一个 Backend 的地址（服务发现），只需要知道 负载均衡器的地址即可，而负载均衡器的地址可以通过 DNS 或者 IP:Port 的形式给出。
- 容错：通过健康检查和各种算法，负载均衡器可以非常有效的避开故障或者过载的 Backend.
- 成本和性能收益：分布式系统网络很少是同质的 (在同一网络分
区中)，通常是跨越多个网络分区。在一个分区内，网络通常是 under subscribed。不同分区之间，over subscribed 是常态。这里说的 under / over subscription 指的是可通过 NIC (Network Information Controller) 使用的带宽量占路由器之间可用带宽的百分比。智能的负载均衡可以尽可能把流量保持在一个分区内，这样可以增加性能（低延迟）和减少整体的系统成本（在分区之间需要更少的带宽和光纤）


Load Balancer v.s. Proxy 负载均衡器和 Proxy 对比

当我们说到网络 Load Balancer 的时候，Load Balancer 和 Proxy 这两个词基本上是可以互换的。这篇文章里面也把这两个术语认为是相同的。（准确的讲，不是所有的 Proxy 都是 Load Balancer，但是大部分的 Proxy 都把负载均衡作为基本功能）。


Load Balancer 的拓扑类型
------------------------------------------------------------------------------

我们已经大体上说了什么是 Load Balancer，L4 & L7 Load Balancer 的区别，并总结了 Load Balancer 的特性。接下来我们看一下在分布式系统拓扑结构中，Load Balancer 是如何部署的。（下面谈到的这些拓扑结构对 L4 & L7 都是适用的）。

**中间代理 Middle proxy**

Client <---> Load Balancer <---> Backend

Figure 4: Middle proxy load balancing topology

这种拓扑结构应该是大多数读者比较熟悉的一种。这个分类包括硬件设备(厂商有Cisco、Juniper、F5)；云软件方案，比如 AWS 的 ALB & NLB 或者 Google 的 Cloud Load Balancer；还有自主搭建的纯软件解决方案，比如 HAProxy, NGINX 和 Envoy. 中间代理的解决方案的好处是用户使用简单。用户只要通过 DNS 连接 Load Balancer 即可，其他不用关心。缺点就是这种方案的 Load Balancer (即使是一个集群)其实是一个故障单点而且也是规模的瓶颈。一个中间代理通常也是一个黑盒，运维起来困难。观察到的问题有可能出在 Client？也有可能是物理网络？或者中间代理？或者后端？很难确定。

**边缘代理 Edge proxy**

Client <---> Internet <---> Load Balancer <---> Backend

Figure 5: Edge proxy load balancing topology
边缘代理的拓扑其实上是中间代理模式的一个变种，区别是前者的 Client 访问 Load Balancer 是通过公网。在这种场景下，Load Balancer 通常必须提供额外的 gateway 特性，比如 TLS 中断，限速，认证和复杂的流量路由。它的优点和缺点跟中间代理模式的一样。通常不可避免的要为一个面向公网的大型分布式系统专门部署一个 Edge proxy。Client 通常是通过 DNS 访问系统，这对于服务的 owner 来说是不可控的。而且，出于安全考虑，必须有一个单一的 gateway 来让所有的公网流量进入系统。

**嵌入 Client 的库 Embedded client library**

Service + Client Library <---> Backend

Figure 6: Load balancing via embedded client library
为了避免 Middle Proxy 模式的单点故障问题，一些比较复杂的解决方案将 Load Balancer 以库的形式嵌入到服务中，如图6所示。在支持的功能上面，库与库之间的差别很大。在这个分类里面，功能丰富，比较知名的有 Finagle，Eureka/Ribbon/Hystrix，gRPC（主要是调用 Google 内部的 Stubby 系统）。基于库的解决方案主要的优势在于完全将 Load Balancer 的所有功能分布到每一个 Client 中，解决了之前说的单点和扩容的问题。但是这种方案的最大缺点就是需要针对每种使用到的开发语言都要实现一个库，而用不同的语言实现一个非常复杂的网络库，这个成本还是很高的。另外，还要考虑到库的升级，对于一个大型的服务架构来说，要升级一个库也是非常痛苦的，这通常会导致多个版本的库存在，这样维护起来会非常麻烦。

但是只要克服多语言开发和升级的问题，这种方案也是非常成功的。

**跨斗代理 Sidecar proxy**

[Service <---> Client Library] <---> Backend

Figure 7: Load balancing via sidecar proxy
Sidecar proxy 是 Embedded client library 方案的一个变种，如图 7 所示。最近几年这种拓扑方案以 『service mesh』的名字流行起来。Sidecar proxy 的思想就是通过另外一个不同进程来进行网络访问，这样虽然牺牲一点性能，但是却可以解决 Embedded client library 多语言实现的问题。截至撰写本文时，最流行的 sidecar proxy 模式的负载均衡器有 Envoy，Nginx，HAProxy，Linkerd。有关 sidecar proxy 方法更详细的描述请看我的这篇介绍 Envoy 的文章和 service mesh 数据面板和控制面板的对比文章。

不同拓扑类型的优势/劣势总结

- Middle proxy 是最容易使用的一种方案，但是它有单点故障，扩容限制和黑盒操作的问题
- Edge proxy 和 middle proxy 类似
- Embedded library proxy 提供了最好的性能和扩容能力，但是有多语言实现和升级的问题
- Sidecar proxy 的性能虽然没有 embedded library proxy 的好，但是也没有它的限制总之，我认为对于服务之间的通信，sidecar proxy （service mesh）会逐渐取代其他的模式。进入 service mesh 的流量需要先通过 edge proxy.

参考资料:

- 现代负载均衡和代理简介: https://zhuanlan.zhihu.com/p/39575765
