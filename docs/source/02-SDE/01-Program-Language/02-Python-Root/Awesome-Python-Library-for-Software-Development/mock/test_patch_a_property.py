# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch, PropertyMock

from my_package.app import print_config


def test():
    print("do test with mock")
    with patch(
        "my_package.config.Config.project_name",
        new_callable=PropertyMock,
        return_value="my-project-dev",
    ):
        print_config()

    print("without mock")
    print_config()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
