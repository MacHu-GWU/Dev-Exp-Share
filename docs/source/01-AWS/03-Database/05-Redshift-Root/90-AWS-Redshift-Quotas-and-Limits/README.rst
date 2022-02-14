.. _aws-redshift-quotas-and-limits:

AWS Redshift Quotas and Limits
==============================================================================
Keywords: limit, limits, quota, quotas

注意, 官方的文档随着时间的推移会更新的. 请以官方文档为准.

Ref:

- https://docs.aws.amazon.com/redshift/latest/mgmt/amazon-redshift-limits.html


AWS Redshift Quotas and Limits
------------------------------------------------------------------------------

- 一个 cluster 最多有 128 个 DC2 node
- 一个 cluster 最多有 128 个 DS2 node
- 一个 account 一个 region 所有的 cluster 加起来最多有 200 个 node
- 一个 cluster 中的一个 database 最多有 9,900 个 schema
- COPY command load 的数据一个 row 不能超过 4MB, 所以不要存 large binary, 请用 S3 存 large binary, 然后把 S3 URI 存在 redshift 中.
- 一个 ``large`` node type, single node cluster 最多有 9,900 个 Table. 包括了 table / temp table / view / datashare table.
- 一个 ``xlplus`` node type, multiple node cluster 最多有 20,000 个 Table.
- 后面的 node type 越大, table 的上限越多.
