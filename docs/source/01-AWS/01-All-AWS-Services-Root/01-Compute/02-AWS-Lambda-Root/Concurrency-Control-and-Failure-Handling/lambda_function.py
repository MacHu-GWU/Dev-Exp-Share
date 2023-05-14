# -*- coding: utf-8 -*-

"""
这个 Lambda Function 是一个 worker, 用来模拟实际业务中可能会出现的各种错误, 例如:

- 正常的业务逻辑会在 1 - 6 秒内完成.
- 有 30% 的概率会因为外部系统的网络抖动导致需要超过 6 秒.
- 有 20% 的概率会因为随机因素而出现错误, 重试几次后是会最终完成的.
- 还有 10% 的概率会收到错误的请求而导致永远不可能成功.

该业务逻辑的本质是给一个 key, 对应的 value 从 0 开始, 每运行一次就 + 1. 这个 key value
保存在 DynamoDB 中.

- 我们给 Lambda 设置了 6 秒的 timeout.
- 我们用 time.sleep() 来模拟 1 - 6 秒的计算.
- 我们用一个含有 10 个元素的数组, 其中 70% 的数在 1 - 4 之间, 肯定不会超时, 而 30% 的数大于 8, 肯定超时了.
- 我们用 random.randint(1, 10) 来模拟 20% 的概率会失败.
- 我们在发送请求的时候, 有 10% 的概率发送一个错误的 key, 由于这个 key 根本不存在, 所以永远没法 + 1.
"""

import time
import random
from pynamodb.connection import Connection
from pynamodb.models import Model, PAY_PER_REQUEST_BILLING_MODE
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

connection = Connection()


class Item(Model):
    class Meta:
        table_name = "lambda-concurrency-control-test"
        region = "us-east-1"
        billing_mode = PAY_PER_REQUEST_BILLING_MODE

    key = UnicodeAttribute(hash_key=True)
    count = NumberAttribute()


# run this only once to create the table, and then comment it out.
# Item.create_table(wait=True)

delay = [1, 2, 3, 1, 2, 3, 4, 8, 9, 10]


def lambda_handler(event, context):
    key = event["key"]
    print(f"------ processing key {key!r} count + 1 ------")
    time.sleep(random.choice(delay))
    if random.randint(1, 10) <= 2:
        raise ValueError
    Item(key=key).update(actions=[Item.count.set(Item.count + 1)])
    return {"status": "succeeded"}
