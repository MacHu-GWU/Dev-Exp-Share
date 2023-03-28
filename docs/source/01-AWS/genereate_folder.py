# -*- coding: utf-8 -*-

"""
这个脚本用来根据 https://aws.amazon.com/ 的 Product 页面中对 AWS 服务的分类, 生成对应的文件夹.
"""

from pathlib import Path

# 生成文件夹之前记得做这么几件事:
# 1. 修改不合法字符, 文件夹中不允许有空格, 空格都用 - 代替.
# 2. 对顺序进行排列
products = [
    # 三巨头
    "01-Compute",
    "02-Storage",
    "03-Networking and Content Delivery",
    # 所有其他服务的基础, AWS Account 管理
    "11-Security Identity and Compliance",
    "12-Management and Governance",
    "13-Cloud Financial Management",
    # 其他常用服务 1
    "21-Database",
    "22-Containers",
    "23-Serverless",
    "24-Analytics",
    "25-Developer Tools",
    "26-Application Integration",
    "27-Machine Learning",
    # 其他常用服务 2
    "31-Migration and Transfer",
    "32-Front End Web and Mobile",
    # 垂直领域服务 1 传统行业
    "41-Business Applications",
    "42-End User Computing",
    "43-Contact Center",
    "44-Media Services",
    "45-Games",
    # 垂直领域服务 2 新兴行业
    "51-Internet of Things",
    "52-Blockchain",
    "53-Quantum Technologies",
    "54-Robotics",
    "55-Satellite",
]

dir_here = Path(__file__).absolute().parent

for folder in products:
    folder_name = folder.replace(" ", "-")
    dir_here.joinpath(folder_name).mkdir(exist_ok=True)
