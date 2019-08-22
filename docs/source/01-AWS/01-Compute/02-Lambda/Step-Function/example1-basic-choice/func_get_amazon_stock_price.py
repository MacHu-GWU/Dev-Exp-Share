# -*- coding: utf-8 -*-

"""
随机生成一个价格, 模拟爬虫抓取.
"""

import random

def lambda_handler(event, context):
    amazon_stock_price = random.randint(90, 110)
    return {"price": amazon_stock_price}
