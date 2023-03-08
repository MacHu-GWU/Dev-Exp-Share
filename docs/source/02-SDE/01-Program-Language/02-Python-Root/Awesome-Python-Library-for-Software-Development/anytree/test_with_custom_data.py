# -*- coding: utf-8 -*-

import dataclasses
from anytree import (
    Node,
    RenderTree,
)

@dataclasses.dataclass
class NodeMixin:
    def __str__(self):
        return self.name

@dataclasses.dataclass
class Department(NodeMixin):
    name: str = dataclasses.field()

@dataclasses.dataclass
class Group(NodeMixin):
    name: str = dataclasses.field()

root = Node(Department(name="root"))

hr = Node(Department(name="hr"), parent=root)
hr_planning = Node(Group(name="planning"), parent=hr)
hr_recruitment = Node(Group(name="recruitment"), parent=hr)

IT = Node(Department(name="IT"), parent=root)
IT_dev = Node(Group(name="dev"), parent=IT)
IT_ops = Node(Group(name="ops"), parent=IT)

for row in RenderTree(root):
    print(row.node)

# print(RenderTree(root))