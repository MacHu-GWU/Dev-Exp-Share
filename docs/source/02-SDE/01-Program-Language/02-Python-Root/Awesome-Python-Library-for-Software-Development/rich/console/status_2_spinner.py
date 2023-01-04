# -*- coding: utf-8 -*-

import time
from rich.console import Console

console = Console()

# Run this ``python -m rich.spinner`` to see the available choices for ``spinner``
with console.status("Working...", spinner="line"):
    for ith in range(1, 10+1):
        print(f"{ith} try ...")
        time.sleep(1)
