.. _kinesis:

Kinesis - Path to Master
==============================================================================
Keywords: AWS Kinesis

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Basic
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Kinesis Architect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. raw:: html
    :file: ./kinesis-architect.html


Kinesis vs Kafka
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Advance
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Throughput Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Optimize Producer - Choose the right Partition Key
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
1. choose the key high cardinality, like order id, device id if N >> n_shard
2. if you have to use low cardinality key for strong ordering purpose, you can append suffix
3. if ordering doesn't matter, you can append random suffix


Optimize Producer - Batch
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
without batch::

    events = [
        {"device_id": 1, "time": "2022-01-01 00:01:00", "measurement": "temperature", "value": 76.1},
        {"device_id": 1, "time": "2022-01-01 00:02:00", "measurement": "temperature", "value": 76.2},
        {"device_id": 1, "time": "2022-01-01 00:03:00", "measurement": "temperature", "value": 76.3},
        ...
    ]

    # many API call
    for event in events:
        kinesis_client.put_record(
            ...
            Data=json.dumps(event).encode("utf-8"),
            PartitionKey=event["device_id"],
        )

with batch::

    # single API call
    kinesis_client.put_records(
        ...
        Records=[
            {
                "Data": json.dumps(event).encode("utf-8"),
                "PartitionKey": event["device_id"],
            }
            for event in events
        ],
    )


Optimize Producer - Aggregation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
without aggregation::

    temperature_measurement_events = ...
    humidity_measurement_events = ...
    ...

    kinesis_client.put_records(
        ...
        Records=[
            {
                "Data": json.dumps(event).encode("utf-8"),
                "PartitionKey": event["device_id"],
            }
            for event in temperature_measurement_events
        ],
    )

    kinesis_client.put_records(
        ...
        Records=[
            {
                "Data": json.dumps(event).encode("utf-8"),
                "PartitionKey": event["device_id"],
            }
            for event in humidity_measurement_events
        ],
    )

with aggregation::

    import gzip

    kinesis_client.put_records(
        ...
        Records=[
            {
                "Data": gzip.compress(json.dumps(temperature_measurement_events).encode("utf-8")),
                "PartitionKey": temperature_measurement_events[0]["device_id"],
            },
            {
                "Data": gzip.compress(json.dumps(humidity_measurement_events).encode("utf-8")),
                "PartitionKey": humidity_measurement_events[0]["device_id"],
            },
            ...
        ],
    )


Optimize Consumer - Slow Consumer
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.. raw:: html
    :file: ./optimize-consumption-slow-consumer.html

- Trade off: you have to ensure "atomic" for each read


Optimize Consumer - Aggregation First
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Aggregate many records into one consumption action. Example: each event is a data change event of Dynamodb stream (update event), you can merge before writing to target database.

.. raw:: html
    :file: ./optimize-consumption-aggregation-first.html


Multi Tenant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
What is Multi Tenant in the Context of Message Streaming Middleware System:

Why Multi Tenant:

    1. smooth the traffic.
    2. n_tenant is too large, it is impossible to maintain an independent infrastructure for each tenant.

Multi Tenant Challenge:

    1. one tenant's consumer should not consume data owned by other consumer
    2. one tenant's slow consumer should not impact the entire system

Kinesis Quota:

    1. There is no upper quota on the number of streams with the provisioned mode that you can have in an account.
    2. The default shard quota is 500 shards per AWS account for the following AWS regions: US East (N. Virginia), US West (Oregon), and Europe (Ireland). For all other regions, the default shard quota is 200 shards per AWS account. This limit is only applicable for data streams with the provisioned capacity mode.

Solutions:

1. Per Tenant Stream
    - pro:
        - physical isolation
        - easy to add / remove tenant
        - producer / consumer of different tenants can be maintained and deployed independently
    - con:
        - read / write IO waste
        - cannot handle large number of tenant
    - use case:
        - all tenant has small traffic, or big but predictable traffic
        - n tenant is not too big >= 500
2. Per Tenant Consumer
    - pro:
        - producer / consumer of different tenants can be maintained and deployed independently
    - con:
        - read IO waste
        - get records API has 5 TPS limit
            - you cannot have >= 5 consumer read at the same time
            - if you have 300 consumer, then the buffer time (delay time) is 300 / 5 = 60
        - cannot fully utilize "aggregation"
    - use case:

3. One Stream, One Consumer, logical isolation
    - pro:
        - no waste
        - easy to scale for both producer / consumer
    - con:
        - stickiness of the code
        - update for one tenant "May" have global impact
        - cannot fully utilize "aggregation"

.. raw:: html
    :file: ./kinesis-multi-tenant.drawio.html

Reference:

- Kinesis Quota and Limit: https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html


Stream Scalability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`kinesis-resharding-a-stream`


Failure Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keys:

1. Store shad iterator in Dynamodb
2. Store failed records in dead-letter kinesis stream
3. Persist failed data in s3
4. Copy records in dead-letter stream back to app stream after fix

.. raw:: html
    :file: ./kinesis-failure-handling.html
