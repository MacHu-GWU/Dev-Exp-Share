# -*- coding: utf-8 -*-

import dataclasses


# ------------------------------------------------------------------------------
# Method 1, 双向 reference
#
# 优点:
#
# - 简洁, 容易实现, 比较直观
#
# 缺点:
#
# - 因为循环引用, garbage collect 永远不会回收
# - 因为循环引用, 对里面的值进行修改要特别小心, 因为所有的对象都是 mutable 的, 牵一发而动全身
#
# 使用条件: 数据只会被创建有限次数, 不会不断的创建很多导致内存溢出. 对象一旦生成, 就不会被修改.
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Child:
    child_attribute: str = dataclasses.field()
    parent: "Parent" = dataclasses.field(init=False)


@dataclasses.dataclass
class Parent:
    parent_attribute: str = dataclasses.field()
    child: Child = dataclasses.field()

    def __post_init__(self):
        self.child.parent = self


parent = Parent(
    parent_attribute="this is parent",
    child=Child(
        child_attribute="this is child",
    ),
)

print(parent.child.parent.parent_attribute)


# ------------------------------------------------------------------------------
# Method 2, 在初始化时将 parent 中所需的值传给 child 的 constructor
#
# 优点:
#
# - 简洁, 对 child 和 parent 的代码没有侵入性, 负面效果比较小
#
# 缺点:
#
# - 只能传属性, 无法从 child 调用 parent 的方法
# - 实现起来麻烦, 需要在 constructor 中写很多代码
#
# 使用条件:
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Child:
    child_attribute: str = dataclasses.field()
    parent_attribute: str = dataclasses.field()


@dataclasses.dataclass
class Parent:
    parent_attribute: str = dataclasses.field()
    child: Child = dataclasses.field()


parent_attribute = "this is parent"
parent = Parent(
    parent_attribute=parent_attribute,
    child=Child(
        child_attribute="this is child",
        parent_attribute=parent_attribute,
    ),
)

print(parent.child.parent_attribute)


# ------------------------------------------------------------------------------
# Method 3, 凡是在 child 需要访问 parent 的地方, 都构造一个方法
#
# 优点:
#
# - 完全符合函数式编程的思想, child 和 parent 完全解耦, child 只需要知道 parent 的接口就可以了
#
# 缺点:
#
# - 相当于要把 parent 中所有的 attribute 和 method 在 child 中都实现一遍, 代码量大
#
# 使用条件: 需要严格遵守函数式编程的规范. parent 和 child 两个模块是由不同的人维护的, 两个模块之间的耦合度很低.
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Child:
    child_attribute: str = dataclasses.field()

    def get_parent_attribute(self, parent: "Parent") -> str:
        return parent.parent_attribute


@dataclasses.dataclass
class Parent:
    parent_attribute: str = dataclasses.field()
    child: Child = dataclasses.field()


parent = Parent(
    parent_attribute=parent_attribute,
    child=Child(
        child_attribute="this is child",
    ),
)
print(parent.child.get_parent_attribute(parent))
