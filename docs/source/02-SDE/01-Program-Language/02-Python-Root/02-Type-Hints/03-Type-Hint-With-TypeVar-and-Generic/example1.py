# -*- coding: utf-8 -*-

"""
我们有一个函数, 它的输入参数的类型和输出参数的类型是发生联动的, 但是这个具体的类型是不确定的.
举例来说, 如何用 Typehint 标注输入的参数是 A 类型, 输出的参数也是 A 类型呢?
我们来看下面这个例子. 我们实现了一个类似于 dict.get() 的方法, 不过输入的 dict 可以是任何
mapper, key 和 value 都可以是任何类型.
"""

import typing as T

# 标注一个 key 和 value 的类型
KT = T.TypeVar("KT") # key type
VT = T.TypeVar("VT") # value type

def get_value_by_key(
    # 入参中定义 mapping 的 key 是 KT, value 是 VT
    mapping: T.Mapping[KT, VT],
    # 获得的 key 是 KT
    key: KT,
    # 默认值是 VT
    default: VT
) -> VT: # 返回值是 VT
    try:
        return mapping[key]
    except KeyError:
        return default

# 如果 Type 正确, 那么 IDE 可以提示以下方法
# int.bit_count()
# str.split()

# Type 正确
v = get_value_by_key(mapping={"a": 1, "b": 2}, key="a", default=0)
# 可以提示 bit_count 方法
v.bit_count()

# Type 正确
v = get_value_by_key(mapping={1: "a", 2: "b"}, key=1, default="c")
# 可以提示 split 方法
v.split()

# Type 不正确, IDE 提示 default="c" 不对
v = get_value_by_key(mapping={"a": 1, "b": 2}, key="a", default="c")
