**问题**

测试如果一个文件夹下的文件有多种不同的格式, 例如 csv, json, excel, 但是他们的 schema 是一致的, 应该如何配置 crawler 进行处理?

**测试**

1. create database: name = ``glue_crawler_poc``
2. create crawler:
    - name = ``exclude_pattern_poc``
    - exclude pattern:
        - ``*/LOAD*``
3. run crawler: 发现创建的 table 中的 object count = 3 是对的, 但是 record count 也是对的 (6的意思是因为包含了 header)
3. 在 athena 中 对 ``users`` 进行 query, 发现返回了 6 条数据. 这是因为 **athena 会对文件夹下的所有数据尝试进行扫描, 除非用到了 partition key. athena 不会自动去 catalog 里只扫描被记录的 object**.


**结论**

一个文件夹下的文件有多种不同的格式, 就算你用 Exclude Pattern 让 Catalog 只收纳部分 object, 但是 Athena 的查询只能进行文件夹的全量扫描 (除非用到了 partition key). Catalog 收纳的部分 object 还是可以用于 Glue ETL Job.

**如果你要用 Athena 查询文件夹下的数据, 但又忽略一部分 object, 是做不到的**.
