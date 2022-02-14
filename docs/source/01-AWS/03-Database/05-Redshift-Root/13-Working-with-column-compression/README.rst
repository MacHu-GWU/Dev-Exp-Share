.. _aws-redshift-working-with-column-compression:

Working with column compression
==============================================================================
Keywords: AWS Redshift, Column Compression

Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/t_Compressing_data_on_disk.html

由于 Redshift 在存储层使用了 column 列存储, 所以对不同的数据类型做压缩优化可以节约磁盘, 在大部分的情况下提高性能, 少部分的情况下牺牲一点点性能.


Compression Encoding
------------------------------------------------------------------------------
AZ64 encoding

    一种针对整数的编码, 其原理不详, 不仅能减少磁盘空间占用, 还能提升查询性能

Byte-dictionary encoding

    对于 Enum 数据 (不同的 unique 值的总数小于 256) 适用的字典存储. 由于 1 bytes = 8 bit, 所以最多支持 256 个不同的值.

Delta encoding

    适合于递增递减的步长不大的数据, 比如 datetime 的类型. 它只保存与前一个值相比的 delta 值.

LZO encoding

    是一种致力于解压缩快的压缩算法, 适合于 CHAR / VARCHAR 数据类型. 如果该字符串 column 需要大量参与到 WHERE, 那么就不太合适. 该编码适合于只存不查的 column

Mostly encoding

    简单来说就是说比如一个 column 中的值的整个范围需要用到 8 bytes, 但大部分的值只需要用到 4 bytes, 那么就可以将大部分的只需要 4 bytes 的值用 4 bytes 编码.

Run length encoding

    简单来说如果一个 column 中的值的 cardinality 很低, 比如只有 10. 那么大概率出现连续多个 row 的这个 column 的值会是一样的. 比如一个 color 的列只有 10 个 color, 那么就可以用 4 个 blue, 5 个 red 这样的方式节约存储空间. 该方法不推荐用在 sort key 上, 这会导致非常大的性能浪费.

Text255 and Text32k encodings

    简单来说就是字典, 把出现频率较高的 word, 照字典编码成整数. 该方式只适合西方语系的语言, 不适合中文日文, 因为中文日文最小单位 token 本身占用的比特就不多, 不适合压缩.

Zstandard encoding

    Facebook 2016 年开源的通用型压缩算法, 对整数, 字符串压缩效果都很好, 压缩解压都快, 压缩率也高. 适合作为通用压缩算法. 但在整数类型上的压缩效率要全面差于 AZ64.

总结

    Byte-dictionary, Delta, Text255, Run length, Mostly 都有独特的应用场景, 基本上没有异议.

    其他情况下对于整数类型基本可以无脑上 AZ64. 对于中等长度复杂字符串可以无脑上 Zstandard, 而对于只存不查的大量字符串则适合 LZO.
