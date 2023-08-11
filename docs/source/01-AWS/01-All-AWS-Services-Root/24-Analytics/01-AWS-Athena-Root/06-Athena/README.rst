Write Athena Query Results in Parquet, Avro, ORC, JSON formats
==============================================================================
Keywords: AWS, Athena, Parquet, Avro, ORC, JSON, S3


Introduction
------------------------------------------------------------------------------
Athena 默认使用 CSV 文件格式来保存 query result. 由于在大数据领域有很多更优秀的数据格式更适合保存数据. 从 2021-08-05 年起, AWS Athena 开始支持 Parquet, Avro, ORC, JSON 等格式. 但是使用这些格式的方法官方文档说的并不清楚. 本文将介绍如何使用 Parquet 格式来保存 Athena 的查询结果 (其他格式都类似).

`UNLOAD command in Athena <https://docs.aws.amazon.com/athena/latest/ug/unload.html>`_ 是一个 SQL 命令, 可以用来指定将 query result 导出到 S3. 而且它支持一些参数, 用来指定导出格式以及这些格式的详细配置.

你在 UNLOAD 的时候需要指定一个还不存在的 S3 folder, 用于保存 parquet 文件. 由于 Athena 是一个并行引擎, 所以会导出多个数据文件. 你在调用 ``boto3.athena_client.start_query_execution()`` API 的时候需要指定一个 S3 folder 用来保存 query result metadata. 这个文件夹和之前那个可以相同也可以不同. 但我推荐用不同的, 以方便区分数据和 metadata. 这里面的 metadata 文件中包括一个 ``${query_execution_id}-manifest.csv`` 文件, 记录了导出的所有 parquet 文件的 S3 URI 列表.

所以总结下来, 你需要做这么几件事:

1. 把原本的 SQL 语句用 UNLOAD 封装.
2. 调用 ``start_query_execution()`` API 来执行查询.
3. 用 Job Poll 模式每隔几秒就去查一下 execution status, 如果成功了就进行下一步.
4. 从 metadata 文件中读取 parquet 文件的 S3 URI 列表.
5. 从 parquet 文件中读取 dataframe 然后拼接成一个.

下面有一个脚本实现了上面的逻辑, 可供参考.

.. literalinclude:: ./example.py
   :language: python
   :linenos:


Reference
------------------------------------------------------------------------------
- From 2021-08-05 `Athena can now write query results in Parquet, Avro, ORC and JSON formats <https://aws.amazon.com/about-aws/whats-new/2021/08/athena-can-write-query-results-parquet-avro-orc-json-formats/>`_
- `UNLOAD command in Athena <https://docs.aws.amazon.com/athena/latest/ug/unload.html>`_