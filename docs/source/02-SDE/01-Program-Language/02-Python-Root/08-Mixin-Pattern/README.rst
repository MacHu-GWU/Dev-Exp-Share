.. _python-mixin-pattern:

Python: Mixin Pattern
==============================================================================


Summary
------------------------------------------------------------------------------
在面向对象 OOP 中 Mixin (混合) 是一种设计模式. 跟继承不同的是, Mixin 类并不是父类的延伸, 而是对父类的功能进行扩展的可插拔功能. 这里的重点是可插拔. 跟继承不一样, 继承了以后子类就是子类, 父类就是父类, 用户两个类都会用到. 而 Mixin 模式中通常只有父类会被用到, 而父类本质上是 父类 + Mixin 类 最终形成的一个类. Mixin 类不会被直接用到.

这个模式在什么时候有用呢? 当你要写一个很复杂的类, 里面的 method (方法) 超级多的时候, 如果你把所有的方法放在一个模块中, 那么这是相当不好测试和维护的. 用继承的模式的话, 相当于你把它分拆成 N 个 .py 文件, 按照顺序, 第 1 个是 class1, 然后第 2 个继承第一个是 class2, 第 3 个又继承第二个是 class3. 这种顺序关系从逻辑上其实是不成立的. 诚然里面的 method 是有一些依赖关系的, 但是大部分其实是相互独立的关系, 将他们做成可插拔的 mixin 会更好. 这个时候就是 Mixin 模式的应用场景了.

由于 Python 中有 TypeHint, 你希望在每个 mixin 类都能利用上所有其他 mixin 类的 type hint, 这需要一点点设计. 请看下面的例子.


Example
------------------------------------------------------------------------------
模块的结构如下::

    my_lib
    |--- __init__.py
    |--- base.py
    |--- mixin1.py
    |--- mixin2.py
    |--- my_class.py

我们有一个基类在 base.py 中. 这里主要定义了 constructor, 而不管其他的. 而 mixin1, 2, ... 都是 Mixin 类. 而最后给用户的 API 是 my_class.py 中的 MyClass. 在 TypeHint 中我们都利用了 TYPE_CHECKING 这个办法只提供 type hint, 不真正的 import. 从而让所有的 Mixin 类都认为自己是最后的 MyClass, 从而获得了其他 Mixin 类中的 type hint.

.. code-block:: python

    import typing as T

    if T.TYPE_CHECKING:
        from .my_class import MyClass


.. literalinclude:: ./my_lib/base.py
   :language: python

.. literalinclude:: ./my_lib/mixin1.py
   :language: python

.. literalinclude:: ./my_lib/mixin2.py
   :language: python

.. literalinclude:: ./my_lib/my_class.py
   :language: python

最后你可以从最终用户的脚步在这个 test.py 进行测试. 你发现你的 type hint 能检测到所有的 Mixin 中定义的东西.

.. literalinclude:: ./test.py
   :language: python
