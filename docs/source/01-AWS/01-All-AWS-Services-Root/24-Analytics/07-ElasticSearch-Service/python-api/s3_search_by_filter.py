# -*- coding: utf-8 -*-

"""
**中文文档**

- ES 数据类型文档: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
"""

import connect
from datetime import datetime

from elasticsearch_dsl import (
    Index, Document, Integer, Float, Date, Text,
)
from superjson import json


def jprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))


class Laptop(Document):
    price = Integer()
    weight = Float()
    release_date = Date()
    product_name = Text()
    product_model = Text()

    class Index:
        name = "laptop"


def document_crud():
    # create the mappings in Elasticsearch
    Laptop.init()

    # instantiate the document
    laptops = [
        Laptop(
            price=1199,
            weight=2.75,
            release_date=datetime(2017, 1, 1),
            product_name="MacBook",
            product_model="2017",
            meta={"id": 1},
        ),
        Laptop(
            price=999,
            weight=2.1,
            release_date=datetime(2017, 1, 1),
            product_name="MacBookAir",
            product_model="2017",
            meta={"id": 2},
        ),
        Laptop(
            price=2399,
            weight=5.4,
            release_date=datetime(2017, 1, 1),
            product_name="MacBookPro",
            product_model="2017",
            meta={"id": 3},
        ),
    ]
    # for laptop in laptops:
    #     laptop.save()

    # retrieve the document
    res = Laptop.search() \
        .filter("range", price={"gt": 1100}) \
        .filter("range", weight={"gt": 3}) \
        .execute()
    assert len(list(res)) == 1
    assert list(res)[0].meta.id == str(3)


document_crud()


def index_crud():
    blogs = Index("laptop")
    # delete the index, ignore if it doesn't exist
    blogs.delete(ignore=404)

# index_crud()
