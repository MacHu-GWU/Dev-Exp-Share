#!/bin/bash

# test if match any
if [ $(ls /bin | grep bash) ]; then
    echo "bash installed"
fi

# test if the match is exactly
if [ $(ls /bin | grep bash) == "bash" ]; then
    echo "bash installed"
fi
