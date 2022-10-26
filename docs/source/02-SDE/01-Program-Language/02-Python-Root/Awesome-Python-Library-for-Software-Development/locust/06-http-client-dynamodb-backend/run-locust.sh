#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
path_locustfile_py="${dir_here}/locustfile.py"

curl http://127.0.0.1:36737/delete_all
locust -f "${path_locustfile_py}" --headless --users 10 --spawn-rate 10 --stop-timeout 3
