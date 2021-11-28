.. _dynamodb-pricing:

DynamoDB Pricing
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:



1. 简介
------------------------------------------------------------------------------

Dynamodb 的收费模型是依据你读了多少数据以及写了多少数据来进行收费的. 而这个读了多少数据和写了多少数据时有最小单位的, 分别叫 Read Request Unit (RRU) 和 Write Request Unit (WRU). 如果实际的读写比特小于这个则向上取整. 详情请参考 :ref:`RRU 和 WRU 的详细文档 <dynamodb_rru_wru>`.

Dynamodb 还有两种收费模式, 分别叫 On-Demand 和 Provisioned. 简单来说 On-Demand 就是你用了多少就 Charge 你多少, 但是单价会比较贵. Provisioned 则是你预设一个值, 超过这个值的请求就会收到报错的回复. 详情请参考 :ref:`On-Demand 和 Provisioned 的详细文档 <dynamodb_on_demand_provisioned>`.


.. _dynamodb_rru_wru:

2. RRU WRU 详解
------------------------------------------------------------------------------



.. _dynamodb_on_demand_provisioned:

2. On Demand 和 Provisioned 详解
------------------------------------------------------------------------------

