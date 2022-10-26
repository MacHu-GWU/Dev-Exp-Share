# -*- coding: utf-8 -*-

"""
This example shows the built-in environment variable
"""

import os
import pytest


def test():
    assert "PYTEST_CURRENT_TEST" in os.environ
    print(os.environ["PYTEST_CURRENT_TEST"])


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
