#!/bin/bash

if [ -n "${BASH_SOURCE}" ]
then
    dir_py="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_py="$( cd "$(dirname "$0")" ; pwd -P )"
fi

echo "the ./bin/py dir is: "$(basename ${dir_py})""