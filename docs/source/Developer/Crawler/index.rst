requests 方案

Scrapy 方案

Cloud 方案


AWS方案
------------------------------------------------------------------------------

- 抓取: Lambda
- 存储: DynamoDB, RDS, DocumentDB, S3
- 调度: FIFO SQS

我们以抓取 CVS 网站为例, 从一个Store Locator的页面出发, 包含所有 State 页面的链接, 再包含所有 City, Zipcode, Store 的 URL.

- Architect: Lambda + RDS + SQS
- ORM: Homepage, State, City, Zipcode, Store

第一步:

1. 在数据库中创建一条 Homepage 的记录.
2. 从数据库中提取 Homepage 的信息, 包装在 Message 中发送给 SQS.
3. SQS 触发 Lambda, 完成抓取后, 更新数据库中 Homepage 的信息, 并创建了多个 State 的记录, 只包含 Url 不包含 HTML. 数据库写入 Homepage 以及 State 成功后, 创建多条包含 State 信息的 Message
将 首页的 URL 包含在 Message 中发送给 SQS.
4. SQS 中的 State 又会触发 Lambda, 创建多个 City, 如此循环下去.

SQS 中的信息如何告诉 Lambda 该条信息是 ORM 中的哪个类?

如何限定抓取间隔,

串行抓取 vs 并行抓取:

- 串行抓取: 方便控制顺序, 抓取间隔时间.
- 并行抓取: 分布式抓取, 效率极高, 但是执行抓取的系统, 例如 Lambda 要小心设置网络, 避免被 Ban. 调度实现起来较难.

- SQS Event 触发 Lambda 的方式是基于 Poll based (轮询), 所以 Invoke 的方式是 Sync, 也就是上一条 Invoke 处理完之前, 无法 Invoke 下一个. 所以如果你 Push 了 10条 Message 到 SQS, 同一时间只有一个 Lambda 在运行
- S3 Event 触发 Lambda 的方式是 Async, 也就是说 如果你 Push 了 10 条 Message 到 SQS, 同一时间会有 10 个 Lambda 在运行.

遍历所有 URL 如何实现?

由于我们的爬虫逻辑中 对 State (Parent) 进行抓取完之后, 就会创建


Lambda 完成抓取后吗更新数据中


需要登录后抓取的应用场景
------------------------------------------------------------------------------
