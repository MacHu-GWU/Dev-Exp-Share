# -*- coding: utf-8 -*-

from sqlalchemy_mate import EngineCreator, test_connection
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import String, Integer

engine = EngineCreator.from_home_db_json("aurora-dev").create_postgresql_psycopg2()
# test_connection(engine, timeout=3)

metadata = MetaData()
t_users = Table(
    "user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)
metadata.create_all(engine)

user_data = [
    dict(id=1, name="Alice"),
    dict(id=2, name="Bob"),
    dict(id=3, name="Cathy")
]

