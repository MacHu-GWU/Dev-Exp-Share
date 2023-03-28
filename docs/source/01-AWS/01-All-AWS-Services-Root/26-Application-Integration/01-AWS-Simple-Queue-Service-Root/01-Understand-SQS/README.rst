Understand SQS
==============================================================================
Keywords: AWS SQS, Simple Queue Service, Message Queue

SQS 是消息队列系统. 主要用于消息可靠抵达和可靠处理. 常用于非即时性的, 可稍后处理但是必须处理的工作. 实现方式是长轮询, 也就是一段时间收一批信息, 并处理一批.

消息队列可以说是最重要的几个软件中间件之一. 常用于平滑请求, 连接多个系统.

.. contents::
    :depth: 1
    :local:

Concept
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


Queue Attributes - Default Visibility Timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The length of time (in seconds) that a message received from a queue will be invisible to other receiving components.

如果信息被 receiver 所接收, 那么在一定时间内其他 receiver 无法看到这条信息. 如果所接收的 receiver 没有删除他, 那么在一段时间后这条消息会再次被接收.


Queue Attributes - Message Retention Period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The amount of time that Amazon SQS will retain a message if it does not get deleted.

信息在 SQS 中最多被保留多长时间? 0 - 4 days


Queue Attributes - Delivery Delay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The amount of time to delay the first delivery of all messages added to this queue.

信息到达 SQS 后在多长时间内是不可见的.


Queue Attributes - Receive Message Wait Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The maximum amount of time that a long polling receive call will wait for a message to become available before returning an empty response. 0 - 20 sec.

每次长轮询时在返回空结果之前等待多久.


Dead Letter Queue Settings - Use Redrive Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Send messages into a dead letter queue after exceeding the Maximum Receives.

一条消息被接受了 N 次之后, 仍然没有被删除, 则转发到 Dead Letter Queue 中.


Dead Letter Queue Settings - Maximum Receives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The maximum number of times a message can be received before it is sent to the Dead Letter Queue.


Pricing
------------------------------------------------------------------------------

Reference: https://aws.amazon.com/sqs/pricing/

Price per 1 Million Requests:

- Standard Queue: $0.40
- FIFO Queue: $0.50

Data Transfer OUT: 1GB - 9.999 TB / Month, $0.09 per GB


Limit
------------------------------------------------------------------------------

Reference: https://aws.amazon.com/sqs/faqs/


Only-Once Delivery
------------------------------------------------------------------------------

Standard Queue 不能保证 only-once delivery, 但是 FIFO Queue 可以保证. 所以对于数据库应用, 必须使用 FIFO Queue.
