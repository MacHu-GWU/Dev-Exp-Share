# -*- coding: utf-8 -*-

"""
Output::

    execute order()
    execute order()
"""

import os
import pytest


# Arrange
@pytest.fixture
def first_entry() -> str:
    return "a"


# Arrange
@pytest.fixture
def order(first_entry: str) -> list:
    print("execute order()")
    return [first_entry, ]


# below two test reuse same fixture ``order``, which is a mutable object
# but they won't impact each other
def test_string(order: list):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


def test_int(order: list):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
