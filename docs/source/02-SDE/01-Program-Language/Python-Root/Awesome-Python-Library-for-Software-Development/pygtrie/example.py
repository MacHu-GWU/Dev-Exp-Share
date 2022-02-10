# -*- coding: utf-8 -*-

"""
``pygtrie`` 是对前缀树数据结构的纯 Python 实现. 开始由 Google 开发, 后来被开源社区个人接手
维护. 这个数据结构的特点是任选一个父节点, 下面所有的子节点都有相同的前缀. 假如有 1M 个字符串,
然后给定一个字符串, 从这 1M 个字符串中找到最大前缀, 这个数据结构就是为了解决这一类问题的.

- https://pypi.org/project/pygtrie/
- https://github.com/mina86/pygtrie

Trie data structure, also known as radix or prefix tree,
is a tree associating keys to values where all the descendants of
a node have a common prefix (associated with that node).
"""

import pygtrie
import random
import string
from datetime import datetime

# 创建许多字符串
n = 1000000
keys = [
    "".join([random.choice(string.ascii_lowercase) for _ in range(10)])
    for i in range(n)
]

# 创建纯 list 数据结构
st = datetime.utcnow()
keys = [
    k
    for k in keys
]
elapse = (datetime.utcnow() - st).total_seconds()
print(elapse)

# 创建 trie 数据结构, 创建数据结构本身比较耗时
st = datetime.utcnow()
t = pygtrie.StringTrie()
for k in keys:
    t[k] = None
elapse = (datetime.utcnow() - st).total_seconds()
print(elapse)

# 创建许多测试用例, 最终取平均值
n_test = 100
test_paths = [f"{random.choice(keys)}/a/b/c/data.json" for _ in range(n_test)]

# 原始的一个个比较的方法
st = datetime.utcnow()
for path in test_paths:
    for k in keys:
        if path.startswith(k):
            break
elapse = (datetime.utcnow() - st).total_seconds()
print(elapse)

# 使用 trie 数据结构的方法
st = datetime.utcnow()
for path in test_paths:
    t.longest_prefix(path)
elapse = (datetime.utcnow() - st).total_seconds()
print(elapse)
