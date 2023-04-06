**问题**

测试如果一个文件夹下的文件有多种不同的格式, 例如 csv, json, excel, 但是他们的 schema 是一致的, 应该如何配置 crawler 进行处理?

**测试**

1. create database: name = ``glue_crawler_poc``
2. create crawler:
    - name = ``same_schema_mixed_file_type_json``
    - exclude pattern:
        - ``**.csv``, ``**.xlsx``
    - prefix = ``json_``
3. run crawler: 发现创建的 table 中的 object count = 1 是对的, 但是 record count 也是对的
3. 在 athena 中 对 ``json_users`` 进行 query, 发现返回了 3 条数据, 只有 1 条是对的, 其他 2 条是空行. 换言之 **athena 会对文件夹下的所有数据尝试进行扫描, 除非用到了 partition key. athena 不会自动去 catalog 里只扫描被记录的 object**.


**结论**

一个文件夹下的文件有多种不同的格式, 就算你用 Exclude Pattern 让 Crawler 只专注于一种格式, 创建出来的表也有问题.

所以一定要保证一个文件夹下的数据格式是相同的.
