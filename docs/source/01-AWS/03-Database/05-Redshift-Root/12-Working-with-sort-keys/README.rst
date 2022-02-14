.. _aws-redshift-working-with-sort-keys:

Working with sort keys
==============================================================================
Keywords: AWS Redshift

Redshift 内部的列式存储使用 1MB 作为 block size, 每个 block 的最大值和最小值是作为 metadata 储存的. 这使得 Redshift 可以快速跳过很多无关 block, 定位到查询结果需要的 data 上.

Redshift 在创建表时如果没有指定 Sort key, 它会先将所有的 row 在磁盘上顺序存储. 当你 run 了很多 query 以后 redshift 会分析 query 的频率, 找出哪个 column 作为 sort key 能最大程度增加 performance, 然后对 table 自动指定 Sort key, 然后数据进行重新排序. 期间不影响使用.

在创建表时, 你还可以指定一个或者多个 column 作为 sort key. 这里有两种情况 COMPOUND sort key 和 INTERLEAVED sort key. 举例来说, 如果指定了 col_a, col_b 为 sort key. 我们用 va, vb 来表示一个 row 中两个 column 的值. COMPOUND sort key 会按照指定 sort key 的顺序, 先对 va 排序, va 一致的时候再根据 vb 进行排序. 而 INTERLEAVED sort key 对所有的 column 采用相同的权重. 从查询优化的角度来说, COMPOUND sort key 可以增加 JOIN, GROUP BY, ORDER BY 的性能, 或是用到 partition by / order by 的 window function. 而 INTERLEAVED sort key 适合特别大的 fact table 中有很多个 sort key column 彼此之间没什么相关性, 并往往单独用在不同的 query 中的情况.

我们用一个传感器数据的例子来决定