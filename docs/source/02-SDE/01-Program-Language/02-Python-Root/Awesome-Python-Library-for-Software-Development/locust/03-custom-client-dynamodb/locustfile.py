# -*- coding: utf-8 -*-

"""
HOST = https://www.python.org


"""

import os
import time
import random
import json

import pynamodb
from locust import User, task, constant
from pynamodb.attributes import UnicodeAttribute
from pynamodb.connection import Connection
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.models import Model

os.environ["AWS_DEFAULT_PROFILE"] = "eq_sanhe"

connection = Connection()


class ItemOrderIndex(GlobalSecondaryIndex):
    class Meta:
        index = "many-to-many-department-item-and-order-index-3"
        projection = KeysOnlyProjection

    item_id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)


class OrderAndItem(Model):
    class Meta:
        table_name = "many-to-many-order-and-item-3"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    order_id = UnicodeAttribute(hash_key=True)
    item_id = UnicodeAttribute(range_key=True)

    item_order_index = ItemOrderIndex()

    @classmethod
    def create_order(cls, order_id, item_id_list):
        with OrderAndItem.batch_write() as batch:
            for item_id in item_id_list:
                batch.save(cls(order_id=order_id, item_id=item_id))


OrderAndItem.create_table(wait=True)


class BQuery:
    @classmethod
    def find_items_in_order(cls, order_id):
        for oi in OrderAndItem.query(hash_key=order_id):
            yield oi.item_id

    @classmethod
    def find_order_include_item(cls, item_id):
        for oi in ItemOrderIndex.query(hash_key=item_id):
            yield oi.order_id


class DynamodbClient:
    """
    XmlRpcClient is a wrapper around the standard library's ServerProxy.
    It proxies any function calls and fires the *request* event when they finish,
    so that the calls get recorded in Locust.
    """

    def __init__(self, host, request_event):
        self._request_event = request_event

    def find_item_in_order(self, order_id):
        start_time = time.perf_counter()
        request_meta = {
            "request_type": "dynamodb",
            "name": "find_item_in_order",
            "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
            "response": None,
            "context": {},  # see HttpUser if you actually want to implement contexts
            "exception": None,
        }
        try:
            item_id_list = list(BQuery.find_items_in_order(order_id))
            print(f"Order({order_id}) has {len(item_id_list)} items")
            request_meta["response"] = ", ".join(item_id_list)
        except Exception as e:
            request_meta["exception"] = e
        request_meta["response_time"] = (time.perf_counter() - start_time) * 1000
        self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust
        return request_meta["response"]


class DynamodbUser(User):
    """
    A minimal Locust user class that provides an XmlRpcClient to its subclasses
    """

    abstract = True  # dont instantiate this as an actual user when running Locust

    def __init__(self, environment):
        super().__init__(environment)
        self.client = DynamodbClient(self.host, request_event=environment.events.request)


# The real user class that will be instantiated and run by Locust
# This is the only thing that is actually specific to the service that we are testing.
class MyUser(DynamodbUser):
    host = "http://127.0.0.1:8877/"

    wait_time = constant(1)

    @task
    def run_query(self):
        self.client.find_item_in_order(order_id=f"O{random.randint(1, 100000)}")

