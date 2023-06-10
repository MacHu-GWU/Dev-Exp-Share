Connect to Opensearch via Opensearch py
==============================================================================
Keywords: AWS OpenSearch, Connect, Python, Authenticate

用 Python 连接到 AWS 托管的 Opensearch 的鉴权方式有很多种, 不过我比较推荐使用 IAM Role. 具体示例代码如下:

Connect to Opensearch Domain

.. literalinclude:: ./connect_to_opensearch_domain.py
   :language: python
   :linenos:

Connect to Opensearch Serverless

.. literalinclude:: ./connect_to_opensearch_serverless.py
   :language: python
   :linenos:
