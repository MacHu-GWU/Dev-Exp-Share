# -*- coding: utf-8 -*-

"""
ref: https://docs.python.org/3/library/enum.html
"""

import enum


class Color(enum.Enum):
    Red = 1
    Blue = 2
    Yellow = 3


def test_api():
    assert Color.Red.value == 1
    assert Color["Red"].value == 1
    assert Color(1).value == 1
    assert isinstance(Color.Red , Color)

    assert [color.name for color in Color] == ["Red", "Blue", "Yellow"]
    assert [color.value for color in Color] == [1, 2, 3]


def test_unique():
    try:
        @enum.unique
        class StatusCode(enum.Enum):
            success = 1
            failed = 0
            complete = 1 # duplicate value raises ValueError
    except ValueError:
        pass
    except:
        raise



if __name__ == "__main__":
    test_api()
    test_unique()
