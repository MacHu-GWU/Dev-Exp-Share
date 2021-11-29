# -*- coding: utf-8 -*-

"""
Order to Item is Many to Many.

在 RDBMS 中通常是 2 个 entity table 1 个 双 primary key 的 association table.

dynamodb 中可以只用一个 association table 即可. 选一个 entity_1_id 作为 hash key,
entity_2_id 作文 range key. 然后建立 GSI, 把 entity_2_id 作为 hash key, 把
entity_1_id 作为 range key. 这样就能满足大部分的查询了
"""

import os
import random

import pynamodb
from pynamodb.attributes import UnicodeAttribute
from pynamodb.connection import Connection
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.models import Model

os.environ["AWS_DEFAULT_PROFILE"] = "eq_sanhe"

connection = Connection()


class ItemOrderIndex(GlobalSecondaryIndex):
    class Meta:
        index = "many-to-many-department-item-and-order-index-1"
        projection = KeysOnlyProjection

    item_id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)


class OrderAndItem(Model):
    class Meta:
        table_name = "many-to-many-order-and-item-1"
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


def create_orders():
    OrderAndItem.create_order("o1", ["i1", "i2"])
    OrderAndItem.create_order("o2", ["i2", "i3"])
    OrderAndItem.create_order("o3", ["i3", "i1"])


# create_orders()

# --- Bussiness Query
class BQuery:
    @classmethod
    def find_items_in_order(cls, order_id):
        for oi in OrderAndItem.query(hash_key=order_id):
            yield oi.item_id

    @classmethod
    def find_order_include_item(cls, item_id):
        for oi in ItemOrderIndex.query(hash_key=item_id):
            yield oi.order_id


def find_items_in_order():
    for item_id in BQuery.find_items_in_order(order_id="O1"):
        print(item_id)


# find_items_in_order()

def find_order_include_item():
    for order_id in BQuery.find_order_include_item(item_id="I1"):
        print(order_id)


# find_order_include_item()


# --- Performance Test

def create_super_many_orders():
    n_item = 10000
    n_order = 100000

    item_id_list = [f"I{i}" for i in range(1, n_item + 1)]
    n_item_per_order_upper = 6
    n_item_per_order_lower = 1

    with OrderAndItem.batch_write() as batch:
        for order_id in range(1, n_order + 1):
            order_id = f"O{order_id}"
            print(order_id)
            for item_id in random.sample(item_id_list, random.randint(n_item_per_order_lower, n_item_per_order_upper)):
                oi = OrderAndItem(order_id=order_id, item_id=item_id)
                batch.save(oi)


# create_super_many_orders()


def delete_all_tables():
    OrderAndItem.delete_table()

# delete_all_tables()
