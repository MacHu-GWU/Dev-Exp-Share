.. _pypi-pygtrie:

Pygtrie, prefix tree data structure
==============================================================================
Install: ``pip install pygtrie``


Overview
------------------------------------------------------------------------------
``pygtrie`` 是对前缀树数据结构的纯 Python 实现. 开始由 Google 开发, 后来被开源社区个人接手
维护. 这个数据结构的特点是任选一个父节点, 下面所有的子节点都有相同的前缀. 假如有 1M 个字符串,
然后给定一个字符串, 从这 1M 个字符串中找到最大前缀, 这个数据结构就是为了解决这一类问题的.


.. literalinclude:: ./example.py
   :language: python
