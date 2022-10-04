# -*- coding: utf-8 -*-
# content of ``my_package/app.py``

from . import constant

def print_constant():
    print(f"constant.key1 = {constant.key1}")
    print(f"constant.key2 = {constant.key2}")
    print(f"constant.key3 = {constant.key3}")
