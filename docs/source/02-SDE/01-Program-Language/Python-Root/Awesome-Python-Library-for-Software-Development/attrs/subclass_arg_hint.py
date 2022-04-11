# -*- coding: utf-8 -*-


import attr


@attr.define
class Person:
    name: str = attr.field()


@attr.define
class User(Person):
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(name=data["name"]) # cls's parent arg cannot captured by pycharm


u = User(name="alice")
print(u)
