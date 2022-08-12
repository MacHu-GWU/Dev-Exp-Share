# -*- coding: utf-8 -*-

"""
我们在设计框架类型的库的时候, 有时候会为一个接口提供一个底层函数, 让用户自己实现自定义的细节,
然后在顶层函数对其进行封装, 增加一些例如, 验证, 打印日志等通用逻辑. 而顶层函数的返回值其实
是和底层函数的返回值是一摸一样的. 但是, 这里实现底层函数的时候的返回类型可能是任何自定义的
类型. 我们如何让顶层函数自动根据底层函数的返回类型, 发现自己实际的返回类型呢?

这个话题实际上就是编程中的泛型.

这里我们来看两个例子. 我们有一个反序列化的类. 他有两个函数, 一个是从字符串中解析数据,
一个是从字节中解析数据. 但是解析出来的数据是什么由用户自己定义. 用户需要继承这个类, 然后
实现对应的方法.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# 首先我们来定义两个类型变量, 分别供 parse_string
T1 = TypeVar("T1")
T2 = TypeVar("T2")


# 这里的 Generic 则是一切的关键, 它是一个 "泛型" 构造器, 定义了一个类里面与泛型有关的变量
# 然后让这个类继承这个 ``Generic[T1, T2, ...]`` 构造器构造出来的父类
# 从而让这个类的子类能够在继承的时候, 通过修改 T1, T2 的值改变里面 TypeHint 的推断
class A(
    ABC,  # 这个是说 A 是一个抽象类.
    # 说明了 A 的子类都会涉及到 2 个类型, 分别用于
    # parse_string 和 parse_bytes 两个函数的返回类型
    Generic[T1, T2],
):
    @abstractmethod
    def _parse_string(self, value: str) -> T1:
        raise NotImplementedError

    def parse_string(self, value: str) -> T1:  # 目前他们都是变量, 具体是什么类型不知道
        try:
            return self._parse_string(value)
        except Exception as e:
            print(f"Failed to parse from string, error: {e}")

    @abstractmethod
    def _parse_bytes(self, value: bytes) -> T2:
        raise NotImplementedError

    def parse_bytes(self, value: bytes) -> T2:
        try:
            return self._parse_bytes(value)
        except Exception as e:
            print(f"Failed to parse from bytes, error: {e}")


class Data1:
    def is_data_1(self):
        return True


class Data2:
    def is_data_2(self):
        return True


# 这里用我们用 Data1, Data2 替换了 T1, T2, 也就是告诉了 parse_string 和 parse_bytes
# 将要返回什么类型了.
class B(A[Data1, Data2]):
    def _parse_string(self, value: str):
        return Data1()

    def _parse_bytes(self, value: str):
        return Data2()


b = B()
b.parse_string("s").is_data_1() # 你输入 b.parse_string("s"). 就能看到 is_data_1 的提示了
b.parse_bytes(b"b").is_data_2()
