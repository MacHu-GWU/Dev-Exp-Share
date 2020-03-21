#!/bin/bash

python_output_data=$(python child.py)
TEST_VAR=$(echo $python_output_data | jq '.TEST_VAR' -r)
echo $TEST_VAR
