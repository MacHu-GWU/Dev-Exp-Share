# -*- coding: utf-8 -*-

import time
from rich.console import Console

console = Console()


with console.status("Working..."):
    for ith in range(1, 10+1):
        print(f"{ith} try ...")
        time.sleep(1)
