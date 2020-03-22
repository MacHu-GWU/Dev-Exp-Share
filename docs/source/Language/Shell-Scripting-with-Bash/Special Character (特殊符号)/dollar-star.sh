#!/bin/bash

# $* = all of the positional parameters, seen as a single word
# $* = 将所有的输入参数看成一个整体, 是一个字符串
# 注意: "$*" 必须要被双引号括起来
func() {
    index=1
    for arg in "$*"
    do
        echo "Arg #$index = $arg"
        let "index+=1"
    done

    args=($*)
    index=1
    for arg in "${args[@]}"
    do
        echo "Arg #$index = $arg"
        let "index+=1"
    done
}

func a b c