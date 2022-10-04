# -*- coding: utf-8 -*-
# content of ``my_package/app.py``

from . import constant, helpers
from .config import Config


def print_constant():
    print(f"constant.key1 = {constant.key1}")
    print(f"constant.key2 = {constant.key2}")
    print(f"constant.key3 = {constant.key3}")


def print_now():
    print(f"now is {helpers.utc_now()}")


def print_config():
    config = Config(env="prod")
    print(f"config.project_name = {config.project_name}")


def print_db_table_name():
    config = Config(env="prod")
    print(f"config.make_db_table_name = {config.make_db_table_name(env='prod')}")
