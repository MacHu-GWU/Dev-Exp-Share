#!/bin/bash
# -*- coding: utf-8 -*-

version="2.7.13"

oldIFS=$IFS
IFS=.
version_numbers=($version)
IFS=$oldIFS

major=${version_numbers[0]}
minor=${version_numbers[1]}
patch=${version_numbers[2]}

echo ${major}
echo ${minor}
echo ${patch}
