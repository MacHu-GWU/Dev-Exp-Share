# -*- coding: utf-8 -*-

from loguru import logger

# logger.info("good")

print(id(logger))
def good():
    from loguru import logger

    print(id(logger))

good()