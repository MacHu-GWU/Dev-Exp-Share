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


定义 Key Value 风格的参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在 Lua 中给函数传递参数都是 positioned, 也就是只按照位置顺序传递参数. 如果你记不住这些参数的位置, 想要用 key value 的方式调用函数, 那么你只能将函数变为只有一个参数的形式, 而且这个参数是一个 table, 然后在函数内部都用 arg.key 的形式调用这些值即可.

.. literalinclude:: ./function_04_key_value_arg.lua
   :language: lua


Table
------------------------------------------------------------------------------
Lua 中有且只有一个数据结构 Table. 它即是链表, 也是哈希表, 还能实现模块, 面向对象等功能.




Table as Dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们这里用 Python 中的 dict 来类比, 看看把 Table 当哈希表用是什么感觉.

.. literalinclude:: ./table_as_dict.lua
   :language: lua

::

    # output
    --- access value from key
    t["a"] = 1
    --- iterate key value pair:
    key = a, value = 1
    key = b, value = 2
    --- iterate key only pair:
    key = a
    key = b
    --- iterate value only pair:
    value = 1
    value = 2
    --- check if table has certain key
    table has key "b": true
    table has key "c": false
    --- assign key value pair
    t["b"] = 20, t["c"] = 30
    key = c, value = 30
    key = b, value = 20
    ❯ lua table_as_dict.lua
    --- access value from key
    t["a"] = 1
    --- iterate key value pair:
    key = b, value = 2
    key = a, value = 1
    --- iterate key only pair:
    key = b
    key = a
    --- iterate value only pair:
    value = 2
    value = 1
    --- check if table has certain key
    table has key "b": true
    table has key "c": false
    --- assign key value pair
    t["b"] = 20, t["c"] = 30
    --- delete key value pair
    key = b, value = 20
    key = c, value = 30
    --- get number of pairs in table
    2


Table as List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们这里用 Python 中的 list 来类比, 看看把 Table 当列表用是什么感觉.

.. literalinclude:: ./table_as_list.lua
   :language: lua

::

    #output
    --- get element by index, lua index start from 1
    t[1] = a
    t[2] = b
    --- get the last item in the list
    e
    --- get the second last item in the list
    d
    --- iterate a list
    ind = 1, value = a
    ind = 2, value = b
    ind = 3, value = c
    ind = 4, value = d
    ind = 5, value = e
    --- iterate the slice of the list
    ind = 2, value = b
    ind = 3, value = c
    ind = 4, value = d
    --- append to the end
    f
    --- remove the last element end
    nil
    e


Local and Global Variable
------------------------------------------------------------------------------
在 lua 中, 如果你不声明 ``local`` 就定义变量, 那么这个变量就是全局变量. 全局变量可以在函数内部被修改. 一般好的 lua 代码中所有的变量都应该定义成局部变量才能避免出 bug. 请看下面的例子:

.. literalinclude:: ./local_and_global_variable.lua
   :language: lua

::

    # output
    inside function a = 2
    outside function a = 2
    inside function b = 2
    outside function b = 1
    inside function c = 2
    outside function c = 2
    inside function d = 2
    outside function d = 1
