Hashicorp Packer
==============================================================================


Summary
------------------------------------------------------------------------------
Packer 是运维开源软件公司 Hashicorp 的一款专注于虚拟机镜像 (VM Image, 下简称 img) 构建的工具. 大名鼎鼎的 terraform 也是 Hashicorp 的产品. Packer 首次发布于 2013 年, 直到 2017 年起 API 趋于稳定, 发布了 1.0 版本.

这里有必要解释一下 Packer 具体解决了什么问题. 传统的构建 img 的方式是先用 base img 启动一个虚拟机, 然后进去运行一些命令安装软件, 配置环境. 然后退出打包. 这个过程在早期可以在本地电脑上运行, 但这样会有本地电脑和最终运行的服务器平台不一致的问题. 所以后来一般都是 SSH 到服务器上进行, 不过 SSH 到服务器上运行命令会麻烦一些. 到了云时代, 主机都在云上了. 而 Packer 就是一款让你专注于编写构建的逻辑, 而它能帮你把远程连接, 构建, 打包等操作都帮你做好的工具.

还有另一款大名鼎鼎的运维工具 Ansible, 它和 Packer 的功能有一小部分重合, 大部分不一样. Ansible 专注的是在已经启动好的远程服务器上运行命令, 并且专注的是批量管理. 它的杀手功能是将配置逻辑模块化, 使得可以方便的排列组合. 而 Packer 只是专注于 img 构建.

下面几个链接可能是你学习 Packer 过程中最常用的几个:

- Packer 官网: https://developer.hashicorp.com/packer
- Packer 官方教程: https://developer.hashicorp.com/packer/tutorials
- Packer API 文档: https://developer.hashicorp.com/packer/docs


Table of Content
------------------------------------------------------------------------------
.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
