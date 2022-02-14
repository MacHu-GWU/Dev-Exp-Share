.. _aws-redshift-unloading-data:

Unloading Data
==============================================================================
Ref:

- https://docs.aws.amazon.com/redshift/latest/dg/c_unloading_data.html

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Unloading data to Amazon S3
------------------------------------------------------------------------------
默认情况下你的 SQL client 发送了一个 query, Redshift 会在每个 Slice 上执行这些 query, 然后这些分布在每个 Slice 上的 result 会以并行的方式返回. (特殊情况是你指定了 sort by 排序, 那么这些数据会被汇总到一个 node 上进行排序后再返回)

如果你想把数据结果 dump 到 S3, 你可以使用 ``UNLOAD`` 命令将 query 的结果写入到 S3. 具体的写入行为可以通过参数控制, 比如写成什么数据格式, 是一个大文件还是多个小文件. 数据在 S3 上会被 Server side encryption 加密.