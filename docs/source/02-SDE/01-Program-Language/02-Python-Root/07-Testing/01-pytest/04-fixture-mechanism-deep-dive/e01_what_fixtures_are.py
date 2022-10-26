# -*- coding: utf-8 -*-

"""
Fixture 本质是一个 callable 的函数. 你可以用 ``@pytest.fixture`` decorator
将函数注册为一个 Fixture, 之后你就可以将其像变量一样使用.

Fixture 可以使用其他的 fixture.

Output::

    execute my_fruit()
    execute fruit_basket(my_fruit)
"""

import os
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    print("execute my_fruit()")
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    print("execute fruit_basket(my_fruit)")
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
