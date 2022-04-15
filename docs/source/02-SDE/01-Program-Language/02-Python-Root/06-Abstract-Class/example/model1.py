from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .model2 import Model2


class Model1:
    def __init__(self, model1_attr: str, model2: Optional['Model2'] = None):
        self.model1_attr = model1_attr
        self.model2 = model2

    def to_dict(self) -> dict:
        d = dict(model1_attr=self.model1_attr)
        if self.model2 is None:
            d["model2"] = None
        else:
            d["model2"] = self.model2.to_dict()
        return d

    # def cal_with(self, model2):
    #     pass
