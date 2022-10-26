.. _kendra-basic:

Kendra Basic
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

本文把 AWS Kendra 这个服务最核心关键的一些信息归纳出来, 用尽量少的篇幅快速了解这个服务.


1. What is Kendra
------------------------------------------------------------------------------
Kendra 为企业提供了一个内部的搜索引擎, 相当于 Google. 它和 OpenSearch 的区别是, OpenSearch 主要是作为搜索的后端索引, 而 Kendra 主要是作为一个开箱即用的 Service. 使得用户专注于提供 Document, 以及构建 Search Application. 相比 OpenSearch, Kendra 无需花费很多的时间在维护 Cluster, 决定 Cluster 要多少个 Node 和磁盘, 如何定义索引, 无需 Web Developer 和 Backend 就可以创建一个 Application.


2. Kendra 中的重要概念
------------------------------------------------------------------------------
- Index: 相当于一个 OpenSearch 的 Index. 不过不需要定义 Schema 和 Mapping.
- Document: 一个个的文档. 和 OpenSearch 不同的是, Kendra Document 不是 JSON, 它的数据面模型是一个非结构的 Content, 以及一个结构的 Metadata Attributes Key Value. OpenSearch 可以对任何 JSON 的 Key Value 进行搜索, 而 Kendra 只能对 Content 进行搜索, 而用 Attributes 来 filter.
- Data Source: 为了方便把数据 ingest 到 Kendra 中, AWS 提供了很多的 Connector. Data Source 则是和 Connector 配合使用的. 一旦用了 Data Source, 就会更推荐用 Connector 来把数据导入到 Kendra, 而不推荐直接用 batch_put_document API. 例如 S3, Microsoft SharePoints, Google Drive, Confluence Page 等都可以作为 Data Source 并且有对应的 Connector, 只需要几下点击, 就会自动启动后台不可见的 EC2 来执行 Index 的工作.
- Query: Kendra 只支持非结构化的 Text Query. 返回的信息有 Title, text excerpt, 以及具体 hit 的地方的 location.

Kendra 的 Document 支持以下几种格式:
    - Structured Text
        - Frequently asked questions and answers
    - Unstructured Text, Kendra 能自动 OCR, 以及从 Word, PPT, PDF 中提取 Text.
        - HTML files
        - Microsoft PowerPoint presentations
        - Microsoft Word documents
        - Plain text documents
        - PDFs


3. Search Experience
------------------------------------------------------------------------------
是 Kendra 中用于构建搜索 App 的服务. 允许用户几下点击, 然后用拖曳的方式就可以创建一个像 Google Search 那样的 App. 其中包含一个搜索框, 以及多个用于 Filter 的 UI. 你可以将 attributes 作为 filter 的条件. 比如你有多个 data source, 你可以通过点击 Filter 上的 check box 来 narrow down 搜索结果.


4. Adjust Capacity
------------------------------------------------------------------------------
Kendra 的 Scale 的最小单位是 Capacity Unit. Kendra 有两种 Capacity Unit, 一个是 Storage Capacity Unit, 一个是 Query Capacity Unit.

- 1 个 SCU: 100k document, 30GB extracted text, around 1M update
- 1 个 QCU: 0.1 query / sec



Kendra 的权限管理
------------------------------------------------------------------------------

权限管理分 API / Index / Data Source 级别的管理, 和 Data Access Control 管理. 前者决定了谁能对 Kendra Index 做什么. 后者决定了谁能看到哪些数据. 这里我们把重点放在 Data Access Control.

Kendra 的 ACL 主要是使用 UserContext. UserContext 包含一个 User 和 Groups. User 是一个 String, Groups 是一个 List of String. Document 有 UserContext, 发起 Query 的时候也要带上 UserContext. 如果 Document 和 Principal 的 UserContext 匹配, 对于 User 是完全匹配, 而对于 Groups 是只要 Document 和 Principal 只要有一个 Group 相同即可.
