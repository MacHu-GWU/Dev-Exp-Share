# -*- coding: utf-8 -*-

from .logger import logger_a, logger_b


def func_a(v):
    logger_a.info(f"func_a, v = {v}")


def func_b(v):
    logger_b.info(f"func_b, v = {v}")
