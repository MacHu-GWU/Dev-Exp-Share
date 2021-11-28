What is AWS Textract
==============================================================================


由于 Textract 的 Input 可能是很大的 PDF, 也可能是图像, 所以运算时间是不确定的, 有可能长到超过 AWS Lambda 的 15 minutes 的 Limitation. 所以 AWS 提供了一个 Async 的 API: ``https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_text_detection``. 能够发起请求后立刻返回. 而如果你想要 Async 的处理结束后自动继续下一步骤, 推荐的方法是使用 SNS Topic 接受 Textract 完成的信息. 然后有两种后续处理方式. 1 是用 AWS Lambda, 直接触发一个 Lambda 进行处理. 2 是将信息发送给 SQS Queue. 然后由用户自行决定如何做 Long polling. 这两者有利有弊. 直接用 Lambda 简单, 如果数据出错, 可能还是要将出错数据保存到 Dead Letter Queue, 这就跟方法 2 的复杂程度其实差不多了.




Textract 发送给 SNS 的 Message 其实是一个 Json dump 成 String 的形式. 具体 Schema 如下 (参考 https://docs.aws.amazon.com/textract/latest/dg/api-async.html#api-async-get-status):

.. code-block:: javascript

    {
        "JobId": "d6f20ee653647d82229bed53dde14a76188a676e1218b6bc0e52ffc57dd52ac8",
        "Status": "SUCCEEDED",
        "API": "StartDocumentTextDetection",
        "JobTag": "Receipt",
        "Timestamp": 1637887077969,
        "DocumentLocation": {
            "S3ObjectName": "document",
            "S3Bucket": "bucket"
        }
    }

而如果你用 SNS 直接触发 AWS Lambda, 那么 Lambda 收到的消息则是:

.. code-block:: javascript

    {
        'Records': [
            {
                'EventSource': 'aws:sns',
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'arn:aws:sns:us-east-1:669508176277:textract-test:3b51e7b5-ec63-4abc-9ea3-a854d6866964',
                'Sns': {
                    'Type': 'Notification',
                    'MessageId': '3878d011-ed99-5d93-901b-8a0bc33fb38e',
                    'TopicArn': 'arn:aws:sns:us-east-1:669508176277:textract-test',
                    'Subject': null,
                    'Message': '{"JobId":"d6f20ee653647d82229bed53dde14a76188a676e1218b6bc0e52ffc57dd52ac8","Status":"SUCCEEDED","API":"StartDocumentTextDetection","Timestamp":1637887077969,"DocumentLocation":{"S3ObjectName":"landing/lease.png","S3Bucket":"aws-data-lab-sanhe-text-insight-dev"}}',
                    'Timestamp': '2021-11-26T00:37:58.001Z',
                    'SignatureVersion': '1',
                    'Signature': 'TUluYeU2...',
                    'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-...',
                    'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:...',
                    'MessageAttributes': {}
                }
            }
        ]
    }