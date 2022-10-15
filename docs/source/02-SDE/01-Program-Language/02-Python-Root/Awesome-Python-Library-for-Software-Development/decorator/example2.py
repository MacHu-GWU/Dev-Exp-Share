# -*- coding: utf-8 -*-

import decorator


@decorator.decorator
def before_and_after(func, *args, **kwargs):
    print("before")
    result = func(*args, **kwargs)
    print("after")
    return result


@before_and_after
def add_two(first: int, second: int) -> int:
    return first + second


# Looks like in PyCharm the signature not working
result = add_two(first=1, second=2)
assert result == 3
