# -*- coding: utf-8 -*-

from rich.tree import Tree
from rich import print

tree = Tree("Rich Tree")
tree.add("foo")
tree.add("bar")
print(tree)

baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)
