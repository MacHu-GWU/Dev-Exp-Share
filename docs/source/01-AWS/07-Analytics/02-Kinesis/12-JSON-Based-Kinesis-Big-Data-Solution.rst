JSON Based Kinesis Big Data Solution
==============================================================================

.. contents::
    :depth: 1
    :local:

无论 IT 公司是做什么产品, 大多都有这样的需求.

1. 各个 App, 以及用户行为每天会产生大量数据, 我们希望将这些数据收集起来, 集中保存, 作为 Datalake 保存起来.
2. 同时我们希望能将这些数据分门别类的进行处理, 将其变为比较容易查询的格式, 并且按照数据的类型分门别类地存储起来.
3. 在面对特定的数据分析问题的时候, 我们希望能很容易地创建一个数据仓库, 供分析师进行查询, 分析.
4. 我们希望 收集收据, 转换数据, 存储数据的过程很容易横向 (增大数据量) 和纵向扩展 (添加新的数据结构)

我在多个大数据项目中, 总结出一套基于 AWS 的架构, 能够满足以上需求.



About The Solution
------------------------------------------------------------------------------




Horizontally Scaling (Bigger Data Volume)
------------------------------------------------------------------------------

- 增大 Stream 的 Shard


Vertically Scaling (More Data Structure)
------------------------------------------------------------------------------

- 更新 Lambda Function Transform 的代码
- 创建新的 Delivery Stream, 并在你的 Lambda Function 中对数据进行过滤
- 更多的 Delivery Stream 意味着更多的 Consumer, 而这些 Consumer 默认共享一个 Shard 2MB/s 的吞吐量, 所以可以启用 Enhanced Fan out 提高吞吐量.


Code Example
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


1. ``kinesis.put_record`` data format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this solutin, we use json format for put_record input data. if your input data include data type other than int, float, string, you have to customize serialization method for special data type, and make the object JSON serializable.

Simple Json Example:

.. code-block:: python

    record_data = {
        "id": "2ed9c811-7481-4fcd-aabc-691904b67cf0",
        "time": "2019-10-12 02:37:22.178652",
        "type": "sign_up",
        "content": "wCrZfreslDvYgQoFChqVEkhHKQkvTdoN",
        "state": "raw"
    }

Complex Json Example:

.. code-block:: python

    record_data = {
        "binary": base64.b64encode(binary_object).decode("utf-8"),
        "datatime": {
            "$.date": (datetime_object - epoch).total_seconds()
        }
    }


2. ``kinesis.put_records`` API call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有两点需要注意:

1. Kinesis Stream 使用 Binary 作为数据编码的接口. 也就是说当用户想传递任何数据时, 用户需要自行负责将数据编码成二进制流. 当然在 transform 的时候, 用户也要自行负责将数据从二进制流中解码. 这也是为什么最后 ``"Data": binary_object`` 里面传递的是 bytes 的原因.
2. Kinesis Stream 是流处理工具. 而 Kinesis Stream 将多个 records dump 到 S3 上时, 采用的是二进制流直接拼接. 也就是说多条 record 汇总后的结果, 是直接连接在一起的, 中间既没有逗号分隔, 也没有 ``\t`` 和 ``\n`` 分隔, 非常不适合人类和机器读取. 由于在本方案中我们的数据是 JSON, 所以我们可以先将数据 dump 成字符串, 然后再最后加上 ``\n``, 最后编码为二进制流. 这样可以时多条 records dump 到 S3 上时, 文件比较容易读.

.. code-block:: python

    record_data = {
        "id": "2ed9c811-7481-4fcd-aabc-691904b67cf0",
        "time": "2019-10-12 02:37:22.178652",
        "type": "sign_up",
        "content": "wCrZfreslDvYgQoFChqVEkhHKQkvTdoN",
        "state": "raw"
    }

    record_data_list = [
        record_data1, # similar to record_data
        record_data2,
        ...
    ]

    records = [
        {
            "Data": (json.dumps(event_data) + "\n").encode("utf-8"),
            "PartitionKey": record_data["id"]
        }
        for record_data in record_data_list
    ]

    res = kinesis_client.put_records(
        Records=records,
        StreamName="test-stream",
    )


