Python Library - mock / pytest-mock
==============================================================================
Keywords: Python, Test, Mock, Pytest


Mock 的作用
------------------------------------------------------------------------------
经常我们会有一个函数被很多其他函数调用, 而这个函数依赖于一些真实的资源. 比如从服务器上获取一个文件. 这里我们在测试的时候可能并不关心获取这个文件的过程, 而是关心对这个文件进行后续处理的逻辑. 这时候我们如何测试呢?

1. 在函数设计的时候可能后续处理的逻辑的输入只有数据, 并不涉及获取文件这个动作. 我们是应该这么设计, 但是并不解决我们的问题. 因为最终的 API 的输入很可能只是包括这个文件的位置, 并没有数据.
2. 我们可以给这个获取文件的函数留一个可选参数 result, 如果 result 存在, 则直接返回而不执行获取文件的动作. 这样做对代码有侵入, 会留下很多 if else 垃圾代码. 并且这只适合返回固定值的情况, 无法做到对输入的参数进行一些静态计算后返回.

这就是 Mock 起作用的地方, mock 可以将你的某个函数替换成你自定义的函数, 或是自定义一个固定返回值. 而且你可以指定这个 Mock 起作用的作用域, 非常灵活. 再者甚至能对这个函数的调用次数进行统计, 追踪每次调用的情况.


几个例子
------------------------------------------------------------------------------
假设我们有一个 get_status 的函数还没有被实现, 而最终的 api 是 ``get_status_api``. 我们要对 ``get_status_api`` 进行测试.

.. literalinclude:: ./my_module.py
   :language: python

.. literalinclude:: ./test_example1.py
   :language: python

.. literalinclude:: ./test_example2.py
   :language: python

.. literalinclude:: ./test_example3.py
   :language: python

.. literalinclude:: ./test_example4.py
   :language: python


Patch a Variable
------------------------------------------------------------------------------
这个例子我们介绍了如何 mock 一个 模块内的 变量的值.

使用 Mock 有一个重点: "假设你有一个 变量/函数 你需要 mock 它的行为, 千万不要在你定义它的地方 Mock, 而是要在你 **使用** 它的地方 mock"

首先我们有这样一个模块::

    my_package
    |--- app.py
    |--- constant.py

.. literalinclude:: ./my_package/constant.py
   :language: python

.. literalinclude:: ./my_package/app.py
   :language: python

可以看出 ``my_package.constant.key1`` 是在 ``constant.py`` 模块中被定义的, 而是在 ``my_package.app.print_constant`` 函数中被使用的. 我们现在要来测试 ``print_constant`` 函数, 不过我们想要替换掉 ``key1`` 的值.

.. literalinclude:: ./test_patch_a_variable.py
   :language: python

最后的结果是这样的::

    do test with mock
    constant.key1 = value111
    constant.key2 = value2
    constant.key3 = value3
    without mock
    constant.key1 = value1
    constant.key2 = value2
    constant.key3 = value3
