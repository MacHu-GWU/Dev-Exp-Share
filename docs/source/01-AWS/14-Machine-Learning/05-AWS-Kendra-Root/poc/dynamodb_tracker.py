# -*- coding: utf-8 -*-

import pynamodb
from pynamodb.models import Model, GlobalSecondaryIndex
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import KeysOnlyProjection


class Status:
    todo = 0
    failed = 1
    success = 2


class StatusIndex(GlobalSecondaryIndex):
    class Meta:
        index = "status-index"
        projection = KeysOnlyProjection

    status = NumberAttribute(hash_key=True)
    uri = UnicodeAttribute()


class KendraTracker(Model):
    class Meta:
        table_name = f"kendra-tracker"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    uri = UnicodeAttribute(hash_key=True)
    status = NumberAttribute(default=Status.todo)

    status_index = StatusIndex()


KendraTracker.create_table(wait=True)


tasks = StatusIndex.query(hash_key=Status.todo, limit=1000)
group_list(tasks, size=10)


