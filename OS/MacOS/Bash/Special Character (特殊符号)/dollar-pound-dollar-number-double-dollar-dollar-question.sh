#!/bin/bash

my-func1() {
    echo $#             # number of argument
    echo $0             # script file
    echo $1 $2 $3       # first, second, third argument
    echo $$             # process id
    echo $?             # exit code
}

my-func1 a b c d e f g
