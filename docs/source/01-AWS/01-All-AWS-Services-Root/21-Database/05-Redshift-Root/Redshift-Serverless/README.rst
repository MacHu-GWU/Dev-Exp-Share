.. _redshift-serverless:

Redshift Serverless
==============================================================================


Summary
------------------------------------------------------------------------------

NameSpaces Workgroups
------------------------------------------------------------------------------
因为 Redshift Serverlss 是无服务器的, 也就不存在具体的服务器的管理了. 而只有 Schema / Table / User 等. 你怎么能对其进行管理呢?

这就引入了 Namespaces 和 Workgroups 的概念. Namespaces 就是对数据相关的资源进行管理的. 而 Workgroup 是负责对计算资源进行管理的, 例如 RPU, VPC 等.

Namespace is a collection of database objects and users. The storage-related namespace groups together schemas, tables, users, or AWS Key Management Service keys for encrypting data. Storage properties include the database name and password of the admin user, permissions, and encryption and security. Other resources that are grouped under namespaces include datashares, recovery points, and usage limits. You can configure these storage properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs for the specific resource.

Workgroup is a collection of compute resources. The compute-related workgroup groups together compute resources like RPUs, VPC subnet groups, and security groups. Properties for the workgroup include network and security settings. Other resources that are grouped under workgroups include access and usage limits. You can configure these compute properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs.

You can create one or more namespaces and workgroups. A namespace can exist without any workgroup associated with it. Each namespace can have only one workgroup associated with it. Conversely, each workgroup can be associated with only one namespace.

Ref:

- Overview of Amazon Redshift Serverless workgroups and namespaces: https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-workgroup-namespace.html
- `Amazon Redshift conceptual overview <https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html>`_: 讲解了 Amazon Redshift 的核心概念
Redshift Serverless vs Redshift
------------------------------------------------------------------------------


Redshift Serverless Pricing
------------------------------------------------------------------------------
简单来说, 跟 Cluster 模式的 Redshift 放在那里就收钱相比, Redshift Serverless 是只按你运行 Query (包括 Insert / Update) 的时长收费, 精确到秒. 也就是说, 你的 Redshift Serverless 可以一直存在, 但是你不运行任何 Query 的时候, 你是不用付钱的. 但是你的存在 Redshift 上的数据无论你有没有运行 Query, 都是要收费的. 但是作为数据分析的仓库的成本而言, 运算成本一般远远高于存储.

- Redshift Processing Units: $0.36 per RPU hour
- Amazon Redshift managed storage pricing: $0.024 per GB / Month
- 注意, Redshift 最小的 RPU 是 8, 512, 一个 RPU 大约是 16G 内存, 你 scale 的时候也会以 8 为单位的增加减少. 并且 8, 16, 24 RPU 能 handle 大约 128TB 的数据, 换算过来大约是 1 个 RPU = 5.33 TB.

案例 1:

你用 Redshift serverless 进行实验性质的开发, 假设你用最小的 8 RPU, 每天实际运行 Query 的时间大约 1 小时, 你的数据集是 1GB. 那么你的开销是:

- 计算成本: 0.36 * 8 = $2.88 / 天 = $86.4 / 月
- 存储成本: 0.024 * 1 = $0.024 / 月

案例 2:

你用 Redshift serverless 每天从 7AM - 7PM (包括 7PM), 每小时运行一个耗时 10 分钟的 Query 来统计每天的指标, 也就是每天运行 13 次. 你的数据量大约是 100 TB, 需要 24 个 RPU. 那么你每月的开销是:

- 计算成本: 0.36 (RPU / Hour 单价) * 24 (24 个 RPU) * 30 (一个月 30 天) * 13 (每天运行 13 次) * 600 (每次 600秒) / 3600 (换算为小时) = 0.36 * 24 * 30 * 13 * 600 / 3600 = $561.6 / 月. 存 100 TB 的数据, 这还是挺划算的.

Reference:

- `Amazon Redshift pricing <https://aws.amazon.com/redshift/pricing/>`_
- `Billing for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-billin.html>`_


Reference
------------------------------------------------------------------------------
- Amazon Redshift Serverless: https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html
- Amazon Redshift Serverless is now generally available (2022-07): https://aws.amazon.com/about-aws/whats-new/2022/07/amazon-redshift-serverless-generally-available/


- Amazon Redshift Serverless Technical Overview Deck: https://aws.highspot.com/items/62a8d0a5282f1e220bf892bb?lfrm=srp.4
- Amazon Redshift Serverless - First Call Deck: https://aws.highspot.com/items/62ccc8244585166b17aa16a1?lfrm=srp.2