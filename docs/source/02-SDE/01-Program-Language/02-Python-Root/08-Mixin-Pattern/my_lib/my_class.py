# -*- coding: utf-8 -*-

from .base import MyClass as Base
from .mixin1 import Mixin1
from .mixin2 import Mixin2


class MyClass(
    Base,
    Mixin1,
    Mixin2,
):
    pass
