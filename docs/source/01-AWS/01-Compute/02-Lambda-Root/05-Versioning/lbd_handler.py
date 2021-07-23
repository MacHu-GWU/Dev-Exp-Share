# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import pynamodb
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

is_lbd_runtime = "AWS_LAMBDA_FUNCTION_NAME" in os.environ

if is_lbd_runtime:
    lbd_version = os.environ["AWS_LAMBDA_FUNCTION_VERSION"]
else:
    os.environ["AWS_PROFILE"] = "sanhe"
    lbd_version = "local"

_ = "Current Version = 3"


class LbdEvent(Model):
    class Meta:
        table_name = "lbd-events"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    date = UnicodeAttribute(hash_key=True)
    time = UnicodeAttribute(range_key=True)
    value = UnicodeAttribute()


LbdEvent.create_table(wait=True)


def main(event, context):
    now = str(datetime.utcnow() - timedelta(hours=4))
    lbd_event = LbdEvent(
        date=now[:10],
        time=now[11:],
        value=lbd_version,
    )
    print(lbd_event)
    if is_lbd_runtime:
        lbd_event.save()


if __name__ == "__main__":
    main(None, None)
