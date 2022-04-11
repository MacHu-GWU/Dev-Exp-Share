.. _aws-lake-formation-basic:

AWS Lake Formation Basic
==============================================================================
Keywords: AWS, Lake Formation, LakeFormation, LF

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


The Nature of Data Access Control Management
------------------------------------------------------------------------------
为了理解数据权限管理 (Data Access Control Management) 的本质, 我们需要先理解三个概念:

- ``Principal``: "谁能访问什么" 这句话里面的 "谁". 可以是真人, 可以是 laptop, 可以是云上的虚拟主机, 可以是容器.
- ``Resource``: "谁能访问什么" 这句话里的 "什么". 可以是某个磁盘位置, 可以是某个数据库, 可以是云存储中的一个文件或者文件夹.
- ``Action``: "我能对这个文件做什么" 这句话里的 "做什么". 例如: 可以读, 可以写, 可以更改, 可以删除.

所谓数据权限管理的本质就是 ``Principal``, ``Resource``, ``Action`` 的排列组合.


AWS Lake Formation How it Works
------------------------------------------------------------------------------
对于传统的权限管理, 本质上就是定义 ``Principal`` 和 ``Resource`` 之间的联系. 这个联系就是 ``Permission``. 无法访问也是一种特殊的 ``Permission``. 但传统的权限管理的问题是随着企业越做越大, 管理的复杂度越来越高. 因为本质上你需要为所有的 ``Principal`` 和 ``Resource`` 之间创建连接, 复杂度为 M * N.

Lake Formation 在几年前也是用的这种传统的权限管理, 但是从 2020 年起, 主流的权限管理变成了 Tag Based Access Control. Tag 就是一个简单的 Key Value Pair. 如果 ``Principal`` 和 ``Resource`` 拥有相同的 ``Tag``, 那么就可以对其进行访问. 这个 Tag 相当于一个中间人, 使得 ``Principal`` 和 ``Resource`` 不直接打交道. 比如你的公司有三类人, Admin, Data Engineer, Business Analytics, 那么你只需要创建 3 个 Tag, 然后给这三种人不同的 Tag, 然后给不同的 Resource 不同的 Tag 即可. 假设你有 K 个 tag, 那么整体复杂度为 M * K + N * K, 从而大大降低了管理的复杂度. (其实 IAM Group, 也是一个原理, 在同一个 Group 人的人自动获得该权限).
