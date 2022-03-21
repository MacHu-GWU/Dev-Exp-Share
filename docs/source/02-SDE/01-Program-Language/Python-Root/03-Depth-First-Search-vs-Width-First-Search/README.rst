.. _dfs-vs-wfs-in-python:

Depth First Search vs Width First Search in Python
==============================================================================
Keywords: DFS, WFS, 深度优先, 广度优先

深度优先 (DFS) 和 广度优先 (WFS) 是算法中两种常用的搜索算法. 在很多场景都有着广泛应用:

**Serialization (序列化)**:

把一个复杂数据结构序列化, 数据结构的 attribute 有可能是另一个复杂的数据结构. 所以一个序列化算法通常需要用 DFS 搜索到最终叶节点, 从叶节点到根节点一直回溯序列化回来, 才算是完成了一个完整的序列化.

**Prefix Tree Search**:

给定一个字符串, 从一堆字符串中找到有着最长前缀的字符串. 比如给定一个文件路径和一堆文件夹路径, 这个文件到底是属于哪个文件夹的呢? 这个算法就要用到 WFS 搜索.

DFS, WFS 在 Python 中的主要实现方法是递归.

这里有个 DFS 和 WFS 的简单实现:

.. literalinclude:: ./dfs_with_wfs.py
   :language: python
