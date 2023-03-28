# -*- coding: utf-8 -*-

"""

- 传入的 parameters 必须要在 template 中进行声明
- template 中声明过的 parameters 没有被用到并没有关系
"""

import boto3
from superjson import json

from pathlib_mate import PathCls as Path

def pprint(data):
    print(json.dumps(data, sort_keys=True, indent=4))

aws_profile = "skymap_sandbox"
session = boto3.session.Session(profile_name=aws_profile)

iam = session.client("iam")

res = iam.get_role(
    RoleName="lambda-skymap-mpl-dev-rds-query"
)
# res = iam.list_attached_role_policies(
#     RoleName="lambda-skymap-mpl-dev-rds-query"
# )
pprint(res)
