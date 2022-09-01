# -*- coding: utf-8 -*-

import attr


@attr.define(frozen=True)
class Base:
    name: str = attr.field()
    mapper: dict = attr.field(factory=dict, hash=False)

    @property
    def id(self) -> str:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.id)


@attr.define
class User(Base):
    @property
    def id(self) -> str:
        return self.name


u1 = User(name="alice")
u1.mapper["a"] = 1

u2 = User(name="alice")
u2.mapper["b"] = 2

print(hash(u1), hash(u2))
