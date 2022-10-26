# -*- coding: utf-8 -*-
# content of a.py
# this only works in Python3.7+

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from avoid_cyclic_import_b import B


class A:
    def __init__(self, b: 'B'):
        self.b = b

    def method(self, b: B):
        return b
