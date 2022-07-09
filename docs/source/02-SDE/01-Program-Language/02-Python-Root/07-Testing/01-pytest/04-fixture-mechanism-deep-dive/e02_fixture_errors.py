# -*- coding: utf-8 -*-

import os
import pytest


@pytest.fixture
def order():
    return []


@pytest.fixture
def append_first(order):
    print("run append_first")
    # raise ValueError
    order.append(1)


@pytest.fixture
def append_second(order, append_first):
    print("run append_second")
    order.extend([2])


@pytest.fixture(autouse=True)
def append_third(order, append_second):
    print("run append_third")
    order += [3]


def test_order(order):
    assert order == [1, 2, 3]


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
