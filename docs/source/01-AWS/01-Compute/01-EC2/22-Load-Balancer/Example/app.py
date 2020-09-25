# -*- coding: utf-8 -*-

import os

from flask import Flask
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

app = Flask(__name__)

HOME = os.path.expanduser("~")

with open(os.path.join(HOME, "instance_id"), "r") as f:
    instance_id = f.read()


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
            InstanceVisitCountModel.count.set(InstanceVisitCountModel.count + 1),
        ])
    except Exception as e:
        if "does not exist in the item" in str(e):
            model.count = 1
            model.save()


@app.route("/")
def hello_world():
    count_plus_one(instance_id)
    return "visit count for {instance_id} +1".format(instance_id=instance_id)
