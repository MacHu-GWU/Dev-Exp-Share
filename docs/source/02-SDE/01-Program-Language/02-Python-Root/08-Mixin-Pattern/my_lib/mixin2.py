# -*- coding: utf-8 -*-

import typing as T

if T.TYPE_CHECKING:
    from .my_class import MyClass


class Mixin2:
    @property
    def b(self: 'MyClass') -> int:
        return self.base + 2
