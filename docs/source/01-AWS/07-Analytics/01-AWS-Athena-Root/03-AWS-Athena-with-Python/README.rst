.. _aws-athena-with-python:

AWS Athena with Python
==============================================================================

Keywords: Athena, Python, pyathena

在 Python 的世界里有一个标准叫做 `DB API 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ 的标准. 无论底层是什么 SQL 数据库 (前提要是 SQL 数据库), 只要你的库遵循这个标准, 那么就可以用 ``connect.execute(sql_statement)`` 这样的语法返回一个 iterable 的 cursor 对象, 返回的每条记录是以 namedtuple 的形式存在的. 而 Python 中的生产级 SQL 库 sqlalchemy 也能对遵循 DB API 2.0 的库有着良好的支持.

Python 社区对 Athena 的 DB API 2.0 实现的库是 https://pypi.org/project/pyathena/. 本质上 Athena 是将数据存在 S3 bucket 中, 而 ``pyathena`` 是通过实现一个 wrapper, 以实现 DB API 2.0 标准. 如果想要用 python 操作 Athena, 建议参照 ``pyathena`` 的文档, 配合 ``sqlalchemy`` 和 ``pandas`` 一起使用, 体验最好.

``requirements.txt`` Dependency

.. literalinclude:: ./requirements.txt

``prepare_data.py`` data faker

.. literalinclude:: ./prepare_data.py

``query_data.py`` pyathena usage example

.. literalinclude:: ./query_data.py
