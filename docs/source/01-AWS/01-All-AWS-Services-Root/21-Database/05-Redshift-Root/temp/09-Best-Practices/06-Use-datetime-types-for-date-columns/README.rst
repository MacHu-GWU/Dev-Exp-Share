.. _aws-redshift-best-practice-use-datetime-types-for-date-columns:

Use datetime types for date columns
==============================================================================
Keywords: AWS Redshift, Best practice


**一句话总结**: 不要用 CHAR 或者 VARCHAR 来存储时间和日期. 建议使用 `Datetime types <https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html>`_ 里面的数据类型储存.

**原因**: 因为字符串占用的空间多, 并且不利于索引, 而时间和日期的本质是整数, 用基于整数的 Datetime 数据类型要有效的多. 至于让人类更加可读, 操作更方便, 这交给输入和输出时的客户端去解决, 让输入和输出更加人类可读的开销要比储存数据, 查询数据少几个数量级.

**结论**: 日期都用 ``DATE`` 数据类型. 而时间则用默认 UTC, 不带时区的 ``TIMESTAMP``. 建议存入数据库之前所有时区都转化为 UTC 时间.

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-timestamp-date-columns.html
- https://docs.aws.amazon.com/redshift/latest/dg/r_Datetime_types.html