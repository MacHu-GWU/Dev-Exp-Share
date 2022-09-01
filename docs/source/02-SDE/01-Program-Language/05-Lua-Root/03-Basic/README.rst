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

.. literalinclude:: ./number_plus_minus_multiply_divide.lua
   :language: lua

::

    # output
    a = 2
    b = 2
    c = 2
    a + b = 8
    a * b = 12
    a / b = 0.33333333333333
    b / a = 3.0
    c / a = 4.5

String
------------------------------------------------------------------------------


字符串拼接
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ./string_01_concatenate.lua
   :language: lua

两个点 ``..`` 是字符串拼接. 相当于 Python 中的 ``s = "b" + s``.

::

    # output
    s = a
    s = ba
    s = dcba
    s = edcba




Function
------------------------------------------------------------------------------
在 Lua 中定义函数非常简单, 其中 ``function``, ``return``, ``end`` 是关键字.

.. code-block:: lua

    function func_name(arg1, arg2)
        ...
        return result
    end

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

定义函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
第一个例子, 函数里面可以有参数, Lua 是动态语言, 参数是没有类型的. 如果一个参数被定义了, 但是却没有被赋值, 那么它的默认值是 nil.

.. literalinclude:: ./function_01_define_a_func.lua
   :language: lua

::

    # output
    msg = hello!
    res = success
    msg = nil


定义多个参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ./function_02_multiple_argument.lua
   :language: lua

::

    # output
    msg1 = hello alice
    msg2 = hello bob



定义多个参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ./function_02_multiple_argument.lua
   :language: lua

::

    # output
    msg1 = hello alice
    msg2 = hello bob


定义可变长度的参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这里明确两个定义:

- 形参 Formal parameter, 定义的形式参数, 可以是任何值
- 实参 Actual parameter, 实际传入的参数, 是一个确定值

例如下面的 ``a`` 就是形参, 1 就是实参.

.. code-block:: lua

    function func(a)
    ...
    end

    func(1)

下面的例子中我们用 ``...`` 来表示该函数可以接受数量不同的实参. 当这个函数被调用时, 它的所有参数都会被收集到一起. 我们定义了个临时变量 ``args``, 它是个 table, 然后我们就可以用 ``ipairs`` 函数遍历里面的元素了, 当然我们对 index 不感兴趣, 只对 value 该兴趣, 所以可以用 ``_`` 语法 (和 Python 一样) 来忽略 index.

.. literalinclude:: ./function_03_any_number_arg.lua
   :language: lua

::

    # output
    alice
    bob


Table
------------------------------------------------------------------------------

Table