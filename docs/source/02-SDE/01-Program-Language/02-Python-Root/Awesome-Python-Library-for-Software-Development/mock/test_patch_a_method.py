# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch, PropertyMock

from my_package.app import print_db_table_name


def mock_make_db_table_name(env: str) -> str:
    return f"this_is_mock_table_{env}"


def test():
    print("do test with mock")
    with patch(
        "my_package.config.Config.make_db_table_name",
        wraps=mock_make_db_table_name,
    ):
        print_db_table_name()

    print("without mock")
    print_db_table_name()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
