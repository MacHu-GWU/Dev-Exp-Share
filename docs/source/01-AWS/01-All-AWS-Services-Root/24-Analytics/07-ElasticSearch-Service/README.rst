Amazon ElasticSearch (AES)
==============================================================================

AES 是亚马逊推出的 ElasticSearch 服务. 开发者无需部署 ES Cluster,



主要用于查询 **非结构化**, **Schema 不一致** 的日志数据.


Amazon ElasticSearch FAQ
------------------------------------------------------------------------------

Reference:

- https://aws.amazon.com/elasticsearch-service/faqs/

- Q: AES 扩容时需要停机么?
- A: 不需要.

- Q: AES 的索引数据保存在哪里?
- A: 保存在 EC2 Instance Storage 或是 EBS 上, 显然保存在 EBS 上更好.

- Q: AES 的
- A:

- Q:
- A:

- Q:
- A:

- Q:
- A:


ElasticSearch API
------------------------------------------------------------------------------

links:

- `ES Rest API <https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html>`_

ES Cluster 在启动以后, 会有一个 REST API 服务器用于跟外部系统会话. 你可以用 HTTP 请求与之通信.

ES 的 API 和 MongoDB 很像. 主要是用 JSON 的 DSL (特殊设计过 Schema 的 JSON 代表不同的语义).

ES 的 API 有很多类型, 例如用于管理集群系统的 Cluster API, 管理文档的 Document API 等等. 不同类别的 API 有着不同的 URL Path, 通常这些 Path 以下划线开头, 用于区分系统 Path 和数据 Path. 例如 Cluster API 是 ``/_nodes`` 开始的.

ES 还有很多 Features, 比如类 SQL 的 EQL (ElasticSearch Query Language); 提供时间序列, Append Only 的 Data Stream 功能.



ElasticSearch in Python
------------------------------------------------------------------------------

在 Python 内使用 ES 主要会用到 2 个包.

- `elasticsearch <https://pypi.org/project/elasticsearch/>`_: 底层 API, 主要使用 JSON 作为 Protocol.
- `elasticsearch_dsl <https://pypi.org/project/elasticsearch-dsl/>`_: 提供了一层 ORM, 主要使用 Object 作为 API.


ElasticSearch vs AWS Open Search
------------------------------------------------------------------------------

很多开源数据库公司对商业云公司非常不满, 认为这些商业云公司将开源方案拿走, 并做成了付费商品卖钱, 特别是 AWS 的产品命名还是 AWS ElasticSearch, 让人很容易误会 ElasticSearch 是 AWS 做的. 所以从 2021 年 1 月 ES 背后的公司将其开原许可协议修改了, 不再允许云厂商商用. 所以 AWS 就从 7.05 版本 Folk 了一个出来, 自己维护一个 OpenSearch 的项目, 并且维护着这个生态, 继续在 AWS 上提供一个本质是 ElasticSearch 的服务, 但名字却是 OpenSearch 的服务. 相信再过一段时间, OpenSearch 和 ElasticSearch 的 API 会越来越不兼容.


