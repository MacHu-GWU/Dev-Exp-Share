# -*- coding: utf-8 -*-

"""
**问题**

在下面的例子中我们用标准库里的 dataclass 定义了一个 class.

作为 class attribute 的 Person.name, 实际上是一个 dataclasses.Field 对象
而作为 instance attribute 的 person.name, 是一个 str 对象

而 IDE 只能根据你在 class 定义中 type hint 推断应该是一个什么类型.

这个问题在几乎所有的 ORM 框架中都存在. 通常我们会手动指定 type hint 的类型为
instance attribute 的类型. 因为毕竟我们用 instance 比较多. 但是还是有很多时候我们需要
将 class / instance attribute 做区分用来做不同的事情. 那么我们如何让 IDE 知道
他们其实是有不同的 type hint 呢?

**解决方案**

1. 在你的 class 定义中, 使用 instance attribute 的类型
2. 在 class 定义之后, 使用 Class.attribute: ${type} 的语法指定 class attribute 的类型
"""

import dataclasses


@dataclasses.dataclass
class Person:
    name: str = dataclasses.field()


Person.name: dataclasses.Field

person = Person(name="alice")

Person.name.
person.name.

def main():
    Person.name.
    person.name.
