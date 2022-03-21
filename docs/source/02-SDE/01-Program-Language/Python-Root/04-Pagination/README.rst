.. _pagination-in-python:

Pagination in Python
==============================================================================
很多 Web API 为了避免一次性 return 太多的资源, 通常都会用一种叫做 Pagination 的机制. 每次 request 只 return 一定数量的资源, 并给予一个 paginator token 作为上次 request 的终点, 或是 下次 request 的起点. 然后用这个 paginator 发起下一个 request, 直到所有的资源都被返回, paginator 为 None 为止. 这样做能让一个客户端单位时间内所能消耗的服务器资源上限为恒定值.

但是在编程中, 我们通常需要返回所有的资源, 但是原生 API 往往出于性能考虑, 不会直接提供这个返回所有资源的 API, 而只会提供 Pagination 的 API. 这里我们提供了一个例子, 展示了如果基于 Pagination API 实现返回所有资源的 API.

.. literalinclude:: ./pagination.py
   :language: python
