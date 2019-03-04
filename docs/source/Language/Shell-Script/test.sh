#!/bin/bash
# -*- coding: utf-8 -*-

py_version='2.7.13'

oldIFS=$IFS
IFS=.

version_numbers=($py_version)
major=${version_numbers[0]}
minor=${version_numbers[1]}

IFS=$oldIFS
version_short="$major.$minor"

python='python'${version_short}
pip='pip'${version_short}

echo ${pip}