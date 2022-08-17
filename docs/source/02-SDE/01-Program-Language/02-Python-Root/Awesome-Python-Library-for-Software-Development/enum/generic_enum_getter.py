# -*- coding: utf-8 -*-

"""
Enum 标准库被引入时还没有 typing. 很多时候你的 enum.Enum.value 是有类型的. 而如果你
用自带的迭代器等方法返回枚举数据的时候, 你就失去了 type hints.

本例给出了一个解决方案, 可以轻易在不侵入已有代码的情况下, 拥有更加友好的 type hint.
"""

import typing as T
import enum

ENUM = T.TypeVar("ENUM")
ENUM_VALUE = T.TypeVar("ENUM_VALUE")


class EnumGetter(T.Generic[ENUM, ENUM_VALUE]):
    enum_class: ENUM = None

    @classmethod
    def get_name(cls, key: T.Union[str, enum.Enum]) -> str:
        if isinstance(key, str):
            return key
        else:
            return key.name

    @classmethod
    def get_enum(cls, key: T.Union[str, enum.Enum]) -> ENUM:
        if isinstance(key, str):
            return cls.enum_class[key]
        else:
            return key

    @classmethod
    def get_value(cls, key: T.Union[str, enum.Enum]) -> ENUM_VALUE:
        if isinstance(key, str):
            return cls.enum_class[key].value
        else:
            return key.value

    @classmethod
    def iter_keys(cls) -> T.List[str]:
        return [
            enum.name
            for enum in cls.enum_class
        ]

    @classmethod
    def iter_enum(cls) -> T.List[ENUM]:
        return list(cls.enum_class)

    @classmethod
    def iter_values(cls) -> T.List[ENUM_VALUE]:
        return [
            enum.value
            for enum in cls.enum_class
        ]

    @classmethod
    def iter_items(cls) -> T.List[T.Tuple[str, ENUM, ENUM_VALUE]]:
        return [
            (enum.name, enum, enum.value)
            for enum in cls.enum_class
        ]


class NameEnum(enum.Enum):
    alice = "Alice"
    bob = "Bob"


class NameGetter(EnumGetter[NameEnum, str]):
    enum_class = NameEnum


assert NameGetter.get_name("alice") == "alice"
assert NameGetter.get_name(NameEnum.alice) == "alice"

assert NameGetter.get_enum("alice") is NameEnum.alice
assert NameGetter.get_enum(NameEnum.alice) is NameEnum.alice

assert NameGetter.get_value("alice") == "Alice"
assert NameGetter.get_value(NameEnum.alice) == "Alice"

assert NameGetter.iter_keys()[0] == "alice"
assert NameGetter.iter_enum()[0] is NameEnum.alice
assert NameGetter.iter_values()[0] == "Alice"

assert NameGetter.iter_items()[0][0] == "alice"
assert NameGetter.iter_items()[0][1] is NameEnum.alice
assert NameGetter.iter_items()[0][2] == "Alice"
