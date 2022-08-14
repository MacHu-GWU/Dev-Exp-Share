# -*- coding: utf-8 -*-

"""
"""

import os
import pytest
from unittest.mock import patch

import my_module
from my_module import get_status_api


def test():
    with patch.object(my_module, "get_status", return_value="good"):
        assert get_status_api(name="alice") == "good"

    with patch.object(my_module, "get_status", return_value="bad"):
        assert get_status_api(name="bob") == "bad"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
