# -*- coding: utf-8 -*-

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

os.environ["AWS_PROFILE"] = "eq_sanhe"

class InstanceVisitCountModel(Model):
    class Meta:
        table_name = "instance-visit-count"
        region = "us-east-1"

    inst_id = UnicodeAttribute(hash_key=True)
    count = NumberAttribute()


def count_plus_one(instance_id):
    model = InstanceVisitCountModel(inst_id=instance_id)

    try:
        model.update(actions=[
            InstanceVisitCountModel.count.set(InstanceVisitCountModel.count+1),
        ])
    except Exception as e:
        if "does not exist in the item" in str(e):
            model.count = 1
            model.save()

instance_id = "i-001"
count_plus_one(instance_id)
