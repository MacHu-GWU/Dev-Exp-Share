Boto3 Stubs
==============================================================================
原生的 AWS Python SDK boto3 是没有 auto complete 和 type hint 的. 因为它的工作原理是利用 JSON 配置文件, 动态生成 class, 然后动态生成 client, 里面的方法都是用 getattr 来实现的. 所以你的 IDE 不可能推断出 client 有什么方法, 每个方法有什么参数.

社区里有一个 `boto3-stubs <https://pypi.org/project/boto3-stubs/>`_ 可以解决这一问题. 这个包的作者 parse 了 botocore 中的 JSON 文件, 动态生成了许多 `stub <https://mypy.readthedocs.io/en/stable/stubs.html>`_ 文件. 你只要安装了 ``boto3-stubs``, 并且安装了 ``mypy`` (可能也不需要). 能让你在 dev 开发的时候能享受到 auto complete 和 type hint.

根据我的实验和作者的反馈, PyCharm 的对自动检测的模式的支持貌似有点问题, 只能用 explicit type hint 来支持这一点. 但是这也完全够了.

要注意的是 ``boto3-stubs`` 里面有 333 个 service 的子包, 你如果全部安装的话光 stub 文件就有 100 多 MB, 这会导致你的 IDE load 很慢, 一般是只装需要的就可以了, 例如 ``pip install 'boto3-stubs[essential]'``. 至于具体怎么安装请参考官方文档..

还有一点要注意的是, 你要用 ``typing.TYPE_CHECKING``, 把用于 type hint 的 class 都放在下面, 只用来做 type hint, 而不实际运行. 你可以参考下面的例子.

.. literalinclude:: ./example.py
   :language: python