3. Firehose Delivery Stream Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Transform Source Records:

- IAM Role:

    在为 Firehose Delivery Stream 创建 IAM Role 的时候, 由于我们会需要 Kinesis Stream, Firehose, Lambda Invoke, Lambda Permission 等很多权限, 并不容易配置, 所以最好使用 Firehose Console 中的向导选定 Lambda Function 自动创建.

    如果你需要用 Cloudformation 来创建 Kinesis, 那么你最好手动创建一次, 并观察 Policy Document 的内容, 自行修改.


4. Firehose Delivery Stream with Data Transform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

注意我们在 output record 中同样加上了换行符.

.. code-block:: python

    import json
    import base64

    print("Loading function")


    def lambda_handler(event, context):
        output = []
        succeeded_record_cnt = 0

        for record in event["records"]:
            print(record["recordId"])
            record_data = json.loads(base64.b64decode(record["data"]).decode("utf-8"))
            record_data["state"] = "transformed"
            succeeded_record_cnt += 1
            output_record = {
                "recordId": record["recordId"],
                "result": "Ok",
                "data": base64.b64encode((json.dumps(record_data) + "\n").encode("utf-8"))
            }
            output.append(output_record)

        print("Processing completed.  Successful records {}.".format(succeeded_record_cnt))
        return {"records": output}



5. Convert Data Format Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你使用了上面的方法, 并确保 output_record 是没有 nested 的 JSON 格式, 那么后续的处理会简单很多.

这里使用的是 Record format conversion = Enable, Output format = Parquet. 因为 Parquet 是一种 **列存储格式**, 非常适合查询, 能够在查询时仅仅扫描部分列, 节约经费并提高效率. **而默认的 Firehose 会使用 snappy 将数据压缩**.

你完全可以禁用 Convert Data Format, 然后为你的 S3 put_object event 创建一个 Lambda Function, 并使用 Lambda 读取 JSON, 并转换成其他你想要的格式, 最后存到 S3 的其他地方. **这样的好处是能让你对数据格式转换做到完全控制, 也不用去查文档, 猜 AWS 内部是怎么做的. 但是坏处是需要额外的算力和 Lambda 的费用**. 在本方案中, 由于我们的 JSON 数据格式很简单, 所以我们可以使用自带的 Convert Data Format 功能, 而无需编写 ETL Lambda Function. 默认情况下 Kinesis Stream 会讲 Buffer 中的数据统一打包放入一个文件, 并根据时间按照, 年, 月, 日, 小时, 分钟 的格式按文件夹存放.

**要注意的是, Kinesis默认的时间可能跟 record 生成的时间并不完全一致, 因为 record 从生成到被 lambda 处理完有一个过程**, 如果你想直接对 S3 上的数据按照时间进行查询, 而不是通过将数据存到 Redshift 上, 你很可能需要为你的 S3 Key 进行一些 Partition 的处理, 以提高 Athena 的性能. 可是由于自动生成的 S3 Key 中的时间, 并不精确代表 record 的时间, 如果需要按时间查询, 并且对性能敏感, 那么我们最好还是直接将 transform 好的 JSON dump 到 S3, 然后用 put object 触发 lambda, 手动进行 format convert, 然后按时间将 record 汇总, 并生成相应的 S3 Key.

为了能使用自带的 Convert Data Format 功能, 你需要配置 AWS Glue Catalog Database 和 Table. 在填写 Table Schema 的时候, 只要你的 JSON 是 Flat Format, 那么你只需要填写 Column Name 和 Type 即可. 而你可以在 Athena 中直接对 Parquet 数据进行查询.
