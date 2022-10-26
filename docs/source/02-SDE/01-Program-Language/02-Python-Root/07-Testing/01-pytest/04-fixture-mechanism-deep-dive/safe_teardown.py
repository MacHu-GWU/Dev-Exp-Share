# -*- coding: utf-8 -*-

import os
import pytest

path_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")


@pytest.fixture
def file():
    print("create file")
    with open(path_file, "w") as f:
        f.write("")

    print("yield file")
    f = open(path_file, "a")
    raise Exception
    yield f

    print("close and delete file")
    f.close()
    os.remove(path_file)


def test(file):
    file.write("log 1")
    file.write("log 2")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
