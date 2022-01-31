# -*- coding: utf-8 -*-

import os
import time
from mpire import WorkerPool

print(f"you have {os.cpu_count()} CPU core")


def func(name):
    for i in range(3):
        time.sleep(1)  # Simulate that this function takes long to complete
        print(f"{i}th call, hello {name}!")
    return f"hello {name}"


args = list("abcdefghijklmnopqrstuvwxyz")
kwargs = [{"name": arg} for arg in args]

with WorkerPool(n_jobs=12) as pool:
    results = pool.map(func, kwargs, enable_insights=True)
    print(results)
    print(pool.get_insights())
