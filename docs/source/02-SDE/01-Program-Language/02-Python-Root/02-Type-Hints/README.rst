.. _type-hint-in-python:

Type Hint in Python
==============================================================================
Keywords: Python, typing, type hint, type hints, typehint, typehints, mypy


.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:



Avoid Cyclic Import for Type Hint
------------------------------------------------------------------------------
**Challenge**

在大型项目的代码中, 通常模块众多, 互有依赖. 所以避免 "循环导入" 是常识, 并且有很多设计模式可以避免这一点. **但一旦想要给所有的 API 涉及到的参数添加 Type Hint, 这一点就变得几乎无法做到**.

**Solution**

``typing.TYPE_CHECKING`` 是 Type Hint 核心模块 ``typing`` 中的一个魔法常量. 在正常 runtime, 这个常量的值永远是 ``False``. 所以你可以把需要用来做 Type Hint 的 import 放在 ``if TYPE_CHECKING:`` 的下面, 这样 IDE 和静态分析软件就可以读取这些信息并提供基于 Type Hint 的功能. 而 Runtime 则完全不受影响. 这得益于 Python 是动态语言的特性, 如果代码不被执行, 即使实际上有错也没有关系. 而静态分析软件则可以在运行检查之前提前 ``import typing`` 然后用 monkey patch 将其改为 ``typing.TYPE_CHECKING = True`` 即可.

这里有一个小问题, 如果用于 Type Hint 的 type 在被标注时没有被定义, 则需要用 ``'yourClassHere'`` 将其标注起来. 这样很不方便. 所以在 Python3.7+ 引入了 ``from __future__ import annotations``, 这使得 type hint 都会被标注为字符串保存在 ``__annotations__`` 系统变量中. 这使得所有的 type hint annotation 都不会在 runtime 中被 evaluate, 从而避免了 ``'yourClassHere'`` 这样的语法. 这也是很多开源库都选择只支持 3.7+. 如果你的库要支持 3.6, 那么请不要使用 ``from __future__ import annotations`` 这一功能.

.. literalinclude:: ./avoid_cyclic_import_a.py
   :language: python

.. literalinclude:: ./avoid_cyclic_import_b.py
   :language: python

Ref:

- https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
- https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports


Distinguish Class Attribute and Instance Attribute Type Hint
------------------------------------------------------------------------------
.. literalinclude:: ./class_attr_and_instance_attr.py
   :language: python


One Method Rtype Depends On Other Method Rtype
------------------------------------------------------------------------------
.. literalinclude:: ./one_method_rtype_depends_on_other_method_rtype.py
   :language: python

.. literalinclude:: ./generic_more_complicate.py
   :language: python
