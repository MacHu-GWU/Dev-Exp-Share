# -*- coding: utf-8 -*-

import decorator
from loguru import logger

@decorator.decorator
def with_verbose(func, *args, **kwargs):
    if "verbose" in kwargs:
        verbose = kwargs.pop("verbose")
    else:
        verbose = False

    if verbose:
        logger.disable("__main__")
    result = func(*args, **kwargs)
    if verbose:
        logger.enable("__main__")
    return result

@with_verbose
def add_two(x, y):
    logger.info(f"input: x = {x}, y = {y}")
    res = x + y
    logger.info(f"output: {res}")
    return res


add_two(x=1, y=2)
