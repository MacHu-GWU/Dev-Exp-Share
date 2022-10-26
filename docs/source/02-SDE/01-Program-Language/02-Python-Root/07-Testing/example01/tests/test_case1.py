# -*- coding: utf-8 -*-

import os
import pytest


def test():
    from lib import __version__
    print(os.environ["PYTEST_CURRENT_TEST"])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
