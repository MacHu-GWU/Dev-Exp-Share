.. _kinesis-firehose-delivery-stream-transformation:

Kinesis Firehose Delivery Stream Transformation
==============================================================================
Keywords: AWS Kinesis, Firehose, Delivery Stream, Lambda, Transform Transformation.

我们来看一个典型的实时数据流 Transformation 案例:

1. 数据以 Batch 的形式, 用 put_records API 发送给 Kinesis Data Stream
2. Kinesis Firehose Delivery Stream 订阅了 Kinesis Data Stream, 收到了数据
3. Firehose 触发了用于做 Transformation 的 AWS Lambda, Lambda 接受到了数据
4. Lambda 对数据进行了 Transformation, 并整理成了 Firehose Programming Model 认识的格式
5. Firehose 将处理好的数据 dump 到 S3 或是其他的 Destination

这里我们重点研究下 #1, #3, #4 三步, 这三步你需要在 SDK 中准备好数据结构和格式, 格式不对前后是接不起来的.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. Raw Data
------------------------------------------------------------------------------
原始数据用 Python Dictionary 的形式保存. 一条数据就是一个 Dict.

.. code-block:: python

    {"id": "1", "value": random.randint(1, 100)}
    {"id": "2", "value": random.randint(1, 100)}
    {"id": "3", "value": random.randint(1, 100)}

用 ``put_records`` 把数据发送给 Data Stream:

.. literalinclude:: ./producer.py
   :language: python


3, 4. Transformation Lambda Function
------------------------------------------------------------------------------

.. literalinclude:: ./transformation.py
   :language: python


5. Data in Destination
------------------------------------------------------------------------------
最终 Delivery Stream 会把每个 record 恢复成 binary, 然后连续拼接在一起, 最终形成一个大的 binary 文件.

由于我们这里的数据其实是 JSON encoded string, 所以最后的文件可以被解读为 pure text json file.

.. code-block:: javascript

    {"id": "1", "value": 3100}{"id": "2", "value": 2800}{"id": "3", "value": 4200}


Summary
------------------------------------------------------------------------------
**Serialization Protocol**

Kinesis 用的是 binary protocol. 虽然我们可以用 json string protocol, 但是在转换过程中会有效率问题, 例如 binary 数据你要用 json serialize 就得先转化成 base64 encode. 然后 dump 之后变成了 binary, 又要经过一次 base64 encode. 这样会造成较大的资源浪费. 如果能用基于 binary 的 serialization protocol, 例如 pickle, google 的 protocol buffer / flatbuffer 等格式, 效率会更高, 不过编程起来会麻烦一点.
