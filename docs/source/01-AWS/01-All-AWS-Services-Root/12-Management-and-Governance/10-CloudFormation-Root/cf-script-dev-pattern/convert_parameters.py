# -*- coding: utf-8 -*-

import json

def convert_json_file_to_paramters_option_for_cloudformation_deploy_cmd(json_file):
    with open(json_file, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))

    chunks = list()
    for key, value in data.items():
        arg = '{}={}'.format(key, value)
        chunks.append(arg)

    return " ".join(chunks)


if __name__ == "__main__":
    import sys

    json_file = sys.argv[1]
    print(convert_json_file_to_paramters_option_for_cloudformation_deploy_cmd(json_file))
