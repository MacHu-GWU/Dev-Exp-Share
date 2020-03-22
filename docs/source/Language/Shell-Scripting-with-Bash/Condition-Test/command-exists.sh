#!/bin/bash

CMD_TO_TEST="bash"
if ! [ -x "$(command -v ${CMD_TO_TEST})" ]; then
    echo "Error: ${CMD_TO_TEST} is not installed." >&2
    exit 1
else
    echo "${CMD_TO_TEST} at: $(command -v ${CMD_TO_TEST})"
fi