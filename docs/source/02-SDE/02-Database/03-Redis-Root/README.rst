.. _redis:

Redis
==============================================================================

.. contents::
    :depth: 1
    :local:


基础概念
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


Redis 解决了什么问题
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redis 是一款超高性能的, 基于内存的, Key Value NoSQL 数据库.





开发实战
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


操作数据的 API (CRUD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :depth: 1
    :local:

- 官方文档: https://redis.io/commands


基础的 CRUD
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


SET
******************************************************************************

- Ref: https://redis.io/commands/set

Example::

    redis> SET mykey "Hello"
    "OK"
    redis> GET mykey
    "Hello"
    redis> SET anotherkey "will expire in a minute" EX 60
    "OK"


GET
******************************************************************************

- Ref: https://redis.io/commands/get

Example::

    redis> GET nonexisting
    (nil)
    redis> SET mykey "Hello"
    "OK"
    redis> GET mykey
    "Hello"


EXISTS
******************************************************************************

- Ref: https://redis.io/commands/exists

Example::

    redis> SET key1 "Hello"
    "OK"
    redis> EXISTS key1
    (integer) 1
    redis> EXISTS nosuchkey
    (integer) 0
    redis> SET key2 "World"
    "OK"
    redis> EXISTS key1 key2 nosuchkey
    (integer) 2


DEL
******************************************************************************

- Ref: https://redis.io/commands/del

Example:

    redis> SET key1 "Hello"
    "OK"
    redis> SET key2 "World"
    "OK"
    redis> DEL key1 key2 key3
    (integer) 2


SCAN
******************************************************************************

遍历所有的 Key Value, 可以根据 Value 的进行 filter 选择一部分数据,


事务
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Redis 部分支持事务.

Redis 用命令 ``MULTI`` 标注事务的开始, 将多个命令缓存在服务器上的 Queue 里, 然后一次性按顺序 EXEC. 如果中间有一个命令出错了, 其他命令也会继续被执行, Redis **不会回滚**. 这种机制下并不能保证多个命令的原子性. **但是能防止客户端在跟服务器通信的过程中出现的网络错误**, 例如 3 条命令中第一条发出去了结果网咯断了导致后面的发不出去, 这样第一条不会被执行. **代价就是无法检测到命令中的逻辑错误**, 三条命令中的第一条是 你对一个 String 进行 Append 操作, 由于命令只是被缓存了, 并没有被执行, 所以服务器也不会发现这个错误, 也不会打断你继续发送后面的命令, 导致最终执行所有命令的时候才会发现这个错误, **导致后面两条命令被错误滴执行**.

所以使用 Redis 事务的时候一定要小心. 要仔细检查命令本身有没有逻辑错误, 要能保证一个事务中的所有命令都可以被执行成功.

