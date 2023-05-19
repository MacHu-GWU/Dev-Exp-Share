# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
arn = "arn:aws:lambda:us-east-1:807388292768:function:lambda-concurrency-control-test-worker"
key = "test"
queue_url = (
    "https://sqs.us-east-1.amazonaws.com/807388292768/lambda-concurrency-control-test"
)

response = bsm.sqs_client.receive_message(
    QueueUrl=queue_url,
    AttributeNames=["All"],
    MaxNumberOfMessages=10,
)

entries = list()
for messages in response.get("Messages", []):
    body = messages["Body"]
    print(f"Message received: {body}")
    response = bsm.lambda_client.invoke(
        FunctionName=arn,
        InvocationType="Event",
        Payload=body,
    )
    entries.append(
        {"Id": messages["MessageId"], "ReceiptHandle": messages["ReceiptHandle"]}
    )

if len(entries):
    bsm.sqs_client.delete_message_batch(
        QueueUrl=queue_url,
        Entries=entries,
    )
