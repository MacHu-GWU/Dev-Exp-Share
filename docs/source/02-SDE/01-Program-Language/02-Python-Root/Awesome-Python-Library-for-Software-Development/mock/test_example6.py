# -*- coding: utf-8 -*-

import os
import pytest
import my_module
from my_module import Order
from unittest.mock import patch

def test():
    order = Order(order_id="oid-1")

    with patch.object(my_module, "run_sql", return_value=1):
        print(order.n_items)

    with patch.object(my_module, "run_sql", return_value=2):
        print(order.n_items)



if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
