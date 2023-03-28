# Pynamodb Tutorial


## Overview

``pynamodb`` is an ORM (objective relation mapping) framework for AWS Dynamodb. It allows you to save hundreds line of code dealing with data value converting, and provides eazy to use, human readable, clean API to perform CRUD easily. It always is recommended to declare a data model in your application code rather than manipulating the raw python dictionary, because it is not easy to maintain and hard to read.  

Without ``pynamodb``

```python

# Insert item
dynamodb_client.put_item(
    TableName="users",
    Item={ # complicate data type adaptor
        "id": {"S": "uid-1"},
        "email": {"S": "alice@example.com"}, # if it is not string type, you need additional code to convert the raw value to string
    }
)

# Query
response = dynamodb_client.query(
    TableName="users",
    KeyConditions={
        "id": {"S": "uid-1"}
    }
)
for item_dict in response["Items"]:
    # you need additional code to convert the item back to native python dictionary
    email = item_dict["id"]["S"] # if it is not string type, you need additional code to convert it back to raw value, like integer, binary ...
    print(email)
```

With ``pynamodb``

```python
# Declare data model
class Users(Model):
    class Meta:
        table_name = "users"
        region = "us-east-1"

    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    
# Insert item
user = Users(id="uid-1", email="alice@example.com") # pass in value as it is, no convertion needed
user.save()

# Query 
for user in Users.query(hash_key="uid-1"):
    # visit dictionary view easily
    print(user.attribute_values)
    # visit raw value as it is
    print(user.email)
```

## Pynamodb Documentation Links

- Pynamodb document: https://pynamodb.readthedocs.io/en/latest/
- Use data model, create / delete dynamodb table: https://pynamodb.readthedocs.io/en/latest/tutorial.html#getting-started
- Use Index: https://pynamodb.readthedocs.io/en/latest/indexes.html


## Sample Code - Single Data Model, No Relationship

In this example, I will demonstrate:

1. How to create a data model for dynamodb table.
2. Basic CRUD:
   - Create:
      - insert one item
      - bulk insert
   - Read:
      - query by keys
      - filter by non-keys attribute
   - Update:
      - full replacement
      - key / value update (recommended for most of scenario)
   - Delete

