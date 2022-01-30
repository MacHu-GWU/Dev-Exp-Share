# -*- coding: utf-8 -*-

"""
概念:

- Iterate: 迭代, 和循环是一样的概念, 也就是 for i in object 的行为.
- Iterator: 迭代器, 也就是支持 for i in object 的行为, 内部调用 __next__ 方法.
    - 一定要有 __iter__ 方法, 并且通常是返回他自己, 也就是 def __iter__(self): return self
    - 一定要有 __next__ 方法, 返回下一个 yield 的元素, 最后要抛出 StopIteration 异常以结束
- Iterable: 可迭代对象, 也就是支持 for i in object 的行为, 内部线用 __iter__ 返回
    一个 迭代器, 然后再调用 __next__ 方法.
    - 一定要有 __iter__ 方法, 但不需要有__next__ 方法

总之, 只要有 for i in object 的语法, object.__iter__ 方法就会被调用.
"""

from typing import Iterable, Iterator


def example1():
    iterable = range(3)

    for i in iterable:
        print(i)

    iterator = iter(iterable)

    for i in iterator:
        print(i)

    print(f"iterable is Iterable: {isinstance(iterable, Iterable)}")
    print(f"iterable is Iterator: {isinstance(iterable, Iterator)}")

    print(f"iterator is Iterable: {isinstance(iterator, Iterable)}")
    print(f"iterator is Iterator: {isinstance(iterator, Iterator)}")


def example2():
    class MyIterator:
        def __init__(self, n):
            self.max = n - 1
            self.now = -1

        def __iter__(self):
            print("iterator's __iter__ is called")
            return self

        def __next__(self):
            print("iterator's __next__ is called")
            self.now += 1
            if self.now <= self.max:
                return self.now
            else:
                raise StopIteration

    class MyIterable:
        def __init__(self, k):
            self.k = k

        def __iter__(self):
            print("iterable's __iter__ is called")
            return MyIterator(self.k)

    my_iterable = MyIterable(5)
    for i in my_iterable:
        print(i)

    my_iterator = iter(my_iterable)
    for i in my_iterator:
        print(i)


if __name__ == "__main__":
    # example1()
    # example2()
    pass
