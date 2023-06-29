Amazon MWAA - Manage Environment
==============================================================================
本文主要讲如何管理 MWAA Environment 本身. 所谓管理 Environment 就等同于管理 Airflow Cluster, 只不过大部分复杂的细节都是 AWS 托管的, 我们只需要关注一些重要的配置即可.

这里我们简单回顾一下 MWAA 的架构. 任何一个 MWAA Environment 都包含以下组件:

- scheduler: 用于中心化的调度, 当然 AWS 是做了冗余和高可用的, 可以有不止一个 scheduler, 但是通常 scheduler 的数量不会需要特别多, 它主要利用的是高性能 event loop 异步执行.
- web server: 用于提供 Airflow UI, 作为 web server 的机器一般只有一台 (当然是有备用的作为高可用). 因为 web server 是给人类用来查看 DAG 运行状态的, 一般不会有太多的并发请求.
- worker: 默认包括 1 个常驻 worker. 当然根据你并发执行 DAG 的多少, 可以自动的 scale 增加和减少 worker.

你可能会注意到这里没有提及 Database, 因为 database 其实是跟开发关系不大的部分, 主要为了持久化 metadata, 而且几乎不存在人工直连 database 的情况. 这部分 AWS 是全权接管的, 开发者无法触及.


Configuring the Amazon MWAA environment class
------------------------------------------------------------------------------
Environment class 就是指这个 environment 的总体大小. 简单来说不同的大小对应 DAG 的上限:

- mw1.small: 50
- mw1.medium: 250
- mw1.large: 1000

而从 task 并行的数量来看:

- mw1.small: 5 个并行 task
- mw1.medium: 10
- mw1.large: 20

这里注意的是, Airflow 本身是个调度系统, 它的主要工作不是执行真正的业务逻辑和数据处理. 这些工作都应该放在专用的工作负载上进行, 例如 AWS Lambda, AWS Batch, AWS Glue 等. 而 Airflow 中的 Task 主要是处理输入输出参数, 调用 API, 监控状态. 每个 Task 本身的运行时间应该是比较短的 (1-3 秒) 之间. 所以这个并行数量其实是比较够用的.


Configuring Amazon MWAA automatic scaling
------------------------------------------------------------------------------


Using Apache Airflow configuration options on Amazon MWAA
------------------------------------------------------------------------------


Upgrading the Apache Airflow version
------------------------------------------------------------------------------


Using a startup script with Amazon MWAA
------------------------------------------------------------------------------

