#!/bin/bash
# -*- coding: utf-8 -*-

version="2.7.13"

# store the default IFS (delimiter) value
oldIFS=$IFS

# set new delimiter value
IFS=.

# split
version_numbers=($version)
IFS=$oldIFS
echo $version_numbers

major=${version_numbers[0]}
minor=${version_numbers[1]}
patch=${version_numbers[2]}

echo ${major}
echo ${minor}
echo ${patch}
