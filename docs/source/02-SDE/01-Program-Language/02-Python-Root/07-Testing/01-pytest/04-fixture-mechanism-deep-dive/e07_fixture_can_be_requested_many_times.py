# -*- coding: utf-8 -*-

"""
Output::

    execute order()
    execute first_entry()
    execute append_first()
    append_first = None
    order = ['a']
    first_entry = 'a'
"""

import os
import pytest


# Arrange
@pytest.fixture
def first_entry():
    print("execute first_entry()")
    return "a"


# Arrange
@pytest.fixture
def order():
    print("execute order()")
    return []


# Act
@pytest.fixture
def append_first(order, first_entry):
    print("execute append_first()")
    return order.append(first_entry)


def test_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
    print(f"append_first = {append_first!r}")
    print(f"order = {order!r}")
    print(f"first_entry = {first_entry!r}")



if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
