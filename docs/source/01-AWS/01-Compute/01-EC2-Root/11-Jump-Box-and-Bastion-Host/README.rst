.. _jump-box-vs-bastion-host:

Jump box vs Bastion Host
==============================================================================

在任何企业 IT 基础架构中, 网络安全都是非常重要的一环, 关键的服务器和数据都会被部署到私有网络上, 外部公有网络是无法直接访问这些位于私有网络上的数据的. 例如数据库应用.

而开发者则需要经常从公有网络, 例如自己家里, 访问私有网络上的服务器. 如何在保证网络安全的同时, 能缩短访问的流程, 提高工作效率呢?

Jump Box 和 Bastion Host 都是为了解决这一问题的工具, 简单来说, 这两者都是一台可以从公网访问 (需要密钥或权限), 同时也可以访问私有网络的服务器.

关于 Jump box 和 Bastion host 的区别, 我们可以参考这篇文章 https://www.greenhousedata.com/blog/whats-a-jumpbox-or-bastion-host-anyway.

    JUMPBOXES VS. BASTION HOSTS:

    Both bastion hosts and jumpboxes function similarly: they segregate between one private network or server group and external traffic. Usually you connect to them through SSH or RDP. They each create a single point of entry to a cluster, but their intended purpose and architecture are subtly different in practice.

    A jump server is a virtual machine that is used to manage other systems. It is sometimes called a “pivot server” for this reason: once you are logged in, you can “pivot” to the other servers. It is usually security hardened and treated as **the single entryway to a server group from within your security zone**, or inside the overall network. A jump server is a “bridge” between two trusted networks. The two security zones are dissimilar but both are controlled.

    A bastion host is also treated with special security considerations and connects to a secure zone, **but it sits outside of your network security zone**. The bastion host is intended to provide access to a private network from external networks such as the public internet. Email servers, web servers, security honeypots, DNS servers, FTP servers, VPNs, firewalls, and security appliances are sometimes considered bastion hosts.

简单来说, 两者的主要共同点是, 都是从外部网络访问私有网络的桥梁. 而区别是, Jump box 部署在私有网络内部, 而 Bastion host 则是部署在私有网络的外部. 而 Jump host

共同点:

- 都是从外部网络访问私有网络的桥梁

区别:

- Jump Server: 部署在私有网络 内部
- Bastion Host: 则署在私有网络的 外部

- Jump Server: 是一台部署在私有网络中的虚拟机
- Bastion Host: 可能是 VPN 服务器, 也可以是防火墙, 或是虚拟机

- Jump Server: 用于让用户直接 ssh 进入, 然后再 ssh 连接其他私有网络上的机器
- Bastion Host: 通常是一个节点, 直接将用户的请求 forward 到私有网络上的机器, 在使用上用户无需登录 bastion host

- Jump Server: 比较初级的网络安全防范
- Bastion Host: 比较高级的网络安全防范, 必须要有日志记录所有的访问

