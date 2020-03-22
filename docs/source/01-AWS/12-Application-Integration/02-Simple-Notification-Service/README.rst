Simple Notification Service (SNS) Docs
==============================================================================

SNS 和 SQS 类似, 也是一个消息队列系统. 但是 SNS 主要是解决实时推送的问题, 不像 SQS 通常用于延迟处理类型的问题.

SNS 的模型是 Topic, Subscription. Subscription 必须要是一个可以进行 Consume 的单元, 可以是 AWS Lambda, SQS, Http Endpoint, Text Message, Email.

简单来说当一条 Message 被发布到 Topic, 所有的 Subscriber 会被同时触发.

SNS 允许创建 100,000 个 Topic, 以及 10 Million 个 Subscription Per Topic.
