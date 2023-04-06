# -*- coding: utf-8 -*-

"""
在 SQL 中我们常有一种查询模式是 根据某个 Column, 通常是时间, 筛选出部分数据, 然后排序返回.
比如博客应用中的列出最近所有帖子. 在 SQL 中式这么写的::

    SELECT * FROM table t
    WHERE t.time BETWEEN ...

但是在 DynamoDB 中, 如果你要使用 query, 则你必须制定 Hash Key, 而你只想根据 Range Key 来查询.
所以此时我们只能用 scan 了.

Reference

- scan() API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan
"""

import os
import rolex
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

os.environ["AWS_DEFAULT_PROFILE"] = "skymap_sandbox"


class EventModel(Model):
    class Meta:
        table_name = "learn-dynamodb-events"
        region = "us-east-1"

    event_id = UnicodeAttribute(hash_key=True)
    time = UnicodeAttribute(range_key=True)


def delete_all(model):
    with model.batch_write() as batch:
        item_list = list(model.scan())
        for item in item_list:
            batch.delete(item)


def create_sample_data():
    n_event = 50
    start = "2019-01-01"
    end = "2019-01-08"
    for event_id in range(1, 1 + n_event):
        time = rolex.rnd_datetime(start, end)
        event = EventModel(event_id="eid_%s" % str(event_id).zfill(16), time=str(time))
        event.save()


def run_scan():
    results = EventModel.scan(
        filter_condition=(EventModel.time >= "2019-01-03") & (EventModel.time < "2019-01-04")
    )
    results = list(sorted(results, key=lambda x: x.time, reverse=True))
    for item in results:
        print(item.time)


if __name__ == "__main__":
    EventModel.create_table(read_capacity_units=5, write_capacity_units=5)
    # delete_all(EventModel)
    # create_sample_data()
    run_scan()
