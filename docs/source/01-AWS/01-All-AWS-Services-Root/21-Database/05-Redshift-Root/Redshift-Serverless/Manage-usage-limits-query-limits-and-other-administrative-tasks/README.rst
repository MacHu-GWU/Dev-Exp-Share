Manage usage limits query limits and other administrative tasks
==============================================================================


Overview
------------------------------------------------------------------------------
作为一款商用的数据仓库产品, redshift 增加了很多对服务器资源的使用进行细致化管理的功能. 并且把很多监控面板都集成到了 console 中.


Manage Redshift processing units (RPU) Limit for Workgroup
------------------------------------------------------------------------------
你可以为每个 workgroup 设置最多 4 个 limit rule. 所谓 limit rule 就是说在多长时间内, 最多用多少 RPU / Hour, 如果超了, 要采取什么 action.

Frequency (多长时间内) 的选项有:

- Daily
- Weekly
- Monthly

ActionL

- Alert: 发 notification, 你自己选择 SNS topic
- Log to System Table: 记录到 Redshift system table 中
- Turn off User Query: 杀掉新的 query, 这也会发送 notification 到 SNS topic

例如你可以说你的 workgroup 有 8 个 RPU, 最大能 scale 到 32 个. 每天最多用 32 个 RPU. 也就是以 8 个 RPU 的状态跑 4 小时.


Manager Redshift Query Limit for Workgroup
------------------------------------------------------------------------------
你还可以为每个 workgroup 中的 query 配置 Limit. 允许设置 limit 的 metrics 如下:

- Query execution time: Elapsed execution time for a query, in seconds. Execution time doesn't include time spent waiting in a queue. If a query exceeds the set execution time, Amazon Redshift Serverless stops the query. Valid values are 0-86399
- Query queue time: Time spent waiting in a queue, in seconds. Valid values are 0-86399
- Query CPU time: CPU time used by the query, in seconds. CPU time is distinct from Query execution time. Valid values are 0-999999
- Query CPU usage: Percent of CPU capacity used by the query. Valid values are 0-6399 (63.99%)
- Scan row count: The number of rows in a scan step. The row count is the total number of rows emitted before filtering rows marked for deletion (ghost rows) and before applying user-defined query filters. Valid values are 0-999,999,999,999,999
- Return rows count: The number of rows returned by the query. Valid values are 0-999999999999999
- Rows joined: The number of rows processed in a join step. Valid values are 0-999,999,999,999,999
- Nested loop join row count: The number or rows in a nested loop join. Valid values are 0-999999999999999
- Blocks read: Number of 1 MB data blocks read by the query. Valid values are 0-1048575
- Memory to disk: Temporary disk space used to write intermediate results, in 1 MB blocks. Valid values are 0-319815679


Filtering queries
------------------------------------------------------------------------------
你可以在 AWS Redshift Console 界面的 Query and database monitoring 中查看你执行过的 query 的详细信息, 包括 SQL statement, 耗时, query plan, related metrics, 非常详细.


Checking Amazon Redshift Serverless summary data using the dashboard
------------------------------------------------------------------------------
你可以在 AWS Redshift Console 界面的 Redshift Serverless Dashboard 上看到很多监控信息, 包括:

- Queries metrics
- RPU capacity used
- Alarms


Reference
------------------------------------------------------------------------------
- `Managing usage limits, query limits, and other administrative tasks <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-console-configuration.html>`_