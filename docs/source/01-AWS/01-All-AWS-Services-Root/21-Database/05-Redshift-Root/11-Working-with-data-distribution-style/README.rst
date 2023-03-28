.. _aws-redshift-working-with-data-distribution-style:

Working with data distribution style
==============================================================================
Keywords: AWS Redshift, distribution key

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/t_Compressing_data_on_disk.html

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Data distribution concepts
------------------------------------------------------------------------------
Redshift 架构中有 Node, Slice 的概念. 和大多数分布式系统一样, 一个 Node 就是一个有单独 CPU 内存 磁盘的机器, 通常是虚拟机. 一个 Slice 则对应着 ElasticSearch 中的 Shard 的概念, 通常对应着一个 CPU 核心, 有时候也会有多个 Slice 对应一个 CPU 核心的情况. 对于一个 Table 中的数据, 一个 Column 会被指定为 Distribution key, 用于决定一个 Row 的数据最终由哪个 Node 和哪个 Slice 负责处理.


Distribution Style
------------------------------------------------------------------------------
- Key: 就是根据 distribution key 计算出一个 hash, 用这个 hash 决定具体由哪个 node 哪个 slice 处理. 这是最常用的情形. 通常用于比如 cardinality 很高的列, 比如几百万条 order id.
- Even: 就是 round robin, 系统维护一个全局序号, 不断从 0 ~ (N-1) 循环, N = node * slices per node.
- All: 每个数据在所有的 Node 都有一个副本. 该方式主要用于提高用小的 dimension table 做 join 时的性能. 比如你有个 business code, 只有 200 多个值, 你经常需要做 join 以获得人类可读的对 business code 的解释, 那么这个表就是和用 All
- Auto: 让 redshift 自动决定, 在数据量小时用 All, 随着数据增加变成 Even.


Viewing distribution styles
------------------------------------------------------------------------------
Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/viewing-distribution-styles.html

你可以以下的 SQL 语句获得每个表的 distribution key.

.. code-block:: SQL

    select "schema", "table", diststyle from SVV_TABLE_INFO

其中 distribution style code 的含义对应如下::

    0	EVEN
    1	KEY
    8	ALL
    10	AUTO (ALL)
    11	AUTO (EVEN)
    12	AUTO (KEY)


Evaluating query patterns
------------------------------------------------------------------------------
评估你的 Query 是决定表设计很重要的一步. 你需要找到你用的最多的表, 以及对最常用的 query 做相应的优化.


Designating distribution styles
------------------------------------------------------------------------------

1. Specify the primary key and foreign keys for all your tables.

    Amazon Redshift does not enforce primary key and foreign key constraints, but the query optimizer uses them when it generates query plans. If you set primary keys and foreign keys, your application must maintain the validity of the keys.

    虽然 Redshift 不强制 primary key 和 foreign key constrain, 但是这些定义是可以被 query optimizer 所利用对 query 进行优化的. 当然你自己需要对 primary key 的唯一性, 以及 foreign key 的存在性负责.

2. Distribute the fact table and its largest dimension table on their common columns.

    Choose the largest dimension based on the size of dataset that participates in the most common join, not just the size of the table. If a table is commonly filtered, using a WHERE clause, only a portion of its rows participate in the join. Such a table has less impact on redistribution than a smaller table that contributes more data. Designate both the dimension table's primary key and the fact table's corresponding foreign key as DISTKEY. If multiple tables use the same distribution key, they are also collocated with the fact table. Your fact table can have only one distribution key. Any tables that join on another key isn't collocated with the fact table.

    最大的 fact table 中最常用于做 join 的 key 以及对应的 dimension table 的 join 的 key 都设置为 distribution key. 这点跟大数据范式有所不同. 通常大数据系统中里的 distribution key 往往是 primary key, 也是 cardinality 最高的一个, 这样能最大利用分布式系统的吞吐量. 比如 Kafka, AWS Kinesis Stream, ElasticSearch 都是这么做的. 而 Redshift 中我们往往用非 primary key, 但是仍然 cardinality 比较高且常用来做 join 的 key 作为 distribution key. 比如电商系统中的三大 entity, order, user, item. 显然 order 是最大的 fact table 因为他集中了 user 和 item 的信息. 从数量上来说, user 的数量更多, 而 item 的数量比 user 少. 但是同一个 order 中会有很多个 item, 但只会有一个 user. (用 user_id 还是 item_id 做 distribution key 我还没想明白)

3. Designate distribution keys for the other dimension tables.

    Distribute the tables on their primary keys or their foreign keys, depending on how they most commonly join with other tables.

    对于其他的 dimension table, 一般把他们最常用与和其他表作 JOIN 的 column 作为 distribution key

4. Evaluate whether to change some of the dimension tables to use ALL distribution.

    If a dimension table cannot be collocated with the fact table or other important joining tables, you can improve query performance significantly by distributing the entire table to all of the nodes. Using ALL distribution multiplies storage space requirements and increases load times and maintenance operations, so you should weigh all factors before choosing ALL distribution. The following section explains how to identify candidates for ALL distribution by evaluating the EXPLAIN plan.

    如果 dimension table 较小, 可以考虑使用 ALL 以提高 join 性能.

5. Use EVEN distribution for the remaining tables.

    If a table is largely denormalized and does not participate in joins, or if you don't have a clear choice for another distribution style, use EVEN distribution.

    如果一个 fact table 已经是 denormalized 的, 基本上不需要 join, 那么使用 EVEN 就很不错.


Evaluating the query plan
------------------------------------------------------------------------------
我们在设计表结构时通常要先创建表, 插入测试数据, 把 business query 用 ``EXPLAIN`` 命令解析一边. `这篇官方文档 <https://docs.aws.amazon.com/redshift/latest/dg/c_data_redistribution.html>`_ 主要是教你如何理解 explain 的结果中与 distribution key 有关的部分.


Query plan example
------------------------------------------------------------------------------
一些实际例子

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/t_explain_plan_example.html


Distribution examples
------------------------------------------------------------------------------
一些实际例子

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_Distribution_examples.html
