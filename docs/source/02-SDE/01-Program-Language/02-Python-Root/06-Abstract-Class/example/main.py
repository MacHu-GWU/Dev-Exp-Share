# -*- coding: utf-8 -*-

from model1 import Model1
from model2 import Model2

m1 = Model1(model1_attr="m1")
m2 = Model2(model2_attr="m2")
m1.model2 = m2
m2.model1 = m1

print(m1.to_dict())
