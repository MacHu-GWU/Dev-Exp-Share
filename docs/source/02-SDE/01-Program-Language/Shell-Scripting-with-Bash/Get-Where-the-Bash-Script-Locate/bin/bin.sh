#!/bin/bash

if [ -n "${BASH_SOURCE}" ]
then
    dir_bin="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
fi

echo "the ./bin dir is: "$(basename ${dir_bin})""

bash ${dir_bin}/py/py.sh
source ${dir_bin}/py/py.sh