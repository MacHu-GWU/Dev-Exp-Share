# -*- coding: utf-8 -*-


from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .model1 import Model1


class Model2:
    def __init__(self, model2_attr: str, model1: Optional['Model1'] = None):
        self.model2_attr = model2_attr
        self.model1 = model1

    def to_dict(self) -> dict:
        d = dict(model2_attr=self.model2_attr)
        if self.model1 is None:
            d["model1"] = None
        else:
            d["model1"] = self.model1.to_dict()
        return d

    def cal_with(self, model1):
        pass
