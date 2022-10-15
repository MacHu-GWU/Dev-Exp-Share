# -*- coding: utf-8 -*-

import os
import pytest
from datetime import datetime, timezone
from unittest.mock import patch

from my_package.app import print_now


def test():
    print("do test with mock")
    with patch(
        "my_package.helpers.utc_now",
        return_value=datetime(2000, 1, 1, tzinfo=timezone.utc),
    ):
        print_now()

    print("without mock")
    print_now()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
