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


def func(numbers: List[int], a: int, b: int):
    res = a + b
    numbers.append(res)
    return res


numbers: List[int] = list()
kwargs: List[dict] = [
    {
        "a": 1,
        "b": 2,
    }
    for _ in range(10)
]

# from https://slimmer-ai.github.io/mpire/usage/workerpool/shared_objects.html#copy-on-write-alternatives
# it says that For ``threading`` these shared objects are readable and writable without copies being made.
# which is our use case here
with WorkerPool(
    n_jobs=cpu_count,
    shared_objects=numbers,
    start_method="threading",
) as pool:
    results = pool.map(func, kwargs)
    print(f"all returned results = {results}, sum = {sum(results)}")
    print(f"number of elements in numbers: {len(numbers)}")
    print(f"sum of the numbers: {sum(numbers)}")
