# -*- coding: utf-8 -*-

"""
Library level logger.
"""

from pathlib_mate import Path
from loguru import logger

dir_loguru = Path.dir_here(__file__).parent


def filter_by_name(name: str) -> callable:
    def func(record: dict) -> bool:
        return record["extra"].get("name") == name

    return func


logger_a = logger.bind(name="logger_a")
logger_a.add("library.log", filter=filter_by_name(name="logger_a"))

logger_b = logger.bind(name="logger_b")
logger_b.add("library.log", filter=filter_by_name(name="logger_b"))
