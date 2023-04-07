# -*- coding: utf-8 -*-

import os
import pytest
import shutil
from pathlib import Path


def test(tmp_path: Path):
    # before
    print(tmp_path) # tmp_path is a dir, not a file
    path = tmp_path.joinpath("test.txt")
    path.write_text("hello")

    # test
    assert path.read_text() == "hello"

    # after
    # this is not necessary, pytest automatically clean up and keep
    # the last three tmp path
    shutil.rmtree(tmp_path)


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
