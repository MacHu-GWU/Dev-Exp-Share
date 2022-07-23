# -*- coding: utf-8 -*-

"""
You can define a function with mocker pytest fixture, define your mock
logic in that function, and call that function when needed in your test.
"""

import os
import pytest
from my_module import get_status_api


# the fake function to replace the not implemented get_status
def fake_get_status(name: str) -> str:
    return f"status of {name}: BAD"


# implement your mock logic
def do_patch(mocker):
    mocker.patch("my_module.get_status", wraps=fake_get_status)


def test_1(mocker):
    do_patch(mocker)  # use for test 1
    assert get_status_api(name="Alice") == "status of Alice: BAD"


def test_2(mocker):
    do_patch(mocker)  # use for test 2
    assert get_status_api(name="Alice") == "status of Alice: BAD"


def test_3(mocker):
    # not use for test 3
    with pytest.raises(NotImplementedError):
        get_status_api(name="Alice")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
