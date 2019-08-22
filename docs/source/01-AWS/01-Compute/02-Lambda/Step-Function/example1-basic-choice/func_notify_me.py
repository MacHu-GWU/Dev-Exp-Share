# -*- coding: utf-8 -*-

"""
将 amazon_stock_price 信息发送给我. 这里没有设置 SNS, 只是对 S3 写入一个文件进行模拟通知.
"""

import boto3
from datetime import datetime


def lambda_handler(event, context):
    price = event["amazon_stock_price"]
    bucket_name = "eqtest-sanhe"
    utcnow = datetime.utcnow()
    key = "{}.txt".format(utcnow.strftime("%Y-%m-%d-%H-%M-%S"))
    body = "amazon price on %s is %s" % (utcnow, price)

    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket_name, Key=key, Body=body.encode("utf-8"))
    return {"message": body}
