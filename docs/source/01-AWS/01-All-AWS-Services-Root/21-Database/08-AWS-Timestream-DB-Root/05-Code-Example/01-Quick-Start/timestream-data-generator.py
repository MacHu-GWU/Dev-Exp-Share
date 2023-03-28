# -*- coding: utf-8 -*-

"""
This python script is a timeseries data generator that randomly pick
a sensor in US and generate 10 observation of temperature and humidity every
second. Then you can go back to the Jupyter Notebook and focus on writing query.
"""

import boto3
from rich import print

boto_ses = boto3.session.Session()
ts_write = boto_ses.client("timestream-write")
ts_query = boto_ses.client("timestream-query")

database = "timestream-quick-start"
table = "weather-sensor"


def is_database_exists(database: str) -> bool:
    try:
        ts_write.describe_database(
            DatabaseName=database,
        )
        return True
    except Exception as e:
        if str(e.__class__.__name__) == "ResourceNotFoundException":
            return False
        else:
            raise e


if is_database_exists(database) is False:
    print(f"TimeStream database {database!r} not exist, create one ...")
    res = ts_write.create_database(
        DatabaseName=database,
    )
else:
    print(f"TimeStream database {database!r} already exist, do nothing")


def is_table_exists(database: str, table: str) -> bool:
    try:
        ts_write.describe_table(
            DatabaseName=database,
            TableName=table,
        )
        return True
    except Exception as e:
        if str(e.__class__.__name__) == "ResourceNotFoundException":
            return False
        else:
            raise e


if is_table_exists(database, table) is False:
    print(f"TimeStream table {database!r}.{table!r} not exist, create one ...")
    res = ts_write.create_table(
        DatabaseName=database,
        TableName=table,
        RetentionProperties=dict(
            MemoryStoreRetentionPeriodInHours=1,
            MagneticStoreRetentionPeriodInDays=1,
        )
    )
else:
    print(f"TimeStream table {database!r}.{table!r} already exist, do nothing")

import time
import random
from datetime import datetime, timezone

EPOCH = datetime(1970, 1, 1)


def utc_now() -> str:
    time.sleep(random.randint(50, 150) / 1000)
    return str(int((datetime.utcnow() - EPOCH).total_seconds() * 1000))


class DataTypeEnum:
    DOUBLE = "DOUBLE"
    BIGINT = "BIGINT"
    VARCHAR = "VARCHAR"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    MULTI = "MULTI"


class FieldEnum:
    temperature = "temperature"
    humidity = "humidity"


device_list = [
    dict(
        device_id="device-KS",
        device_lat="039.045167",
        device_lng="-094.580552",
    ),
    dict(
        device_id="device-WA",
        device_lat="047.516842",
        device_lng="-120.556755",
    ),
    dict(
        device_id="device-CA",
        device_lat="037.351811",
        device_lng="-119.870587",
    ),
    dict(
        device_id="device-NY",
        device_lat="042.965073",
        device_lng="-075.073632",
    ),
    dict(
        device_id="device-FL",
        device_lat="028.049414",
        device_lng="-081.641238",
    ),
]

device_dimension_list = [
    [
        dict(
            Name=key,
            Value=value,
            DimensionValueType=DataTypeEnum.VARCHAR,
        )
        for key, value in data.items()
    ]
    for data in device_list
]


def put_records():
    try:
        res = ts_write.write_records(
            DatabaseName=database,
            TableName=table,
            CommonAttributes=dict(
                Dimensions=random.choice(device_dimension_list),
            ),
            Records=[
                dict(
                    Time=utc_now(),
                    TimeUnit="MILLISECONDS",
                    MeasureName="observation",
                    MeasureValueType=DataTypeEnum.MULTI,
                    MeasureValues=[
                        dict(
                            Name=FieldEnum.temperature,
                            Value=str(random.randint(32, 102)),
                            Type=DataTypeEnum.BIGINT,
                        ),
                        dict(
                            Name=FieldEnum.humidity,
                            Value=str(random.randint(20, 80) / 100),
                            Type=DataTypeEnum.DOUBLE,
                        )
                    ]
                )
                for _ in range(10)
            ]
        )
        # print(res)
    except ts_write.exceptions.RejectedRecordsException as err:
        print("RejectedRecords: ", err)
        for rr in err.response["RejectedRecords"]:
            print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
        print("Other records were written successfully. ")


for i in range(1, 3600 + 1):
    print(f"{i} th")
    time.sleep(1)
    put_records()
