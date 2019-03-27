# -*- coding: utf-8 -*-

"""
API Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
"""

import os
import boto3
import dev_exp_share
from pprint import pprint

SANHE_AWS_ID = os.environ["SANHE_AWS_ID"]

aws_profile = "sanhe"
session = boto3.Session(profile_name=aws_profile)
sqs = session.client("sqs")

queue_url = "https://sqs.us-east-1.amazonaws.com/{SANHE_AWS_ID}/dev-exp-learn-sqs.fifo".format(
    SANHE_AWS_ID=SANHE_AWS_ID
)

# response = sqs.send_message(
#     QueueUrl=queue_url,
#     MessageBody="Hello1",
#     MessageGroupId="playground",
# )
# pprint(response)
"""
{'MD5OfMessageBody': '7a6d1b13498fb5b3085b2fd887933575',
 'MessageId': '41d5713f-bb60-4b81-a798-c5d28f7eb597',
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '431',
                                      'content-type': 'text/xml',
                                      'date': 'Thu, 21 Mar 2019 04:05:12 GMT',
                                      'x-amzn-requestid': '1da0c02b-11f1-56a6-812a-95261e4923d2'},
                      'HTTPStatusCode': 200,
                      'RequestId': '1da0c02b-11f1-56a6-812a-95261e4923d2',
                      'RetryAttempts': 0},
 'SequenceNumber': '18844348198489327616'}
"""

response = sqs.receive_message(
    QueueUrl=queue_url,
)
pprint(response)
"""
{'Messages': [{'Body': 'Hello1',
               'MD5OfBody': '7a6d1b13498fb5b3085b2fd887933575',
               'MessageId': '41d5713f-bb60-4b81-a798-c5d28f7eb597',
               'ReceiptHandle': 'AQEBBzhZQVq4PQoqCD4Xzkegis+zbgx57/I9cwiV9l2hvm65n41SIQqUWhB1mhMTfo6duAmOrNkby16K5KRv/JXrnhLRrnzBvtXbvPaf2MsQ6MkaQ7dFOdBRYCYlC4W4fgFqyHcJvZ/tVwAMV0mU1ftu0n800YuWoIDVta4ZADDHd+0WmctBIsfIWLPSI3swcXqDPzvIRxaug2pay79gczfyhsAkLqKCjJ0NS2kFASgzER2bjTbu99AKtlQRFq92JNMvfWBcEiXqODCx5IWlKp0ozSsht14w6qQNd9L8MuBlBWk='}],
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '749',
                                      'content-type': 'text/xml',
                                      'date': 'Thu, 21 Mar 2019 04:07:03 GMT',
                                      'x-amzn-requestid': '674567ef-1b6d-508b-b1ba-32e20b4ac397'},
                      'HTTPStatusCode': 200,
                      'RequestId': '674567ef-1b6d-508b-b1ba-32e20b4ac397',
                      'RetryAttempts': 0}}
"""