# -*- coding: utf-8 -*-
# content of: mixin1.py

import typing as T

if T.TYPE_CHECKING:
    from .my_class import MyClass

class Mixin1:
    @property
    def a(self: 'MyClass') -> int:
        return self.base + 1
