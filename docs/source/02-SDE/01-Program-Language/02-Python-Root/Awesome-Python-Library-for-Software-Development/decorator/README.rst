.. _pypi-decorator:

decorator
==============================================================================
keywords: python decorator

装饰器在 Python 中是非常有特点, 也非常有用的语法, 能大幅减少代码重复, 并且让代码更加易维护.

标准的 decorator 的实现会比较难, 首先你需要对于内部函数外部函数加很多 wrapper, 并且还要更新很多 function 本身的属性, 还可能丢失参数定义和类型信息, 可能还要对被装饰的函数按照 类, 方法, 函数 做区分.
很少有人能写出正确的装饰器实现. decorator 这个库可以让你写出来的装饰器更容易符合你的需求.

.. code-block:: bash

    pip install decorator

还有另一个用于写 decorator 的包 `wrapt <https://pypi.org/project/wrapt/>`_, 效果类似.


Examples
------------------------------------------------------------------------------
.. literalinclude:: example1.py
   :language: python

.. literalinclude:: example2.py
   :language: python
