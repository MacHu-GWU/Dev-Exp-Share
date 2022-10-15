# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch

from my_package.app import print_constant


def test():
    print("do test with mock")
    with patch("my_package.constant.key1", "value111"):
        print_constant()

    print("without mock")
    print_constant()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
