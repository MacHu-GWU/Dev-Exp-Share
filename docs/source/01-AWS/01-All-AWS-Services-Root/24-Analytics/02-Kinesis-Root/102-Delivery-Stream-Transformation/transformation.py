# -*- coding: utf-8 -*-

"""
The lambda function that transform records pass through kinesis firehouse
"""

import json
import base64


def lambda_handler(event, context):
    """
    ``event`` example::

        {
            "invocationId": "invocationIdExample",
            "deliveryStreamArn": "arn:aws:kinesis:EXAMPLE",
            "region": "us-east-1",
            "records": [
                {
                    "recordId": "49546986683135544286507457936321625675700192471156785154",
                    "approximateArrivalTimestamp": 1495072949453,
                    "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4="
                },
                ...
            ]
        }

    return example::

        {
            "records": [
                {
                    "recordId": "49546986683135544286507457936321625675700192471156785154",
                    "result": "OK",
                    "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4="
                }
            ]
        }
    """
    output = []

    for record in event["records"]:
        print(record["recordId"])
        # convert the data back to raw data
        raw_record = json.loads(base64.b64decode(record["data"].encode("utf-8")))

        # Do custom processing on the payload here
        transformed_record = raw_record
        transformed_record["value"] = transformed_record["value"] * 100

        # convert transformed data to output
        output_record = {
            "recordId": record["recordId"],
            "result": "Ok", # "OK" | "Dropped" | "ProcessingFailed"
            "data": base64.b64encode((json.dumps(transformed_record) + "\n").encode('utf-8'))
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {"records": output}
