TimeStream Data Modeling
==============================================================================



What is the Right Data Model for TimeSeries Data?
------------------------------------------------------------------------------
我们先来分析时间序列数据的需求是什么. 首先我们来看一个气象传感器的例子. 气象局在全国各地部署了很多传感器, 每个传感器有自己的 ID, 以及地理位置信息. 这些 传感器 (Device) 可以测量 (Measurement) 多种不同的数据, 例如 温度 (Temperature), 湿度 (Humidity). 然后我们希望将传感器的数据每隔 1 分钟就打包通过卫星网络发送给气象局的数据中心里. 这样我们就可以对其进行实时的分析, 并预测天气了.

我们先考虑一下数据应该长什么样. 首先每个传感器有自己的 Metadata, 例如 ID, 型号, 坐标, 高度, 等等. 我们希望能在数据中看到一条数据, 就知道这条数据是来自于哪个传感器的. 显然由于数据量巨大, 如果我们在每条数据中都包含传感器的 Metadata, 那重复的数据量也太大了. 在 AWS TimeStream 中, 时序数据的 Metadata 也被称为 Dimension. 因为在 SQL 中, 这些重复信息通常是以 Dimension Table 作为外表存在的, 需要的时候只要做一个 JOIN 即可, 由此得名. 例如::

    # fact table
    device_id   timestamp   temperature    humidity
    d-1         08:30:00    24.5            0.33
    d-1         08:31:00    24.6            NULL
    d-1         08:32:00    24.7            0.36

    # dimension table
    device_id   lat     lng
    d-1         33.7    -72.8

然后每个传感器会有不同的测量值, 有的时候在一个瞬间, 我们同时有温度和湿度的测量值. 但有的时候一个瞬间我们只有稳定. 如果用 SQL 的思维, 我们通常有两种方式对其数据建模:

1. Single-Measure, 每一条记录只记录一个测量值::

    device_id   timestamp   measurement_name    measurement_value
    d-1         08:30:00    temperature         24.5
    d-1         08:31:00    temperature         24.6
    d-1         08:32:00    temperature         24.7
    d-1         08:30:00    humidity            0.33
    d-1         08:32:00    humidity            0.36

2. Multi-Measure, 每一条记录记录多个测量值, 如果有的测量值不存在, 则为 Null::

    device_id   timestamp   temperature    humidity
    d-1         08:30:00    24.5            0.33
    d-1         08:31:00    24.6            NULL
    d-1         08:32:00    24.7            0.36

在 SQL 的世界里第一种情况其实是由问题的, 因为不同的 measurement 的 value 的数据类型可能不同, 你无法用一个 Column 搞定所有的 measurement.

在时序数据库的世界里, 各个产品的方案是有所不同的.


AWS TimeStream Data Modeling
------------------------------------------------------------------------------
现在我们来看一下 AWS TimeStream 是怎么解决这个问题的.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Single Table vs Multi Tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
首先你要考虑的是, 你准备用一个 Table 还是用多个 Table. 例如在 OpenTSDB 里采用的就是 Single-Measure, 由于 Type 的不同, 所以它只能为每一个 Measurement 创建一个关系表. 而在 AWS TimeStream 里, Data Retention Policy, Table Level Access Control 都是 Table 级别的, 如果你需要为不同的数据设置不同的这些设定, 那么你肯定得分表. 其次就是要考虑你的 Query Pattern, 如果你的 Query 总是要扫描几个表最后汇总, 那么这几个表可能不如直接用一个表代替会更好. 在 AWS TimeStream 里, 担心单表数据过大导致性能变差不是我们要考虑的.


Multi-measure records vs. single-measure records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们上面的例子已经看到了两种表结构的不同了. 简单来说, 如果能上 Multi measure 肯定尽量上, 因为查询效率更高, 不必要的数据聚合步骤处理更少. 能上 Multi measure 的主要条件是你在同一个 Timestamp 下是不是真的会同时采集几个数据点, 或者说大部分的数据点. 如果你有 10 个指标,  但经常同一时间只有 2-3 个指标, 这会导致数据非常稀疏, 肯定不合适.


Dimensions and measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们已经了解了 Dimension 就是 metadata, 可以理解为 key value pair. AWS 有以下官方建议:

1. Dimension 的数据不能够随着时间变化, 不然会导致严重的逻辑错误.
2. Dimension 的 key value pair 数据不能超过 2KB, 一个 Table 中所有的 Dimension 不能超过 128 个 Pair.
3. 如果你的数据里有 request_id, invoke_id 等类似于 uuid 的字段, 那么不要将其放在 Dimension 中, 而是将其视为一个 Measure.


Using measure name with multi-measure records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AWS TimeStream 里有一个特殊字段 ``measure_name`` (Multi 和 Single Measure 都有). 如果你用的 Single Measure 模型, 那么这个字段显然是应该放你的 Measure Name, 例如 Temperature, Humidity. 那在 Multi Measure 模型下我们应该放什么? 以及这个字段对架构, 性能, 使用有什么影响呢?

AWS TimeStream 用 ``measure_name`` 这个字段来做 Partition 和 Index. 如果你的查询里有 ``WHERE measure_name = "temperature"`` 这样的条件, 那么就可以用 push down predicate, 避免扫描不必要的数据.z

Timestream uses the values in the measure name attribute to partition and index the data. Therefore, if a table has multiple different measure names, and if the queries use those values as query predicates, then Timestream can use its custom partitioning and indexing to prune out data that is not relevant to queries. For instance, if your table has cpu and memory measure names, and your query has a predicate WHERE measure_name = 'cpu', Timestream can effectively prune data for measure names not relevant to the query, i.e., rows with measure name memory in this example. This pruning applies even when using measure names with multi-measure records. You can use the measure name attribute effectively as a partitioning attribute for a table. Measure name along with dimension names and values, and time are used to partition the data in a Timestream table. Please be aware of the limits on the number of unique measure names allowed in a Timestream table. Also note that a measure name is associated with a measure value data type as well, i.e., a single measure name can only be associated with one type of measure value. That type can be one of DOUBLE, BIGINT, BOOLEAN, VARCHAR, and MULTI. Multi-measure records stored with a measure name will have the data type as MULTI. Since a single multi-measure record can store multiple metrics with different data types (DOUBLE, BIGINT, VARCHAR, BOOLEAN, and TIMESTAMP), you can associate data of different types in a multi-measure record.

Below we discuss a few different examples on how the measure name attribute can be effectively used to group together different types of data in the same table.