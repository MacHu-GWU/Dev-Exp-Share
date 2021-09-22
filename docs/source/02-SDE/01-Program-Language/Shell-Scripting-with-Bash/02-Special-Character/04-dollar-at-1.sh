#!/bin/bash
# -*- coding: utf-8 -*-

# try ``bash dollar-at-2.sh 1 2 3``

# $@ = all of the positional parameters, but each parameter is a quoted string
# $@ = 将所有的输入参数看成一个列表
# 注意: "$@" 必须要被双引号括起来

index=1
for arg in "$@"
do
echo "Arg #${index} = $arg"
let index+=1
done
