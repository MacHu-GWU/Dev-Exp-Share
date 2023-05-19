# -*- coding: utf-8 -*-

import json
import uuid
import random
from pathlib import Path
from boto_session_manager import BotoSesManager
from rich import print as rprint

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
arn = "arn:aws:lambda:us-east-1:807388292768:function:lambda-concurrency-control-test-worker"
key = "test"
wrong_key = "invalid_key"

request_list = list()
invalid_request_count = 0
for ith in range(1, 1 + 100):
    print(f"=== {ith} ===")
    request_id = uuid.uuid4().hex
    if random.randint(1, 10) == 1:
        request = {"key": wrong_key, "request_id": request_id}
        invalid_request_count += 1
    else:
        request = {"key": key, "request_id": request_id}
    request_list.append(request)
    response = bsm.lambda_client.invoke(
        FunctionName=arn, InvocationType="Event", Payload=json.dumps(request)
    )
    rprint(response)

data = {
    "request_list": request_list,
    "invalid_request_count": invalid_request_count,
}

Path("request_list.json").write_text(json.dumps(data, indent=4))
