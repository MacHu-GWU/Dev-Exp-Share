#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_venv="${dir_here}/venv"

# Glue 0.9 = Python2.7, Spark 2.2.1
# Glue 1.0 = Python3.6, Spark 2.4.3
# Glue 2.0 = Python3.7, Spark 2.4.3
# Glue 3.0 = Python3.7, Spark 3.1.1
virtualenv -p python3.7 "${dir_venv}"