```python
# -*- coding: utf-8 -*-

"""
Author: sanhehu@amazon.com
"""

import pynamodb
from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

# create boto3 dynamodb client connection with default AWS profile
connection = Connection()
# if you want to use different profile, uncomment below code
# import os
# os.environ["AWS_DEFAULT_PROFILE"] = "a_different_aws_profile_for_aws_cli_on your_local"

# Create bank account data model
class Accounts(Model):
    class Meta:
        """
        declare metadata about the table
        """
        table_name = "accounts"
        region = "us-east-1"

        # billing mode
        # doc: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html
        # pay as you go mode
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

        # provisioned mode
        # write_capacity_units = 10
        # read_capacity_units = 10

    # define attributes
    account_id = UnicodeAttribute(hash_key=True)
    primary_holder_email = UnicodeAttribute()
    balance = NumberAttribute(default=0) # set default value for attribute
    create_time = UnicodeAttribute()
    description = UnicodeAttribute(null=True) # allow null value for this attribute


# Create dynamodb table if not exists, if already exists, this code won't do anything
Accounts.create_table(wait=True)

# Insert one item
Accounts(
    account_id="111-111-1111",
    primary_holder_email="alice@example.com",
    balance=0,
    create_time="2000-01-01 10:00:00",
    description="alice's account"
).save()

# Query one item
account = Accounts.query(hash_key="111-111-1111").next()
print(account.balance) # visit value using object, should be 0
print(account.attribute_values) # visit value using python dictionary, should be {"account_id": "111-111-111", "primary_holder_email": "alice@example.com", ...}

# Update one item - key / value update
# change primary holder and description
Accounts(account_id="111-111-1111").update( # specify the item you want to update by hash key
    # define multiple update actions
    actions=[
        Accounts.primary_holder_email.set("bob@example.com"),
        Accounts.description.set("bob's account'"),
    ]
)

# atomic balance change
Accounts(account_id="111-111-1111").update( # specify the item you want to update by hash key
    actions=[
        Accounts.balance.set(Accounts.balance + 1),
    ]
)

# WARNING, NEVER DO THIS, this operation is not atomic
# if you have multiple worker running this code, it may cause double pay or double spend
account = Accounts.query(hash_key="111-111-1111").next()
account.balance = account.balance + 1
account.save()


# Update one item - replacement the existing one
Accounts(
    account_id="111-111-1111",
    primary_holder_email="cathy@example.com",
    balance=0,
    create_time="2000-01-01 10:00:00",
    # even though we don't change description here, but the old description is gone, because it is a full item replacement.
).save()


# Build insert
# create some dummy data in memory, or read from csv, database, etc ...
many_account_data = [
    dict(account_id="222-222-2222", primary_holder_email="john@example.com", create_time="2000-01-02 00:00:00"),
    dict(account_id="333-333-3333", primary_holder_email="mike@example.com", create_time="2000-01-03 00:00:00"),
    dict(account_id="444-444-4444", primary_holder_email="smith@example.com", create_time="2000-01-04 00:00:00"),
]

with Accounts.batch_write() as batch:
    for account_data in many_account_data:
        account = Accounts(**account_data)
        batch.save(account)


# Filter by non-keys attribute
for account in Accounts.scan(
        filter_condition=Accounts.create_time.between("2000-01-01 23:59:59", "2000-01-03 23:59:59")
):
    print(account.attribute_values)
    # expected output
    # {'balance': 0, 'account_id': '222-222-2222', 'create_time': '2000-01-02 00:00:00', 'primary_holder_email': 'john@example.com'}
    # {'balance': 0, 'account_id': '333-333-3333', 'create_time': '2000-01-03 00:00:00', 'primary_holder_email': 'mike@example.com'}


# Bulk delete
with Accounts.batch_write() as batch:
    for account in Accounts.scan(
            filter_condition=Accounts.create_time.between("2000-01-01 23:59:59", "2000-01-03 23:59:59")
    ):
        batch.delete(account)

```

## Sample Code - Data Model with many-to-many Relationship and Index

In this example, I will demonstrate:

1. How to define index.
2. How to query many-to-many relationship efficiently using pynamodb

```python
# -*- coding: utf-8 -*-

"""
author: sanhehu@amazon.com
"""

import pynamodb
from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

connection = Connection()


# Create Index, allow us to query order that contains specific item
class ItemOrderIndex(GlobalSecondaryIndex):
    class Meta:
        index = "item-and-order-index"
        projection = KeysOnlyProjection

    item_id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)


# Create Orders data model
class Orders(Model):
    class Meta:
        table_name = "orders"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    # define attributes
    order_id = UnicodeAttribute(hash_key=True)
    item_id = UnicodeAttribute(range_key=True)
    item_unit_price = NumberAttribute()
    quantity = NumberAttribute()

    # associate index
    item_order_index = ItemOrderIndex()


Orders.create_table(wait=True)

# Insert one item
many_order_data = [
    dict(order_id="order-1", item_id="item-1-apple", item_unit_price=0.8, quantity=3),
    dict(order_id="order-1", item_id="item-2-banana", item_unit_price=0.4, quantity=5),
    dict(order_id="order-2", item_id="item-2-banana", item_unit_price=0.4, quantity=8),
    dict(order_id="order-2", item_id="item-3-cheery", item_unit_price=1.3, quantity=2),
]
with Orders.batch_write() as batch:
    for order_data in many_order_data:
        order = Orders(**order_data)
        batch.save(order)

# Given a order id, find out all items in that order
for order in Orders.query(hash_key="order-1"):
    print(order.attribute_values)

# Given a item id, find out all order that has that item
for order in ItemOrderIndex.query(hash_key="item-2-banana"):
    print(order.attribute_values)
```
