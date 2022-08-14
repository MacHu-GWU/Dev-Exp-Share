.. _aws-timestream:

AWS Timestream
==============================================================================

.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst


.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Amazon Timestream
------------------------------------------------------------------------------

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Timestream Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Serverless with auto-scaling
2. Data lifecycle managemen
3. Simplified data access
4. Purpose-built for time series
5. Always encrypted
6. High availability
7. Durability


Timestream Use cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Monitoring metrics to improve the performance and availability of your applications.
- Storage and analysis of industrial telemetry to streamline equipment management and maintenance.
- Tracking user interaction with an application over time.
- Storage and analysis of IoT sensor data


How it Works
------------------------------------------------------------------------------

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:



Timestream Concepts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Time series: 一个有具体应用场景的数据集, 例如 CPU utilization, temperature reading, sensors measurement.
- Record: 一个 Time series 中的一条记录.
- Dimension: 一个 Time series 的 metadata, 例如 IOT sensor 的场景下, dimension name = ``device_id``, dimension value = ``12345``. 在一个 Time series 中, Dimension 是被所有 record 共享的.
- Measure: 一个具体的 measurement 的值, 也就是这个 dataset 中最重要的那个 value.
- Timestamp: 时间戳.
- Table: A container for a set of related time series.

这些概念在 Database 以及 Table 中的逻辑关系是这样的::

    Database
        Table
            Series 1 CPU                Timestamp   Measurement
            Region: us-west-1           2019-01-01  55%
            Host: server1               ...         ...
            measurement name: cpu       ...         ...

            Series 2 CPU                Timestamp   Measurement
            Region: us-east-1           2019-01-01  61%
            Host: server2               ...         ...
            measurement name: cpu       ...         ...

            Series 3 CPU                Timestamp   Measurement
            Region: us-east-2           2019-01-01  53%
            Host: server3               ...         ...
            measurement name: cpu       ...         ...


Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

架构简图::

    timestream-write
        | aws sdk (java, python, ...)
    ingestion layer
        |
    storage layer: in-memory store, magnetic store
        |
    query layer
        | jdbc, aws sdk (java, python)
    timestream-query

**Write Architect**:

数据写入是通过 API 与 ingestion layer 交互的. ingestion layer 被设计为能处理 trillion (1,000,000,000,000) 条数据每秒. 在写入 storage layer 之前, 可以检测 duplicate data 并自动去重, 并且会将数据写入到多个 availability zone.

**Storage Architect**:

写入数据时, 数据存储层会自动对数据进行索引. Timestream 存储层分为两部分, 热数据用内存存储, 冷数据用磁盘存储. 天生支持 data retention policy. 满足一定条件自动将数据从内存转移到磁盘. 转移到磁盘后, 数据会用一种高度优化的格式进行保存, 并且磁盘存储也支持 data retention, 自动删除太久的过期数据.

**Query Architect**:

查询层的运算是运行在完全独立于 ingestion 和 storage layer 的运算节点上的. 无需做任何特殊处理即可同时查询位于 内存 和 磁盘 上的数据, 查询引擎会自动优化和汇总结果.

**Cellular Architect**:

为了能保证 scale 容易, Timestream scale 的基础单位是 Cell. 一个 Cell 打包了一整套 ingestion, storage, query layer. 同时用一个类似于 Load balancer 的 timestream-write 和 timestream-query discovery endpoint 与外界通信, endpoint 会自动路由请求.


Writes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Timestream 支持的数据类型有:

1. BIGINT
2. BOOLEAN
3. DOUBLE
4. VARCHAR

**No upfront schema definition**

和 Dynamodb 类似, 创建 Database 和 Table 的时候无需指定 Schema. 在写入的时候设计好 Schema 即可.

**Duplicate data**

如果 Dimension, measurement name, measurement value, timestamp 都一样, 则会被判定为 duplicate 数据.

**Writing data (Inserts and Upserts)**

对于同一个 record 的多个写操作并发时, Timestream 用的是 first write win 的模型. 如果你需要 last write win 的模型.

**Batch Writes**

1. 在一个 request 中批量写入数据有助于提高性能和节约开支.
2. 在 batch 写入时, batch 不是原子操作, 可能有部分写入成功, 部分被拒绝.

**Eventual consistency for reads**

Timestream 使用的是 Eventual consistency for read. 也就是说如果你对某条数据有更新, 你有可能读取到的是旧数据. 而如果你插入了很多新数据, 查询返回的结果中可能并不包含这些数据, 哪怕他们理应被 query 所返回.


Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当写入到数据库时, 数据首先被写入到 memory 中, 并且会快速复制到其他 availability zone. 保证了即使一个节点挂掉, 数据依然还在.

**Time delay and future in Write**

你写入数据时, ingestion layer 会将 timestamp 与服务器时间做比较, 如果 timestamp 是历史数据并且超前的时间已经超过了 retention 的时间, 那么会拒绝写入. 你无法直接将数据跳过 memory, 直接写入 disk. 而如果 timestamp 是发生在未来, 如果超过的时间不超过 15 分钟, 那么是可以被接受的. 而如果超过太多, 则也会被拒绝写入. 这个设置可以被修改.

在 memory 中的数据被视为热数据, 并且支持 point-in-time query, 也就是可以将查询运行在过去某个时间节点上的数据库状态上. 而 disk 中的数据被视为历史数据, 不支持 point-in-time.

如果你需要写入许多比较久的历史数据, 你可以把 memory retention 提高到最大, 写入后将 memory retention 改回来即可.

**Change Retention Policy**

- increase Memory Retention time: 之前是 2 小时, 你修改为 24 小时, 此时 memory storage 会一直继续接受数据, 直到最老的数据已经是 24 小时之前的了, 然后将旧数据转移到磁盘. 但是 timestream **不会** 立刻在修改生效后, 将磁盘中落后现实 2 ~ 24 小时的数据读回 memory.
- increase Memory Retention time: 之前是 24 小时, 你修改为 2 小时, 此时 memory storage 会立刻将落后 2 ~ 24 小时的数据转移到磁盘.


Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Timestream 的查询引擎是用 Presto 实现的. Presto 是一个分布式, in-memory 的查询引擎. 而对于用户而言, 用户使用 SQL (AWS 基于 Presto 实现的 Timestream SQL 方言) 进行查询.


Best Practice
------------------------------------------------------------------------------

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Data Modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Timestream 和一般的 NoSQL 很不相同. 它是为基于时间的查询和时间相关的计算函数高度优化的数据库.

在 MongoDB 或是 Dynamodb 中, 你除了 primary key / hash key / partition key, 你可以为每条记录加入任意多的 key value pair. 而在 Timestream 中每条记录只能有 MeasureName, MeasureValue, MeasureType, Time, TimeUnit, Version. 你无法给每个独立的 record 指定其他自定义的字段. 对于这一问题但 Timestream 有自己的解决方式.

Timestream 的 Table 里有 Timeseries 的概念, 一个 Table 可以有很多 Timeseries, 这些 timeseries 是逻辑概念, 不是实体概念. 在一个 timeseries 中的所有 record, 共享使用 timeseries 所关联的 dimensions 数据. 说白了就相当于 如果许多 record 有共同的属性和值, 那么他们就构成一个 timeseries, 这些共同的属性就是 dimensions.

Timestream Limit 限制 https://docs.aws.amazon.com/timestream/latest/developerguide/ts-limits.html:

