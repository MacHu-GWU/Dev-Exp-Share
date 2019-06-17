# -*- coding: utf-8 -*-

"""
``pynamodb`` 库是 Python 中 DynamoDB 的 ORM 库. 由于 boto3 的原生 API 非常晦涩难懂复杂,
所以我非常推荐使用 ``pynamodb`` 库.
"""

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

os.environ["AWS_DEFAULT_PROFILE"] = "skymap_sandbox"


class UserModel(Model):
    class Meta:
        table_name = "learn-dynamodb-users"
        region = "us-east-1"

    username = UnicodeAttribute(hash_key=True)
    firstname = UnicodeAttribute(null=True)
    lastname = UnicodeAttribute(null=True)


UserModel.create_table(read_capacity_units=1, write_capacity_units=1)


def delete_all(model):
    with model.batch_write() as batch:
        item_list = list(model.scan())
        for item in item_list:
            batch.delete(item)


# reset table first
delete_all(UserModel)

# create UserModel(username="alice", firstname="Alice")
user = UserModel(username="alice", firstname="Alice")
user.save()

user = UserModel.get("alice")
assert user.firstname == "Alice"
assert user.lastname == None

# update firstname, it will overwrite the entire item
user = UserModel(username="alice")
user.lastname = "Donald"
user.save()

# firstname attribute gone ...
user = UserModel.get("alice")
assert user.firstname == None
assert user.lastname == "Donald"

# the correct way to update lastname
# let's recreate UserModel(username="alice", firstname="Alice")
user = UserModel(username="alice", firstname="Alice")
user.save()

user = UserModel.get("alice")
user.update(
    actions=[
        UserModel.lastname.set("Donald")
    ]
)

# lastname has been correctly updated
user = UserModel.get("alice")
assert user.firstname == "Alice"
assert user.lastname == "Donald"

# refresh method
user = UserModel(username="alice")
user.refresh()  # user.refresh() is inplace update, equals to user = UserModel.get("alice")
assert user.firstname == "Alice"
assert user.lastname == "Donald"
