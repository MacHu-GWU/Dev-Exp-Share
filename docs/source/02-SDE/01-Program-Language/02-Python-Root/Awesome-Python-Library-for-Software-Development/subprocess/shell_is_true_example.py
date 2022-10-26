# -*- coding: utf-8 -*-

import subprocess

print("before")
subprocess.run(["jq", "--version"], shell=True)
print("after")