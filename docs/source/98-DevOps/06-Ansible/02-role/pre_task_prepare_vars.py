# -*- coding: utf-8 -*-

import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
vars_json_file = os.path.join(HERE, "vars.json")


vars_data = {
    "message": "Bob"
}

with open(vars_json_file, "w") as f:
    f.write(json.dumps(vars_data))