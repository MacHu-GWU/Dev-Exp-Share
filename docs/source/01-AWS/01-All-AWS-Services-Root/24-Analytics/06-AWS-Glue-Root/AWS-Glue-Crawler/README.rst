AWS Glue Crawler
==============================================================================



Include Exclude Pattern
------------------------------------------------------------------------------

- Include and Exclude Patterns: https://docs.aws.amazon.com/glue/latest/dg/define-crawler.html#crawler-data-stores-exclude


Include
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S3:

对于 S3, Include 只有两种模式, 一种是指定具体的文件, 只爬取一个文件. 另一种是指定一个具体的文件夹, 爬取这个文件夹下的所有文件. Include 不支持模糊匹配.








Exclude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S3:

对于 S3, Exclude 中的 Glob Pattern 是跟 Include Path 合在一起使用的, 只有 Include Path 是文件夹的时候有用. 是在 Include Path 下的相对路径. 其中有几个重要的通配符:

- ``**`` 可以跨文件夹匹配
- ``*`` 不能跨文件夹匹配
- ``[]`` 枚举匹配的字符 (不是字符串)
- ``{}`` 枚举 Sub pattern
