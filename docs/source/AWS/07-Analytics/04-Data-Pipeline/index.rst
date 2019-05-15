AWS Data Pipeline
=================

简单来说, Data Pipeline 是和 EMR 绑定的一个服务, 用于将数据从 数据库中 转移到 S3 中. 相当于一个自动化的 ETL. 你可以在 Data Pipeline 中设定百分之多少的 读写负载 用于执行 ETL.

Example: Dynamodb -> Data Pipeline -> S3


.. _data-pipeline-what-is-data-notes:

Data Nodes
------------------------------------------------------------------------------

Data Nodes define the location and type of data that Data Pipeline activities use as input or output.

- DynamoDB
- SQL
- Redshift
- S3

Date Pipeline


Data Nodes Activities:

- Preconditions:
- Scheduling Pipelines:
- Resources: The computational resource like EC2 or EMR cluster
- Actions:

Parts of Data Pipeline

- Pipeline Components:
- Instances (Tasks):
- Attempts:
