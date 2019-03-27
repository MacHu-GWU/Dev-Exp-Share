# -*- coding: utf-8 -*-

import os
import json

env_file = os.path.join(os.path.expanduser("~"), ".env.json")


def load_env_json_file():
    with open(env_file, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    for key, value in data.items():
        os.environ[key] = str(value)
