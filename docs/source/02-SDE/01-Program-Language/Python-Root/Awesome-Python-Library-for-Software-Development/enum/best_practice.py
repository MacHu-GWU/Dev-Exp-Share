# -*- coding: utf-8 -*-

import enum
from pytest import raises


class Color(enum.Enum):
    red = 1
    blue = 2


# 这是主要的访问 Enum 的方式, 可以理解为这是一个 Enum 的实例
_ = Color.red

# Enum 的实例是一个 Enum 的 instance
assert isinstance(Color.red, Color)

# Enum 是 单例 模式. 可以用 is
assert Color.red is Color.red

# 可以用 in 来检查是否在 Enum 中
assert Color.red in Color

# 访问 name
assert Color.red.name == "red"

# 访问 Value
assert Color.red.value == 1

# 根据 name 访问
assert Color["red"] is Color.red

# 根据 value 访问
assert Color(1) is Color.red

# name 不存在会报 KeyError
with raises(KeyError):
    _ = Color["green"]

# value 不存在会报 ValueError
with raises(ValueError):
    _ = Color(3)
