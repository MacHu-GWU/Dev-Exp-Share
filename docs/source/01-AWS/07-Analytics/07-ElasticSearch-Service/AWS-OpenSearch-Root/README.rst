
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
以下讨论的都是 OpenSearch (主要) 或 ElasticSearch (次要) Host 在 AWS 上时的使用场景.

AWS OpenSearch 的 API 权限管理有两种方法:

1. Fine Grained Access Control (FG): 简单来说就是 OpenSearch 版本的 Kibana Dashboard 有一套 UI, 可以在里面对 IAM User / Role, Domain, Index, Document, Field, Value-based (待验证) 进行超级细粒度的控制. 但是前提是你要能 login Dashboard. 而对于 Admin 要 login Dashboard 需要配置 AWS Cognito 具体就不展开讲了, 总之不那么容易. 然后 Admin 进去以后就可以在 Dashboard 中设置权限了, 并且可以创建 Dashboard 用户, 给他们账号密码用于登录. 用户不仅需要有账号密码, 用户的 IAM Role 也需要有权限才能对 Index 进行操作. FG 方法里可以手动指定一个 IAM Role 作为 Domain Admin, 这个 Role 能 CRUD 也能进 Domain, 且不需跟创建者的 IAM Role 不同.
2. IAM Role (IAM): 简单来说就是一个 Resource Policy 的 JSON, 和 IAM Policy 很像. 里面定义了 Principal (就是 IAM User / IAM Role) 以及 Resources (就是 Domain, Index 的 ARN), 以及 Action, 比如增删查改. 最小控制粒度是 Index, 不能实现 Field / Document (Column / Row) 级别的控制. 注意, 即使在 Resource Policy 中不给权限, 只要你有 Admin 的 IAM Policy 你一样可以有权限, 但如果被 Explicit Deny 了, 即使有 Admin 的 IAM Policy 也没用了.

无论使用以上哪种方法, 创建 Domain 的人都有最高权限.

官方明确说明了, FG 和 IAM 会有冲突, 会带来隐藏的行为不一致的问题, 官方不推荐同时用. 原因很好理解.


OpenSearch Dashboard
------------------------------------------------------------------------------

- `elasticsearch-py <https://elasticsearch-py.readthedocs.io/en/v7.15.2/>`_
