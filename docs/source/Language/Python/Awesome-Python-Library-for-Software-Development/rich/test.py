# -*- coding: utf-8 -*-

from rich import print
from rich import pretty
from rich import inspect
from rich.console import Console

# print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())


# pretty.install()

# print(locals())

# print([False, True, None, 3.14, "Hello World! " * 5, {"foo": "bar"}])
# print(inspect(str, methods=True))
# print(inspect([1,2,3]))

console = Console()
console.print("Hello", "World!", style="bold red")