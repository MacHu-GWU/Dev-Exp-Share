#!/bin/bash

# ... > filename
# redirect output of command ... to a file, will overwrite the content
ls > test.txt

echo "a" >> test.txt
echo "b" >> test.txt
echo "c" >> test.txt
