Kinesis Boto3 API
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Put Records
------------------------------------------------------------------------------
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.put_records

根据 API 文档. ``put_records`` 的 parameter 和 response 长这样:

.. code-block:: python

    response = client.put_records(
        Records=[
            {
                'Data': b'bytes',
                'ExplicitHashKey': 'string',
                'PartitionKey': 'string'
            },
        ],
        StreamName='string'
    )

    response = {
        'FailedRecordCount': 123,
        'Records': [
            {
                'SequenceNumber': 'string',
                'ShardId': 'string',
                'ErrorCode': 'string',
                'ErrorMessage': 'string'
            },
        ],
        'EncryptionType': 'NONE'|'KMS'
    }


    import base64

    print('Loading function')


    def lambda_handler(event, context):
        output = []

        for record in event['records']:
            print(record['recordId'])
            payload = base64.b64decode(record['data']).decode('utf-8')

            # Do custom processing on the payload here

            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(payload.encode('utf-8'))
            }
            output.append(output_record)

        print('Successfully processed {} records.'.format(len(event['records'])))

        return {'records': output}



测试如果将两个 Firehose Delivery Stream 连接到同一个 Kinesis Stream 上, 是否两个
Delivery Stream 都会受到数据.

Delivery Stream 1:

- name: ``test-delivery1``
- s3 bucket: ``eq-sanhe-for-everything``
- prefix:
    - success: ``data/kinesis-test/raw/good/``
    - failed: ``data/kinesis-test/raw/bad/``

Delivery Stream 2 - Transform Data:

- name: ``test-delivery2``
- s3 bucket: ``eq-sanhe-for-everything``
- prefix:
    - success: ``data/kinesis-test/processed/good/``
    - failed: ``data/kinesis-test/processed/bad/``

Lambda Function for Delivery Stream 2

- function name: ``test-delivery2``



Kinesis Firehose Delivery Stream Transform Lambda Function Programming Model
------------------------------------------------------------------------------

- Reference: https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html

1. 使用 Put Records 发送到 Kinesis Stream 的数据长这样:

.. code-block:: python

    {
        "Data": b"bytes",
        "PartitionKey": "string",
        "ExplicitHashKey": "string",
    },

- Data: 将你的数据序列化成二进制数据, 例如 dict, list 可以 json.dumps 后用 utf-8 编码, str 可以直接用 utf-8 编码, 二进制数据就可以直接编码了.
- PartitionKey: 用于决定在哪个 shard 上的 key.
- ExplicitHashKey: shard 的 id, 直接指定发送到哪个 shard 上, 通常无需指定.

2. 简单来说负责输入的 Transformer Lambda Function 的输入长这样:

.. code-block:: python

    {
        "invocationId": "invocationIdExample",
        "deliveryStreamArn": "arn:aws:kinesis:EXAMPLE",
        "region": "us-east-1",
        "records": [
            {
                "recordId": "49546986683135544286507457936321625675700192471156785154",
                "approximateArrivalTimestamp": 1495072949453,
                "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4="
            }
        ]
    }

- records.data: 将你 put record 时发送的字节码用 base64 编码后的字符串. 根据你之前序列化的原则, 你可以自定义你解码的方式.

3. 合法的 Transformed 输出长这样:

.. code-block:: python

    {
        "recordId": "49546986683135544286507457936321625675700192471156785154",
        "result": "OK",
        "data": b"bytes",
    }

- result: "OK", "Dropped", "ProcessingFailed" 中的一个, 其中 OK 和 Dropped 表示成功, ProcessingFailed 表示失败.
- data: 将你的数据序列化成字节码, 然后使用 base64 编码成字节码.

4. 如果一次性处理多个 Record, 最后 Firehose Dump 到 S3 文件时, 多个 Record 之间是以字节码直接拼接的形式 Dump 的. 这里有必要解释一下.

下面是一段帮助用户在各种 base64 字节码, 字符串 之间转换的代码

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
    Kinesis Programming Model.
    """

    import attr
    import typing
    import json
    import base64
    from datetime import datetime


    @attr.s
    class KinesisStreamInputRecord(object):
        recordId = attr.ib()  # type: str
        approximateArrivalTimestamp = attr.ib()  # type: int
        data = attr.ib()  # type: typing.Union[str, list, dict]

        @property
        def approximateArrivalDatetime(self):
            """

            :type: datetime
            """
            return datetime.fromtimestamp(self.approximateArrivalTimestamp / 1000.0)

        @property
        def binary_data(self):
            """

            :type: bytes
            """
            return base64.b64decode(self.data.encode("utf-8"))

        @property
        def string_data(self):
            """

            :type: str
            """
            return self.binary_data.decode("utf-8")

        @property
        def json_data(self):
            """

            :rtype: typing.Union[list, dict]
            """
            return json.loads(self.string_data)


    @attr.s
    class KinesisStreamOutputRecord(object):
        recordId = attr.ib()
        result = attr.ib()  # type: str
        data = attr.ib()  # type: typing.Union[bytes, str, list, dict]

        def to_dict(self):
            return dict(
                recordId=self.recordId,
                result=self.result,
                data=base64.b64encode(json.dumps(self.data).encode("utf-8")),
            )


    record_data = {
        "recordId": "49546986683135544286507457936321625675700192471156785154",
        "approximateArrivalTimestamp": 1495072949453,
        "data": "eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9", # {'a': 1, 'b': 2, 'c': 3}
    }

    input_record = KinesisStreamInputRecord(**record_data)
    print(input_record.approximateArrivalDatetime)
    print(input_record.json_data)


    output_record = KinesisStreamOutputRecord(
        recordId=input_record.recordId,
        result="OK",
        data={k: v * v for k, v in input_record.json_data.items()}
    )
    print(output_record.data)
    print(output_record.to_dict())
