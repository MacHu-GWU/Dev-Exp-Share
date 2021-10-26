# -*- coding: utf-8 -*-

from rich import print
import time
import boto3

class Constant:
    database_name = "sampleDB"
    table_name = "stock"

ts_write = boto3.client("timestream-write")

def current_milli_timestamp(delta=0):
    return str(int(round(time.time() * 1000)) + delta)


def write_records():

    dimensions = [
        dict(Name="market", Value="NASDAQ"),
        dict(Name="symbol", Value="Amazon"),
    ]

    common_attributes = dict(
        Dimensions=dimensions,
        MeasureName="price",
        MeasureValueType="DOUBLE",
    )

    records = [
        dict(
            MeasureValue=str(3030),
            Time=current_milli_timestamp(delta=10000000),
        ),
        dict(
            MeasureValue=str(3040),
            Time=current_milli_timestamp(delta=10000001),
        )
    ]

    try:
        result = ts_write.write_records(
            DatabaseName=Constant.database_name,
            TableName=Constant.table_name,
            Records=records,
            CommonAttributes=common_attributes
        )
        print(result)
    except ts_write.exceptions.RejectedRecordsException as err:
        print(err.response)

    # result = ts_write.write_records(
    #     DatabaseName=Constant.database_name,
    #     TableName=Constant.table_name,
    #     Records=records,
    #     CommonAttributes=common_attributes
    # )
    #
    # print(result)

    # records = [
    #     dict(Name="market", Value="NYSE"),
    #     dict(Name="market", Value="Amazon"),
    # ]


write_records()


def another():
    current_time = self._current_milli_time()

    dimensions = [
        {'Name': 'region', 'Value': 'us-east-1'},
        {'Name': 'az', 'Value': 'az1'},
        {'Name': 'hostname', 'Value': 'host1'}
    ]

    cpu_utilization = {
        'Dimensions': dimensions,
        'MeasureName': 'cpu_utilization',
        'MeasureValue': '13.5',
        'MeasureValueType': 'DOUBLE',
        'Time': current_time
    }

    memory_utilization = {
        'Dimensions': dimensions,
        'MeasureName': 'memory_utilization',
        'MeasureValue': '40',
        'MeasureValueType': 'DOUBLE',
        'Time': current_time
    }

    records = [cpu_utilization, memory_utilization]

    try:
        result = self.client.write_records(DatabaseName=Constant.DATABASE_NAME, TableName=Constant.TABLE_NAME,
                                           Records=records, CommonAttributes={})
        print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
    except self.client.exceptions.RejectedRecordsException as err:
        print("RejectedRecords: ", err)
        for rr in err.response["RejectedRecords"]:
            print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
        print("Other records were written successfully. ")
    except Exception as err:
        print("Error:", err)