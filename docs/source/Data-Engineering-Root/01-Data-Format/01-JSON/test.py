# -*- coding: utf-8 -*-

from rich import print
from flatten_json import flatten
# from flattentool import flatten

def e01():
    data = {
        "data": {
            "k1": 1,
            "k2": 2
        },
        "tags": [
            {"key": "k1", "value": "v1"},
            {"key": "k2", "value": "v2"}
        ],
        "2d_array": [
            [1, 2],
            [3, 4]
        ]
    }
    print(flatten(data))


if __name__ == "__main__":
    e01()
    pass
