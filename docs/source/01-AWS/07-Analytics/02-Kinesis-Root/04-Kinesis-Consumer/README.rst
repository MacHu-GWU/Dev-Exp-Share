Kinesis Consumer
==============================================================================

Keywords:

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


.. _kinesis-consumer-low-latency-processing:

Low Latency Processing
------------------------------------------------------------------------------
Record 一旦被写入到 Kinesis, 就可以立刻被读取到并消费了. Kinesis 的消费模型是 ``拉取`` 而不是 ``推送``. 所以消费者需要主动去 ``拉取`` 数据. 由于每个 Shard 有 5 TPS (每秒 5 次 Get API 调用) 的限制.


消费速度跟不上 Pull 的速度


