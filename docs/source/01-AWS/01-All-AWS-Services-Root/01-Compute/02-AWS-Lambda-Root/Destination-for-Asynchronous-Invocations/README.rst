Destination for Asynchronous Invocations
==============================================================================
Keywords: AWS Lambda Function, Asynchronous Invocation, Error Handling, SNS.

以前对于 Lambda 的异常处理, 通常有两种方法:

1. 在代码里用 try except 这一类的语法捕获异常, 然后自己将其发送到 SNS 或者 SQS 等服务. 这样做的问题在于如果程序是 timeout 或者 OOM 之类的异常, 代码里的 try except 根本无法被运行到, 也就无法发送到 SNS 或者 SQS 了.
2. 设置 Dead letter queue, 让 lambda 将 async invoke 时出现的异常发送到一个叫 DLQ 的特殊的 SQS 中, 然后你自己去 poll 去处理.

这里简单说一下, 之所以 AWS 不支持 sync 的自动异常处理是因为, 如果你用 sync, 那么你就有一个客户端保持跟 lambda 的连接, 你这个客户端就应该负责处理, 无论是异常还是超时都很容易做到, 没有必要用 AWS.

但如果你想要将失败的 invoke 发给其他的系统, 例如 SNS topic, 或是另一个 lambda, 或是 Event bridge, 那么你就要自己写代码去 poll 这个 DLQ 然后进行转发.

从 2019 年 11 月起, AWS 支持了以上 3 种额外的 destination, 可以在 success 或是 failure 的时候自动转发, 而无需写代码了. 这里我觉得最通用的是 SNS, 因为 SNS 可以转发到很多地方, 而且订阅模型非常灵活. 本文就以 SNS 为例, 列出了 failed 和 succeeded 时, 如果我用一个 Lambda 来 subscribe 这个 SNS, 它的 event 和 message 是什么样子的.


.. literalinclude:: ./sns-event-failed.json
   :language: json
   :linenos:

.. literalinclude:: ./sns-event-succeeded.json
   :language: json
   :linenos:

.. literalinclude:: ./sns-message-failed.json
   :language: json
   :linenos:

.. literalinclude:: ./sns-message-succeeded.json
   :language: json
   :linenos:

- `AWS Lambda Supports Destinations for Asynchronous Invocations <https://aws.amazon.com/about-aws/whats-new/2019/11/aws-lambda-supports-destinations-for-asynchronous-invocations/>`_
