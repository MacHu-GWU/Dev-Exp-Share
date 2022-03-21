# -*- coding: utf-8 -*-

"""
A simple implementation of depth first search / width first search::

    t
    |--- t1
        |--- t11
        |--- t12
    |--- t2
        |--- t21
        |--- t22

    # depth first search result
    t11, t12, t1, t21, t22, t2, t

    # width first search result
    t, t1, t2, t11, t12, t21, t22
"""

from typing import List


class Node:
    def __init__(self, name: str, children: List['Node'] = None):
        self.name = name
        if children is None:
            children = list()
        self.children = children

    def __repr__(self):
        return f"'{self.name}'"


t11 = Node("t11")
t12 = Node("t12")
t21 = Node("t21")
t22 = Node("t22")
t1 = Node("t1", [t11, t12])
t2 = Node("t2", [t21, t22])
t = Node("t", [t1, t2])


def depth_first_search(node: Node):
    for n in node.children:
        yield from depth_first_search(n)
    yield node


def width_first_search(node: Node, _is_root=True):
    if _is_root:
        yield node
    for n in node.children:
        yield n
    for n in node.children:
        yield from width_first_search(n, _is_root=False)


print(list(depth_first_search(t)))  # ['t11', 't12', 't1', 't21', 't22', 't2', 't']
print(list(width_first_search(t)))  # ['t', 't1', 't2', 't11', 't12', 't21', 't22']
