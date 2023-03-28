.. _aws-redshift-best-practice-choose-the-best-sort-key:

Choose the best sort key
==============================================================================
Keywords: AWS Redshift, Best practice

首先要知道的是 Redshift 是基于列式存储的. Redshift 在将数据存储到磁盘上时, 会基于 Sort Key 在磁盘上顺序写入. 这相当于时候每个 Table 都有个默认的 sorted index column. 同时 Redshift 由于使用了列式存储, RDBMS 中的那些 index 根本就没有必要, 所以在 Redshift 中没有 Index. 查询性能的优化主要取决于 Sort Key, Distribution Key.

官方文档推荐用以下几个原则来决定哪个 Column 成为 Sort Key

- 如果有 datetime column, 并且最近的数据查询的更为频繁, 则果断选择时间列为 sort key
- 如果你的 query 会有很多 range query, 选择在 query 中被使用最多的列作为 sort key
- 如果你频繁的要 join table, 那么把 join ON column 的列同时作为 sort key 和 distribution key
