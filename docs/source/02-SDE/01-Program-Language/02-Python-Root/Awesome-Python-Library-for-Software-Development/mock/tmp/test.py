# -*- coding: utf-8 -*-

import os
import sys
import pytest
from my_lib import my_lib_module
from unittest.mock import patch
from my_main_package import main

def fake_my_function(*args, **kwargs):
    sys.exit(5)

def test_main(*args):
    with patch.object(
        my_lib_module,
        "my_function",
        wraps=fake_my_function,
    ) as mock_get_status:
        with 
        main()
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])