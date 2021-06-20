Flink Note
==============================================================================

.. contents::
    :depth: 1
    :local:


Flink 3 major components:

- DataSource:
- Transformation:
- DataSink:


Streaming vs Batching:

Major difference:

when to move data from node to node?

- Streaming: process one record, then go
- Batching: process one record, then persistent to buffer. When buffer is fulled, then send to next node

Spark is designed for Batching. Spark supports Streaming via "Spark Streaming", it is actually a "micro batch".


Streaming Framework Comparison:

+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+
|     Product     |         Model        |     API     |    Delivery   | ErrorTolerance |  StateManagement | Latency | Throput |
+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+
|      Storm      | Native (immidiately) |             | at-least-once |   Record ACK   |        No        |   Low   |   Low   |
+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+
|     Trident     |    micro-batching    |             |   exact-once  |   Record ACK   |   Per Operation  |  Middle |  Middle |
+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+
| Spark Streaming |    micro-batching    | declaration |   exact-once  | RDD Checkpoint | based on DStream |  Middle |   High  |
+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+
|      Flink      | Native (immidiately) | declaration |   exact-once  |   Checkpoint   |   Per Operation  |   Low   |   High  |
+-----------------+----------------------+-------------+---------------+----------------+------------------+---------+---------+

