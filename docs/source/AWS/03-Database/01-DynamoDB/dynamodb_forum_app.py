# -*- coding: utf-8 -*-

"""

"""

import boto3
from pprint import pprint

aws_profile = "eqtest"
ses = boto3.Session(profile_name=aws_profile)
client = ses.client("dynamodb")