.. _aws-batch-root:

AWS Batch Root
==============================================================================
Keywords: AWS Batch Root

`AWS Batch <https://aws.amazon.com/batch/faqs/>`_ 是一个用容器 (也可以用 EC2) 来运行 Batch Job 的全托管服务, 使得用户可以专注于业务逻辑的开发, 而将调度, 运行, 扩容交给 AWS. 和 Lambda 相比虽然多了构建容器的环节, 但是也获得了长达 14 天的运行时间, 以及更大的内存和 CPU 资源. AWS 自己的很多服务都是基于 AWS Batch 来实现的, 比如 SageMaker, Textract, Comprehend 等等. 该服务的调度, 管理部分完全免费, 只对你实际用容器进行计算的时间收费.

在我的生产实践中, 该技术是一个应用非常广泛, 非常实用的技术. 是 AWS Lambda 很好的补充. 是我认为 AWS 计算类服务中的 Top 3 服务之一 (EC2, Lambda, Batch).

.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
