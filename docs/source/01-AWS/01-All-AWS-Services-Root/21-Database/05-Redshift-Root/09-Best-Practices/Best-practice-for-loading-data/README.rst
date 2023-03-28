.. _aws-redshift-best-practice-for-loading-data:

Best practice for loading data
==============================================================================
Keywords: AWS Redshift, best practice, load data,

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_loading-data-best-practices.html

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Use a COPY command to load data
------------------------------------------------------------------------------
在其他数据库系统中, 批量 load 数据主要靠的是 bulk insert API. 这个 SQL 的语法和这个例子很相似:

.. code-block:: SQL

    // table = user, 有 id (integer), name (string) 两个 column
    INSERT INTO user
    VALUES
        (1, "alice"),
        (2, "bob"),
        (3, "cathy");

这个过程的本质是用 SQL 文本作为数据 IO 的 protocol. 全部过程有如下步骤:

1. 在 SQL client 将数据编译成 SQL 文本
2. 把 SQL 文本通过网络传输给数据库
3. 数据库把 SQL 文本 parse 成数据

在 AWS Redshift 中, **COPY FROM AWS S3 在 99% 的情况下都是 Load 大量数据的最佳选择**. 原因如下.

首先 SQL client 将数据编译成 SQL 文本这一步骤完全不需要了, 这一步骤转变成了将数据序列化为常用的数据格式例如 CSV, JSON, Parquet 等再存到 AWS S3 上. 专业的数据格式序列化要比 SQL client 文本编译效率高的多, 并且 upload 到 S3 可以利用 parallel upload, 并且从客户端到 S3 网络的速度也会比从客户端到 Redshift 快得多, 因为 Redshift 要部署在 VPC 以内, 比 S3 API 多了 internet gateway 等几个额外步骤.

其次 Redshift 从 AWS S3 读取数据的网络走的是 AWS 的内网, 速度极快. 这比把 SQL 文本通过网络传输给数据库要快得多. 其次 S3 上的数据可以是被压缩后的, 这能进一步减少 IO 开销, 并且在 Redshift 服务器上解压的速度也很快, 这点解压消耗比 IO 少多了.

最后, Redshift 把数据格式文件反序列化为数据的速度要比把 SQL 文本 parse 成数据要快得多.

综上所述, 由于 Redshift 是云原生应用, COPY FROM S3 是最优选择.

另外, 由于 Redshift 是个数据仓库, 不是关系数据库, primary key / foreign key constrain 都只是作为 query analyzer 的参考而没有实际的限制, 所以关系数据库中 bulk insert 时 primary key integration error 错误完全不可能发生, S3 copy 只要数据格式对, 是 100% 成功的.


Use a single COPY command to load from multiple files
------------------------------------------------------------------------------
如果用单个 COPY 命令从 Manifest 清单文件中定义的多个 S3 文件中 load 数据, 会自动启用 parallel load, 也就是用多个 node 多个 CPU 同时 load 不同的文件.

而你同时运行多个 COPY 命令, 每个 COPY 命令只读取一个 S3 文件, 则 Redshift 内部需要将这些 COPY 命令按照顺序执行, 一个执行完了才能执行下一个. 该方式要比前一种方法慢很多, 并且每次 COPY 命令执行完之后都要执行 VACUUM 如果

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-single-copy-command.html


Split your load data ofr Parallel load
------------------------------------------------------------------------------
parallel load 能做到:

1. 并行读取多个 压缩后的小文件, 每个 slice 读一个
2. 并行读取单个 未压缩, 分隔符为主的数据格式 (例如 CSV, JSON), 数据被按行分段每个 slice 负责读取一定的行数

parallel load 不能做到

1. 并行读取单个 压缩后的大文件.

Redshift 建议你把文件分割成压缩后大约 1 - 125MB 每个的大小, 这样效率最高.

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html


Compress your data files
------------------------------------------------------------------------------
Redshift 支持读取 gzip, lzop, bzip2, or Zstandard 压缩格式的数据文件. 前面说了, 压缩后节约的网络 IO 时间要远远大于解压缩的额外开销.


Load data in sort key order
------------------------------------------------------------------------------
简单来说就是 COPY 的文件顺序如果能按照 Sort Key 排序好, 那么可以跳过入库后的 VACUUM 阶段, 从而提高效率. 换言之就是避免外排序.

COPY 每次读取一个文件之后, 在写入到数据库之前会按照 Sort Key 进行内排序, 然后 append 到磁盘数据的最后面. 如果你 COPY 的文件的顺序比如第一个文件的数据的 sort key 永远小于第二个文件, 那么磁盘上的顺序和 sort key 肯定就是一致的. 如果 COPY 的顺序错了, 就需要做 VACUUM.


Use time-series tables
------------------------------------------------------------------------------
time series table 的意思就是你可以按照时间分表, 例如每个表负责一个月的数据. 这样错有几个好处:

1. 容易删除旧数据, 你可以直接 drop 旧表, 从而避免在大表上执行 delete by query 操作, 并且避免 VACUUM
2. 插入新数据永远是在大小可控的小表上进行, 这样每次 VACUUM 排序的速度较快, 从而写入性能更好

从查询的角度, 你可以创建一个 ``UNION ALL`` 的 view, 然后查询都走这个 view, 这样就跟用一个大表没什么区别了. 你只要每次 drop 旧表或是 create 新表之后, 记得更新这个 view 即可.

当然 ``UNION ALL`` 的本质是将你的 query 分给各个表, 最后把查询结果合并, 这不像 Glue Catalog 中的 Partition key, 你是无法自动利用对于人类有意义表名的时间范围信息来跳过一些表的. 所以最佳实践是根据你的查询模式, 建立比如 最近 1 年的 VIEW, 最近 3 个月的 VIEW, 最近 1 个月的 VIEW, 每次查询走不同的 VIEW 来减少扫描的数据.

由于最小的 node 可以最多创建 9,900 个 table, 所以就算按照每天一个 table, 你也够保存约 20 年的数据, 基本够用了.


Use a staging table to perform a merge (Upsert)
------------------------------------------------------------------------------
对于 Upsert 操作, 比如你要插入很多行, 一部分是 update, 一部分是 insert. 这时用 staging table 临时表就比较好.


Schedule around maintenance windows
------------------------------------------------------------------------------
如果系统维护期间你有未完成的 query, 那么这个 query 会被杀死, 并且回滚