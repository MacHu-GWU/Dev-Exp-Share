.. _pystdlib-enum:

enum - Enumeration
==============================================================================

从 Python3.4 起, ``enum`` 成为了标准库中的一部分. 是枚举常量的不二选择. enum 在 3.4 之前的 backport 替代品是 `enum34 <https://pypi.org/project/enum34/>`_.


什么时候需要用 enum?
------------------------------------------------------------------------------

Example: Status Code

很多业务代码中会定义状态码. 但是 0, 1, 2 这些状态码对于机器很友好, 但是对于人类意义不明. 最佳实践是在代码中用 enum 枚举定义这些值, 然后 import 枚举. 这样使得代码更加容易维护, 也可以通过语法来避免 typo.

.. code-block:: python

    import enum

    class StatusCode(enum.Enum):
        todo = 0
        failed = 1
        success = 2

    print("Now status code is {}".format(StatusCode.success.value))


Best Practice
------------------------------------------------------------------------------
.. literalinclude:: ./best_practice.py
   :language: python


Generic Enum Getter
------------------------------------------------------------------------------
.. literalinclude:: ./generic_enum_getter.py
   :language: python


.. toctree::
   :maxdepth:
   :caption: Notebooks:

   enum-tutorial