.. _postgres:

Postgres
==============================================================================

.. contents::
    :depth: 1
    :local:


逻辑结构管理
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


数据库逻辑结构介绍
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``Postgres 数据库服务`` (或叫实例): 就是一个单点部署, 或是一个集群部署就是一个 Postgres DB 服务. 一个服务会以 Endpoint (host / port) 的形式暴漏给外界.
- ``数据库`` (Database): 一个 ``Postgres 数据库服务`` 可以管理多个 ``数据库``. 当应用连接到一个数据库时, 一般只能访问这个数据库中的数据, 除非用 DB Link 等手段
- ``表, 索引`` (Relation, Index): 一个 ``数据库`` 中可以有很多表, 索引. 在 Postgres 中表的术语叫 Relation, 其他数据库中则通常叫 Table
- ``数据行`` (Tuple): 每张表中都有很多行数据. 在 Postgres 中行的术语叫 Tuple. 其他数据库中则叫 Row

注意: 在 Postgres 中, 一个 ``Postgres 数据库服务`` 下可以有多个 ``数据库. 但一个数据库不能属于多个实例. 这与 Oracle 数据库不同, 在 Oracle 数据库中, 一个实例只能有一个数据库, 但一个数据库可以在多个实例中 (如 RAC)


模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


高可用性方案设计
------------------------------------------------------------------------------


高可用架构基础
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通常数据库的高可用方案都是让多个数据库协同工作. 跟 Web 服务器高可用方案不一样的是, Web 服务器是无状态的, 而数据库中有数据, 也就是说有状态的. 我们需要在多个数据库之间同步数据. **所以数据同步是数据库高可用性的基础**.

**数据同步可靠性设计**:

从解决数据同步问题的方式来看, 高可用方案可以分为以下几种:

- 共享磁盘的失效切换 或 磁盘的底层复制方案: 使用共享存储, 如 SAN (Storage Area Network) 存储, 一台机器故障后, 把 SAN 存储输出的磁盘挂载到另一台机器上, 然后把磁盘上的文件系统挂起来完成切换.
- WAL (Write Ahead Log) 日志同步, 或 流复制 同步方案: Postgres 自身提供了这种方案, 通过该机制可以搭建 主 / 从 数据库
- 基于触发器的同步方案: 使用触发器记录数据变化, 然后同步到另一台数据库上
- 基于语句复制的中间件: 客户端不直接连接到底层数据库, 而是连接到一个中间件, 中间件把数据库的变更发送到底层多台数据库上完成数据同步

**服务的可靠性设计**:




