Avoid Double Consume
==============================================================================
当 consumer **处理一条信息的时间, 超过了 visibility timeout 的时间时, 会导致这条信息被其他的 consumer 收取到, 导致重复处理**.

为了避免这种情况, 请一定要在 consumer 的处理逻辑中设置 ``visibility timeout`` 确保整个处理逻辑如果在一定时间内没有完成, 则自动结束.

如果你的 Consumer 是用 Python 语言写成的, 建议使用 `timeout-decorator <https://pypi.org/project/timeout-decorator/>`_ 这个库.

假设我们一条 Message 的平均处理时间是 30 秒, 且一定不会超过 60 秒, 但是 Consumer 客户端可能会因为各种奇怪的原因卡住导致超时, 使得代码中的 timeout 不起作用, 比如数据库无响应. 在这种情况下, 我们应该怎么做?

1. 将 Visibility Timeout 设置为 60 秒
2. 使用 AWS Lambda 作为 Consumer
3. 在 Lambda 代码中, 在处理完毕后立刻使用 delete message API 删除该条消息
4. 并且设置 Timeout 59 秒, 因为删除该条消息有可能需要 1 秒时间
5. timeout-decorator 是代码级别的超时限制, 而 Lambda Timeout 是系统级的超时限制, 更加可靠和稳定
