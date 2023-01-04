# -*- coding: utf-8 -*-

import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(os.getcwd())
print(directory)
print(Columns(directory))
