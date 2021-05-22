Simple Notification Service (SNS) Docs
==============================================================================

SNS 和 SQS 类似, 也是一个消息队列系统. 但是 SNS 主要是解决实时推送的问题, 不像 SQS 通常用于延迟处理类型的问题.

SNS 的模型是 Topic, Subscription. Subscription 必须要是一个可以进行 Consume 的单元, 可以是 AWS Lambda, SQS, Http Endpoint, Text Message, Email.

简单来说当一条 Message 被发布到 Topic, 所有的 Subscriber 会被同时触发.

SNS 允许创建 100,000 个 Topic, 以及 10 Million 个 Subscription Per Topic.


1. Topic 不多 Subscriber 非常多, 要求实时.
------------------------------------------------------------------------------

邮件订阅场景. 你的 App 有多个不同的 Topic, 比如 Daily / Weekly / Monthly Ads, 也有 Update Notification. 但是 Topic 的数量肯定不会特别多, 顶多几百个. 你的所有用户都可以 Subscribe 这些. 那么这事一个完美的 AWS SNS 使用场景.


2. Topic 非常多 Subscriber 不是很多, 不要求实时.
------------------------------------------------------------------------------

例如 GitHub Watch a Repo 的场景. 世界上的 Repo 非常多, 但是每个 Repo Watch 的人不是很多. 此时


3. Topic 非常多 Subscriber 非常多, 不要求实时.
------------------------------------------------------------------------------


4. Topic 非常多 Subscriber 非常多, 要求实时.
------------------------------------------------------------------------------

这是最难的一种情况了. 比如 微信 消息推送, 每一个点对点的聊天都是一个 Topic.