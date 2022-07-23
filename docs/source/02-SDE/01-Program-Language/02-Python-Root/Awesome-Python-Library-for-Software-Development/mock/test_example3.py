# -*- coding: utf-8 -*-

"""
Replace a specific function with your own function.
"""

import os
import pytest
from my_module import get_status_api


# the fake function to replace the not implemented get_status
def fake_get_status(name: str) -> str:
    return f"status of {name}: BAD"


def test_1(mocker):
    mocker.patch("my_module.get_status", wraps=fake_get_status)
    assert get_status_api(name="Alice") == "status of Alice: BAD"


def test_2(mocker):
    with pytest.raises(NotImplementedError):
        get_status_api(name="Alice")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
