AWS Data Pipeline
=================

简单来说, Data Pipeline 是和 EMR 绑定的一个服务, 用于将数据从 数据库中 转移到 S3 中. 相当于一个自动化的 ETL. 你可以在 Data Pipeline 中设定百分之多少的 读写负载 用于执行 ETL (通常为 0.25). 而这些工作则在 由 Data Pipeline 自动启动的 EC2, EMR 上, 或是用户自己管理的 EC2 或 EMR 上运行的.

Example: Dynamodb -> Data Pipeline -> S3, Data Pipeline 支持以 S3 为媒介, 将 DynamoDB, RDS, Redshift 的数据移来移去.

Data Pipeline FAQ: https://aws.amazon.com/cn/datapipeline/faqs/

.. _data-pipeline-what-is-data-notes:

Data Nodes
------------------------------------------------------------------------------

Data Nodes define the S3location and type of data that Data Pipeline activities use as input or output. 简单来说, Data Nodes 是一个抽象的数据节点 (S3 Folder), 用于保存数据的中间状态.

Data Nodes Activities:

- Preconditions:
- Scheduling Pipelines:
- Resources: The computational resource like EC2 or EMR cluster
- Actions:

Parts of Data Pipeline

- Pipeline Components:
- Instances (Tasks):
- Attempts:

