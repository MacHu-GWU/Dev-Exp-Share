# -*- coding: utf-8 -*-

import sys
import json


def run() -> dict:
    print("start")
    print("done")
    return {
        "python": sys.executable,
        "weird_string": "\\a\nb\tc\"d'e@f#g:h/i"
    }


if __name__ == "__main__":
    print(json.dumps(run()))
