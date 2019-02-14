#!/bin/bash

FILE_TO_TEST="$(pwd)/file-dir-exists.sh"
if [ -e ${FILE_TO_TEST} ]; then
    echo "${FILE_TO_TEST} exists!"
else
    echo "${FILE_TO_TEST} NOT exists!"
fi

DIR_TO_TEST="$(pwd)"
if [ -e ${DIR_TO_TEST} ]; then
    echo "${DIR_TO_TEST} exists!"
else
    echo "${DIR_TO_TEST} NOT exists!"
fi