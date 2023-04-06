# -*- coding: utf-8 -*-

import sqlalchemy as sa
from pysecret import AWSSecret
from sqlalchemy_mate import EngineCreator
aws_profile = "sanhe"
secret_id = "db-demo-configure-rds"

aws = AWSSecret(profile_name=aws_profile)
engine = EngineCreator(
    host=aws.get_secret_value(secret_id, "host"),
    port=int(aws.get_secret_value(secret_id, "port")),
    database=aws.get_secret_value(secret_id, "database"),
    username=aws.get_secret_value(secret_id, "username"),
    password=aws.get_secret_value(secret_id, "password"),
).create_postgresql_psycopg2()

print(aws.secret_cache)
# stmt = sa.text("SELECT 999;")
# result = engine.execute(stmt).fetchone()[0]
# print(result)
