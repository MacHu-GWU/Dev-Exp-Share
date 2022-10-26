# -*- coding: utf-8 -*-

"""
Use mock without pytest
"""

import pytest
import my_module
from my_module import get_status_api
from unittest.mock import patch


# the fake function to replace the not implemented get_status
def fake_get_status(name: str) -> str:
    return f"status of {name}: BAD"


# temporarily replace your function with a fake function
with patch.object(my_module, "get_status", wraps=fake_get_status) as mock_get_status:
    print(get_status_api(name="Alice"))

with pytest.raises(NotImplementedError):
    get_status_api(name="Alice")
