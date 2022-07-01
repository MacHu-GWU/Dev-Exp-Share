# -*- coding: utf-8 -*-

import sys
from functools import partial
from pathlib_mate import Path
from loguru import logger

dir_here = Path.dir_here(__file__)


def clear_all():
    """
    Clear off all existing log
    """
    for p in dir_here.select_by_ext(".log"):
        p.remove()


clear_all()


def e1_simple_logger():
    """
    The ``loguru.logger`` is a global logger.
    """
    logger.debug("debug 10 here")
    logger.info("info 20 here")
    logger.warning("warning 30 here")
    logger.error("error 40 here")
    logger.critical("critical 50 here")


def e2_format_and_handler():
    # remove built in sys.stderr handler
    logger.remove()

    # add new handler
    handler_id = logger.add(sys.stdout, format="Time = {time} | Level = {level: <8} | {message}")
    print(f"handler_id is {handler_id}")

    # start logging
    logger.debug("{key} - {value}", key="a", value=1)
    logger.info("{key} - {value}", key="a", value=1)
    logger.warning("{key} - {value}", key="a", value=1)
    logger.error("{key} - {value}", key="a", value=1)
    logger.critical("{key} - {value}", key="a", value=1)


def e3_sink():
    logger.add(Path(dir_here, "e3_sink.log"))
    logger.info("1")
    logger.info("2")
    logger.info("3")


def filter_by_name(name):
    def func(record):
        # print(record)
        return record["extra"].get("name") == name

    return func


def e4_logger_with_name_case1():
    """
    虽然是用 logger_app.add 注册的 handler 但是这个 handler 是全局生效的
    所以还是会将 "info from default 写入文件
    """
    logger_app = logger.bind(name="app")

    logger_app.add(Path(dir_here, "e4_logger_with_name.log"))

    logger.info("info from default")


def e4_logger_with_name_case2():
    """
    虽然是用 logger.add 注册的 handler 但是这个 handler 是全局生效的
    所以还是会将 "info from default 写入文件
    """
    logger_app = logger.bind(name="app")

    logger.add(Path(dir_here, "e4_logger_with_name.log"))

    logger_app.info("info from app")


def e5_filter():
    # 注册两个 handler
    handler_a = logger.add(
        Path(dir_here, "e5_filter.log"),
        filter=filter_by_name(name="company_a"),
    )
    handler_b = logger.add(
        Path(dir_here, "e5_filter.log"),
        filter=filter_by_name(name="company_b"),
    )

    # 创建两个预先绑定了变量的 logger
    logger_a = logger.bind(name="company_a")
    logger_b = logger.bind(name="company_b")

    # 每一条消息都经过了 3 个 handler, 不过 logger_a 发出的消息, 只会经过 handler_a
    logger_a.info("from company a, 1")
    logger_a.info("from company a, 2")
    logger_b.info("from company b, 1")
    logger_b.info("from company b, 2")


def e6_disable_and_enable_by_handler():
    """
    有一个常见的需求. 你的业务逻辑中有很多打印日志的项. 你可以在不修改业务逻辑的情况下, 选择
    启用或者禁用日志.
    """
    logger.remove() # remove default handler
    logger.info("1") # nothing happen

    handler_id = logger.add(sys.stdout)
    logger.info("2")

    logger.remove(handler_id) # remove specific handler
    logger.info("3")

    logger.add(sys.stdout)
    logger.info("4")

    logger.remove() # remove last handler
    logger.info("5")


def e7_disable_by_module():
    logger_a = logger.bind(name="company_a")
    logger_b = logger.bind(name="company_b")

    logger.add(
        Path(dir_here, "company_a.log"),
        filter=partial(filter_by_logger_name, name="company_a"),
    )
    logger.add(
        Path(dir_here, "company_b.log"),
        filter=partial(filter_by_logger_name, name="company_b"),
    )

    logger.info("Hello all")
    logger_a.info("Hello a")
    logger_b.info("Hello b")


# multi_logger_filter_by_name()

def use_in_library():
    from library.logger import logger_a, logger_b
    from library.module import func_a, func_b

    func_a(1)
    func_a(2)
    func_b(1)
    func_b(2)


# use_in_library()


def disable_and_enable_logger():
    from library.logger import logger_a, logger_b
    from library.module import func_a, func_b

    func_a(v=1)
    func_b(v=1)

    logger_a.disable("library")
    func_a(v=2)
    func_b(v=2)
    logger_a.enable("library")

    func_a(v=3)
    func_b(v=3)

    # logger.add(Path(dir_here, "disable_and_enable_test.log"))
    # logger_alice = logger.bind(name="alice")
    #
    # logger_alice.info("1")
    # logger.disable(name="disable_and_enable_logger")
    # logger_alice.info("2")
    # logger.enable(name="disable_and_enable_logger")
    # logger_alice.info("3")


if __name__ == "__main__":
    # e1_simple_logger()
    # e2_format_and_handler()
    # e3_sink()
    # e4_logger_with_name_case1()
    # e4_logger_with_name_case2()
    # e5_filter()
    # e6_disable_and_enable_by_handler()
    disable_and_enable_logger()

    pass
