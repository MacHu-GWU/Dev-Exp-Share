# -*- coding: utf-8 -*-

from rich.traceback import install
from rich.console import Console

install()
console = Console()

def do_something():
    return 1 + "a"

try:
    do_something()
except:
    console.print_exception()
