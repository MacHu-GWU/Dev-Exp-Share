# -*- coding: utf-8 -*-

from bidict import bidict

element_by_symbol = bidict({"H": "hydrogen"})
print(element_by_symbol["H"])
print(element_by_symbol.inverse["hydrogen"])

bidct = bidict({"a": 1, "b": 1, "c": 1})
print(bidct["a"])
print(bidct.inverse[1])
