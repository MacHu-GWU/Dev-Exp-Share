# -*- coding: utf-8 -*-

"""

"""

import os

import pynamodb
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.exceptions import UpdateError

from flask import Flask, request

# --- Dynamodb
os.environ["AWS_DEFAULT_PROFILE"] = "aws_data_lab_sanhe_us_east_2"
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"

connection = Connection()


class Counter(Model):
    class Meta:
        table_name = "locust_test_counter_app"
        region = os.environ["AWS_DEFAULT_REGION"]
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    key = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(default=0)

    def plus_one(self):
        try:
            self.update(actions=[Counter.count.set(Counter.count + 1)])
        except UpdateError:
            self.count = 1
            self.save()

    @classmethod
    def delete_all(cls):
        with cls.batch_write() as batch:
            for item in cls.scan():
                batch.delete(item)


Counter.create_table(wait=True)
# Counter.delete_table()

# --- Flask
app = Flask(__name__)


@app.route(
    "/delete_all",
    methods=["GET", ]
)
def delete_all():
    if request.method == "GET":
        Counter.delete_all()
        return "All Dynamodb items are removed"
    else:
        raise Exception


@app.route(
    "/plus_one",
    methods=[
        "POST",
    ],
)
def plus_one():
    if request.method == "POST":
        print("=" * 80)
        print(f"{request.form}")
        print("=" * 80)
        counter = Counter(key=request.form["key"])
        counter.plus_one()
        return f"{request.form}"
    else:
        raise Exception
