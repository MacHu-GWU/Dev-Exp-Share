# -*- coding: utf-8 -*-
# content of b.py
# this only works in Python3.7+

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from avoid_cyclic_import_a import A


class B:
    def __init__(self, a: 'A'):
        self.a = a

    def method(self, a: A):
        return a
