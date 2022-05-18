# -*- coding: utf-8 -*-

"""
Share object Example
"""

import os
import random
from typing import List
from mpire import WorkerPool

# MacOS high sierra disable multi process by defaultz
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

cpu_count = os.cpu_count()
print(f"you have {cpu_count} CPU core")


class Container:
    def __init__(self):
        self.count = 0


def func1(container: Container):
    i = random.randint(1, 100)
    container.count += i
    return i


container = Container()

kwargs: List[dict] = [{} for _ in range(10)]

# from https://slimmer-ai.github.io/mpire/usage/workerpool/shared_objects.html#copy-on-write-alternatives
# it says that For ``threading`` these shared objects are readable and writable without copies being made.
# which is our use case here
with WorkerPool(
    n_jobs=cpu_count,
    shared_objects=container,
    start_method="threading",
) as pool:
    results = pool.map(func1, kwargs)
    print(f"all returned results = {results}, sum = {sum(results)}")
    print(f"count = {container.count}")


def func2(count: int):
    i = random.randint(1, 100)
    count += i
    return i


count = 0  # this won't work, int is immutable
with WorkerPool(
    n_jobs=cpu_count,
    shared_objects=count,
    start_method="threading",
) as pool:
    results = pool.map(func2, kwargs)
    print(f"all returned results = {results}, sum = {sum(results)}")
    print(f"count = {count}")
