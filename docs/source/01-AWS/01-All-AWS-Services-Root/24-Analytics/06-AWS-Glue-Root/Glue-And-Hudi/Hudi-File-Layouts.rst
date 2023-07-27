Hudi File Layouts
==============================================================================
本文是我研读 Apache Hudi 微信公众号 - "探索Apache Hudi核心概念 (1) - File Layouts" 一文的读书笔记.


原文
------------------------------------------------------------------------------


核心概念
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File Layouts（文件布局）是指Hudi的数据文件在存储介质上的分布，Hudi会严格管理数据文件的命名、大小和存放位置，并会在适当时机新建、合并或分裂数据文件，这些逻辑都会体现在文件布局上。

Hudi在文件操作上有一个重要“原则”：Hudi always creates immutable files on disk。即：文件一旦创建，永远不会再更新，任何添加、修改或删除操作只会在现有文件数据的基础上合并输入数据一起写入到下一个新文件中，清楚这一点对我们解读文件布局很有帮助。

整体上，Hudi文件布局的顶层结构是数据表对应的base目录，下一层是各分区目录，分区目录可根据分区列数量嵌套多层，这和Hive/Spark的表结构是一致的。在最底层分区文件夹上，Hudi不再创建子文件夹，全部都是平铺的数据文件，但是这些文件在逻辑上依然有着清晰的层级关系。顶层的文件集合是File Group，File Group下面是File Slice，File Slice下面就是具体的数据文件了。我们反过来，按从下到上的顺序梳理一下这些文件和文件集合：

• Base File

Base File是存储Hudi数据集的主体文件，以Parquet等列式格式存储，所以我们在Hudi中看到的Parquet文件基本都是Base File。实际上，Base File的命名是为了呼应Log File，在没有Log File的COW表里，Base File就是基层的数据存储文件，没必要强调它的“Base”身份，直接叫Parquet文件就可以。Base File遵循一致的命名规范，格式为：

    <fileId>_<writeToken>_<instantTime>.parquet

以下是一个真实的Base File文件名：

    14845db4-80fc-48b3-88c6-1596ad704890-0_0-265-3521_20230309084842127.parquet
    fileId = 14845db4-80fc-48b3-88c6-1596ad704890-0
    writeToken = 0-265-3521
    instantTime = 20230309084842127

fileId部分是一个uuid，我们会在多个文件中看到相同的fileId，这些fileId相同的文件就组成了一个File Group。instantTime是写入这个文件对应的instant的时间，也是该文件的一个“版本”标注，因为一个Base File历经多轮增删改操作后就会产生多个版本，Hudi就使用instantTime对它们进行标识。不管是MOR表还是COW表，都有Base File，只是在COW表里只有Base File，在MOR表里除了Base File还有Log File。

• Log File

Log File是在MOR表中用于存储变化数据的文件，也常被称作Delta Log，Log File不会独立存在，一定会从属于某个Parquet格式的Base File，一个Base File和它从属的若干Log File所构成的就是一个File Slice。Log File也遵循一致的命名规范，格式为：

    .<fileId>_<baseCommitTime>.log.<fileVersion>_<writeToken>

以下是一个真实的Log File文件名：

    .14845db4-80fc-48b3-88c6-1596ad704890-0_20230309084842127.log.1._0-313-3582
    fileId = 14845db4-80fc-48b3-88c6-1596ad704890-0
    baseCommitTime = 20230309084842127
    fileVersion = 1
    writeToken = 0-313-3582

不同于Base File，Log File文件名中时间戳部分并不是Log File自己对应的instanceTime，而是它所从属的Base File的instanceTime，即baseCommitTime。如此一来，就没有办法通过时间戳来区分Log File提交的先后顺序了，所以Hudi在Log File文件名中加入了fileVersion，它是一个从1开始单调递增的序列号，用于标识Log File产生的顺序。

• File Slice

在MOR表里，由一个Base File和若干从属于它的Log File组成的文件集合被称为一个File Slice。应该说File Slice是针对MOR表的特定概念，对于COW表来说，由于它不生成Log File，所以File Silce只包含Base File，或者说每一个Base File就是一个独立的File Silce。总之，对于COW表来说没有必要区分File Silce，也不没必要强调Base File的“Base”身份，只是为了概念对齐，大家会统一约定Hudi文件的三层逻辑布局为：File Group -> File Slice -> Base / Log Files。

• File Group

在前面介绍Base File时，我们已经提到了File Group，简单说，就是fileId相同的文件属于同一个File Group。同一File Group下往往有多个不同版本（instantTime）的Base File（针对COW表）或Base File + Log File的组合（针对MOR表），当File Group内最新的Base File迭代到足够大（ >100MB）时，Hudi就不会在当前File Group上继续追加数据了，而是去创建新的File Group。


COW表的File Layouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
