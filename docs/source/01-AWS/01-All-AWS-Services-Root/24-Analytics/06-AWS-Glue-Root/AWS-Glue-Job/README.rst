AWS Glue ETL
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 基础篇
------------------------------------------------------------------------------

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1.1 AWS Glue 服务是什么? 解决了什么问题?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



2. Glue Catalog
------------------------------------------------------------------------------


3. Glue Crawler
------------------------------------------------------------------------------


4. Glue Job
------------------------------------------------------------------------------


4.1 What is Glue Job
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Glue Job 是一个 ETL Job 的抽象. 指定一个编程语言 (只支持 Python / Scala), 一个 ETL main script, 作为唯一的入口, 需要的依赖的压缩包 (对于 python 是 .zip, 对于 scala 则是 .jar). 而 AWS Glue Job 在 Console

这篇官方文档 https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html 详细介绍了 Glue Job Run 相关的所有参数.


4.1 ETL Programming
------------------------------------------------------------------------------

4.1.1 General Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4.1.1.1 Special Parameters Used by AWS Glue
******************************************************************************

Special Parameter 是一些在运行 ETL script 之前, 对如何运行 ETL job 做出详细定义的一组参数. 和 Glue Job 的 settings 不同的是, settings 里面是一些比较高级, 非底层的设置. 例如 Job name, script 在 S3 的位置, IAM Role, Worker Type 算力 这些. 而 Special Parameter 里面则是 "是否使用 Glue Catalog 作为 metastore", "job bookmark 的策略是 enable, disable, pause" 等等这些细节.

这篇官方文档 https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html 详细介绍了 Glue Job Run 相关的所有参数.



4.2



对于一个 S3 Data Lake 而言,

- How can I configure an AWS Glue ETL job to output larger files?: https://aws.amazon.com/premiumsupport/knowledge-center/glue-job-output-large-files/
- Optimize memory management in AWS Glue: https://aws.amazon.com/blogs/big-data/optimize-memory-management-in-aws-glue/
- Reading Input Files in Larger Groups: https://docs.aws.amazon.com/glue/latest/dg/grouping-input-files.html

- WorkerType: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-job.html#aws-glue-api-jobs-job-Job