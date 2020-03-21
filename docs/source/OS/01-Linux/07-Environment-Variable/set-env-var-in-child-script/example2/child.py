#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

if __name__ == "__main__":
    os.environ["TEST_VAR"] = "this is test var"

    data = {"TEST_VAR": os.environ["TEST_VAR"]}
    print(json.dumps(data))
