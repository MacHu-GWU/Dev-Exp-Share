How to determine if Amazon DynamoDB is appropriate for your needs, and then plan your migration
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Reference:

- How to determine if Amazon DynamoDB is appropriate for your needs, and then plan your migration: https://aws.amazon.com/blogs/database/how-to-determine-if-amazon-dynamodb-is-appropriate-for-your-needs-and-then-plan-your-migration/
- Best Practices for Migrating from an RDBMS to Amazon DynamoDB: https://d1.awsstatic.com/whitepapers/migration-best-practices-rdbms-to-dynamodb.pdf

Is DynamoDB right for your use case?
------------------------------------------------------------------------------
You should consider using DynamoDB if you:

- Have had scalability problems with other traditional database systems.
- Are actively engaged in developing an application or service.

    It doesn’t always make sense to migrate legacy applications that are not under development, unless you’re willing to invest time and effort to reimplement the data access layer, inline SQL code, or the stored procedures and functions of that application.

- Are working with an online transaction processing (OLTP) workload.

    High-performance reads and writes are easy to manage with DynamoDB, and you can expect performance that is effectively constant across widely varying loads.

- Are deploying a mission-critical application that must be highly available at all times without manual intervention.

    Dynamodb is Highly Available, low Ops.

- Are understaffed with respect to management of additional database capability and need to reduce the workload of your operations team.

- Require a high level of data durability, regardless of your backup-and-restore strategy.

- Have insufficient data for forecasting peaks and valleys in required database performance.


DynamoDB suitability guidelines
------------------------------------------------------------------------------
Before deciding to use DynamoDB, you should be able to answer “Yes” to most of the following evaluation questions:

- Services that require ad hoc query access. Though it’s possible to use external relational frameworks to implement entity relationships across DynamoDB tables, these are generally cumbersome.
- Online analytical processing (OLAP)/data warehouse implementations. These types of applications generally require distribution and the joining of fact and dimension tables that inherently provide a normalized (relational) view of your data.
- Binary large object (BLOB) storage. DynamoDB can store binary items up to 400 KB, but DynamoDB is not generally suited to storing documents or images. A better architectural pattern for this implementation is to store pointers to Amazon S3 objects in a DynamoDB table.

Some unsuitable workloads for DynamoDB include:

- Services that require ad hoc query access. Though it’s possible to use external relational frameworks to implement entity relationships across DynamoDB tables, these are generally cumbersome.
- Online analytical processing (OLAP)/data warehouse implementations. These types of applications generally require distribution and the joining of fact and dimension tables that inherently provide a normalized (relational) view of your data.
- Binary large object (BLOB) storage. DynamoDB can store binary items up to 400 KB, but DynamoDB is not generally suited to storing documents or images. A better architectural pattern for this implementation is to store pointers to Amazon S3 objects in a DynamoDB table.

DynamoDB migration planning
------------------------------------------------------------------------------

1. Developer training
2. Data conversion
3. Data migration
4. Consistency model
5. Security – encryption
6. Network security – VPC endpoint for DynamoDB
7. Performance – throughput and auto scaling
8. Required performance – microseconds versus milliseconds?
9. Reliability considerations
10. Regional resiliency
11. Optimizing capacity and spending
