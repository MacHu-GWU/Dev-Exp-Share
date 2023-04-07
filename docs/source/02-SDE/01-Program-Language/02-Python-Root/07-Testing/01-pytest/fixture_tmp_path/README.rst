``pytest`` ``tmp_path`` fixture
==============================================================================
在测试中使用临时的目录进行测试, 然后测试结束后删除这个目录是一种很常见的模式.

pytest 提供了一个内置的 `tmp_path <https://docs.pytest.org/en/latest/how-to/tmp_path.html#tmp-path>`_ 的 fixture 来完成这个任务.

Example:

.. literalinclude:: ./test.py
   :language: python
