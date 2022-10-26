# -*- coding: utf-8 -*-

import os
import subprocess

os.environ["EnvName"] = "local"
subprocess.call(["python", "main.py"])
