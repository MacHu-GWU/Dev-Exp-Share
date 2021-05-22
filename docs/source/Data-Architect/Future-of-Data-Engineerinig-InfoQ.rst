Data Engineering Definition

This is just my personal Definition:

    What:

        A data engineer's job is to help a organization move and process data

    How:

        Data engineers build tools, infrastructure, framework, and services



There are three stages of data pipeline maturity:

1. Land (batch, few system integrated)
2. Expand (realtime, many system integrated)
3. On Demand (self-serve, automated tooling, data catalog, MDM (master data management), DataOps, data mesh)

Six Stage of data pipeline maturity:

0. None
1. Batch
2. Realtime
3. Integration
4. Automation
5. Decentralization


0. None

Architect::

    [Monolith] <---> [DB] <--- Data Consumer

    [Php Monolith] <---> [Mysql] <--- Data Consumer

Problems:

- Queries began time out
- Users were impacting each other
- MySQL was missing complex analytics SQL functions
- Report generation was break


1. Batch

You might be ready for batch if ...

- You have monolithic architecture
- Data engineering is your part-time job
- Queries are timing out
- Exceeding DB capacity
- Need complex analytical SQL functions
- Need reports, charts, and business intelligence

Architect::

                               +-------------------------------+
                               |                               |
    [Monolith] <---> [DB] ---> [Scheduler] ---> [Data Warehouse] <--- Data Consumer
                               |                               |
                               +-------------------------------+

Problems:

- Large number of Airflow jobs for loading all tables
- Missing and inaccurate create_time, and modify_time
- DBA operations impacting pipeline
- Hard deletes weren't propagating
- MySQL replication latency was causing data quality issue
- Periodical loads cause occasional MySQL timeouts

2. Realtime

You might be ready for realtime if ...

- Loads are taking too long
- Pipeline is no longer stable
- Many complicated workflows
- Data latency is becoming an issue
- Data engineer is your full time job
- You already have Apache Kafka in your organization

Architect::

                               +-------------------------------+
                               |                               |
    [Monolith] <---> [DB] ---> |     [Streaming Platform]      | ---> [Data Warehouse] <--- Data Consumer
                               |                               |
                               +-------------------------------+

Problems:

- Pipeline for Datastore was still on Airflow
- No pipeline at all for Cassandra or Bigtable
- BigQuery needed logging data
- Elastic search needed data
- Graph DB needed data

3. Integration

You might be ready for integration if ...

- You have microservices
- You have diverse database ecosystem
- You have many specialized derived data systems
- You have a team of data engineers
- You have a mature SRE organization

Metcalfe's Law: value of a networking increase exponentially more node and edge you added to it

4. Automation

You might be ready for automation if ...

- Your SRE can't keep up
- You are spending a lot of time on manual toll
- You don't have time for the fun stuff

Automation Data Management

- Data Catalog
- Access: RBAC (Role based access control) / IAM / ACL (access control list)
- DLP (Data Lose Prevention)

Automation Operations

- orchestration
- monitoring
- configuration

if a human operator needs to touch your system during normal operations, you have a bug -- Carla Geisser, Google SRE

Normal Operations:

- Add new channel to replica MySQL DB
- Create and configure Kafka topics
- Add new Debezium connector to Kafka connect
- Create destination dataset in BigQuery
- Add new KCBQ connector to Kafka connect
- Create BigQuery view
- Configure data quality checks for new tables
- Granting access
- Deploying stream processor or workflows

Automated operations:

- Terraform
- Ansible
- Helm
- Salt
- Cloudformation
- Chef
- Puppet
- Spinnaker

Spending time on Data Management:

- Who get access to this data?
- How long can this data been persisted?
- Is this data allowed in this system?
- Which geographies must data be persisted in?
- Should column be masked?

Automate Data Management:

1. Set up a data catalog
    - Location
    - Schema
    - Ownership
    - Lineage (where it came from)
    - Encryption
    - Versioning
2. Automate management
    - New user access
    - New data access
    - Service account access
    - Temporary access
    - Unused access
3. Detect Violations
    - Auditing
    - Data loss prevention

Problems:

- Data engineers still manages configuration and deployment

5. Decentralization

You might be ready for decentralization if ...

- You have a fully automated realtime data pipeline
- People still come to you to get data loaded

From monolith to micro datawarehouse ...

Partial decentralization

- Raw tools are exposed to other engineering teams
- Requires git, yaml, json, pull requests, terraform commands, etc

Full decentralization

- Polished tools are exposed to everyone
- Security and compliance manage access and policy
- Data engineering manages data tooling and infrastructure
- Everyone manages data pipelines and data warehouses




Integration


Integrate Operation Database with Data Warehouse

你有个 RDBMS 数据库
