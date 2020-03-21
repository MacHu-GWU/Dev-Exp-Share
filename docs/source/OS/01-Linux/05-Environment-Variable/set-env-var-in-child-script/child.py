#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.environ["TEST_VAR"] = "this is test var"
# os.putenv("TEST_VAR", "this is test var") # not work either
# os.system('export TEST_VAR="this is test var"') # not work either