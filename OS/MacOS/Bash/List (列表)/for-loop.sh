#!/bin/bash

# construct a list this way:
text="a b c d e f g"
words=($text)

# or this:
#words=(a b c d e f g)

# or this:
#words=("a" "b" "c" "d" "e" "f" "g")

for i in "${words[@]}"
do
    echo $i
done
