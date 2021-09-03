ElasticSearch
==============================================================================

.. contents::
    :depth: 1
    :local:

基础篇
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


什么是 ElasticSearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ElasticSearch 是一个 开源的, 用于搜索的类数据库软件, 底层使用 Lucene 实现. 而 Lucene 是搜索引擎功能底层库, 使用 Java 实现. ElasticSearch 可以被部署到任何机器或集群上. AWS ElasticSearch Service 是一个托管的服务器部署服务, 大大简化了部署, 运维的工作量.



ElasticSearch 中的重要概念
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Document: 一条记录, 相当于 MongoDB 中的 Document, 关系数据库中的 Row
- Document Metadata: 关于 Document 的元数据, 比如 Index 名字, ID, Type 等
- Document Body: 文档的本体数据
- Index: 一类结构相同的文档集合, 相当于 MongoDB 中的 Collection, 关系数据库中的 Table
- Node: 一个运行着 ES 服务的实体机器
- Shard: 一个分片, 一个 Node 上可以运行多个分片
- Replica: 冗余数据, 通常指位于不同 Node 上的多个分片
- Field: Document 中的一个数据点, 或是 JSON 中的一个 Key
- Mapping: 定义了一个 Field 如何被 Index 的一个逻辑关系. 一个 Field 可以有多个 Mapping.


ElasticSearch 和 MongoDB 的比较
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

很多熟悉 MongoDB 的开发者一开始会有疑问, ES 同样是使用 JSON, 也可以对每个 Field 进行搜索, 那 ES 和 MongoDB 有什么不同呢?

首先 ES 的核心是搜索, 而不是数据库. ES 可以针对每个 Field 被搜索的方式进行优化, 这个优化主要服务于搜索而不是服务于存储. 比如对 Text 的分词索引等功能, 做的要远远优于 MongoDB 中的 Text Index.

ES 可以将多个 Field 的搜索方式汇总, 集合到一起, 从而无需指定被搜索的 Field 就可以搜索. 这点 MongoDB 以及其他数据库做不到, 它们通常都需要分别指定各个 Field 的搜索方式, 然后用逻辑 AND OR 来进行过滤.

ES 可以对一个 Field 设定多种不同的搜索方式, 这点 MongoDB 以及其他数据库做不到.


几个常见的坑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

对于已经设定了 Mapping 的 Field, 大部分情况下是无法修改已有的 Mapping 的, 这事因为每当你建立一个 Mapping, ES 就要根据被索引的方式维护一个 Index, 你修改了 Mapping, 就意味着要重新建立新的 Index, 而你无法直接将已有的 Index 变成新 Index. 正确的做法是对同一个 Field 创建一个新的 Mapping, 从而创建一个新 Index, 然后再删除旧的 Index 即可. 只有少量 DataType 支持动态修改 Mapping


查询的语法入门
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html
