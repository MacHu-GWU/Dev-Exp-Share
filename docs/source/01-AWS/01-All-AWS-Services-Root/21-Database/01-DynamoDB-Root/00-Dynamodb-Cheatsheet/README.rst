.. _dynamodb-cheatsheet:

Dynamodb Cheatsheet
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

What is Dynamodb
------------------------------------------------------------------------------

- Key / Value store
- No SQL
- Schemaless
- Cloud Native, AWS Managed, low Ops
- Highly Available
- Easy to integrate with other AWS Service, suche as AWS
- Support Transaction, Strong Consistent Read

Dynamodb Pricing
------------------------------------------------------------------------------

- :ref:`Write Request Unit <dynamodb_rru_wru>`
    - Transaction write
- :ref:`Read Request Unit <dynamodb_rru_wru>`
    - Eventual consistence read
    - Strong consistence read
    - Transaction read

Data Modeling
------------------------------------------------------------------------------

- Hash Key and Range Key
- Partition and Data Distribution
- Global Secondary Indexes
- Local Secondary Indexes
- One to One Relationship
- One to Many Relationship
- Many to Many Relationship

Design:

- Versioned document
- Cumulated value

CRUD
------------------------------------------------------------------------------

- Read
    - Scan
    - Query
    - Use index
- Write
    - single vs batch
- :ref:`Transaction <dynamodb-transaction>`
- Delete

DBA Ops
------------------------------------------------------------------------------

- :ref:`Backup <dynamodb-backups>`
    - On-demand AWS Backup
    - On-demand Dynamodb Backup
    - Point-in-time Backup


Security
------------------------------------------------------------------------------

- Data Protection
    - Encryption at Rest
    - Inter Network traffic privacy
        - between AWS service and on-premises: option1, AWS Site-to-Site VPN; option2, AWS Direct Connect
        - between AWS resources in the same region: VPC endpoint
- Authentication
    - IAM role based access


In-memory Acceleration with DAX
------------------------------------------------------------------------------



