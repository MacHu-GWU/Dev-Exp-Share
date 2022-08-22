Lua Basic
==============================================================================
本文主要参考自官方文档中的 Basic Concepts 一章.

- https://www.lua.org/manual/5.3/manual.html
- https://cloudwu.github.io/lua53doc/manual.html

Lua 中一共有这么 8 种基本数据类型:

- nil: 类似于 None
- boolean: true 和 false
- number: 整数和浮点都是这个
- string
- function: 函数也是一个数据类型
- userdata
- thread
- table: 万能数据结构, 即是列表, 也是字典, 还是面向对象的类

.. literalinclude:: ./lua_number_plus_minus_multiply_divide.lua
   :language: lua

::

    a = 2
    b = 2
    c = 2
    a + b = 8
    a * b = 12
    a / b = 0.33333333333333
    b / a = 3.0
    c / a = 4.5
