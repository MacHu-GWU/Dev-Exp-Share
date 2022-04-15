# -*- coding: utf-8 -*-

import os
import time
from multiprocessing import Pool

print(f"you have {os.cpu_count()} CPU core")


def func(name):
    for i in range(10):
        time.sleep(1)  # Simulate that this function takes long to complete
        print(f"{i}th call, hello {name}!")
    return f"hello {name}"


# multiprocessing.Pool has to use under if __name__ == "__main__":
# it is like run this script with different parameter 8 times
if __name__ == "__main__":
    args = list("abcdefghijklmnopqrstuvwxyz")
    with Pool(processes=12) as pool:
        results = pool.map(func, args)
        print(results)
