# -*- coding: utf-8 -*-

"""
Patch a function with a fixed return value
"""

import os
import pytest
from my_module import get_status, get_status_api


def test_1(mocker):
    # this would work
    mocker.patch("my_module.get_status", return_value="status of Alice: GOOD")
    assert get_status_api(name="Alice") == "status of Alice: GOOD"

    # don't use that directly
    # print(get_status(name="BOB"))


def test_2(mocker):
    # not work, the patch context is not available
    with pytest.raises(NotImplementedError):
        get_status_api(name="Alice")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
