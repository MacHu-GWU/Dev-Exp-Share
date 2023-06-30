# -*- coding: utf-8 -*-

import json
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")

token = "your token here"
output = {
    # you have to define the external job run output here,
    # lambda function will read the $.Payload field
    "Payload": {"message": "succeeded"}
}
response = bsm.sfn_client.send_task_success(
    taskToken=token,
    output=json.dumps(output),
)