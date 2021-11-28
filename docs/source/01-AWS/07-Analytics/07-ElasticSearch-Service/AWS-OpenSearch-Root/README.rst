
.. _aws-opensearch-root:

AWS OpenSearch
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Links:

- `AWS OpenSearch Document <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html>`_



AWS OpenSearch vs ElasticSearch
------------------------------------------------------------------------------

很多开源数据库公司对商业云公司非常不满, 认为这些商业云公司将开源方案拿走, 并做成了付费商品卖钱, 特别是 AWS 的产品命名还是 AWS ElasticSearch, 让人很容易误会 ElasticSearch 是 AWS 做的. 所以从 2021 年 1 月 ES 背后的公司将其开原许可协议修改了, 不再允许云厂商商用. 所以 AWS 就从 7.05 版本 Folk 了一个出来, 自己维护一个 OpenSearch 的项目, 并且维护着这个生态, 继续在 AWS 上提供一个本质是 ElasticSearch 的服务, 但名字却是 OpenSearch 的服务. 相信再过一段时间, OpenSearch 和 ElasticSearch 的 API 会越来越不兼容.


OpenSearch Authentication
------------------------------------------------------------------------------



OpenSearch Dashboard
------------------------------------------------------------------------------

- `elasticsearch-py <https://elasticsearch-py.readthedocs.io/en/v7.15.2/>`_
