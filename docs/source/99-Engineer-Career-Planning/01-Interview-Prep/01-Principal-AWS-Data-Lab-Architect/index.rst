AWS Principal Data Lab Architect
==============================================================================

.. contents::
    :depth: 1
    :local:


Interview Prep Overview
------------------------------------------------------------------------------

关于 Position:

- Job Description: https://amazon.jobs/en/jobs/871592/data-lab-architect
- AWS Data Lab overview: https://aws.amazon.com/aws-data-lab/
- AWS Data Lab FAQ: https://aws.amazon.com/aws-data-lab/faqs/

From the overview information, AWS Data Lab Architect (DLA) is to help customer to build a solution on customer's own AWS environment to solve their problems.

It take care of one customer every week. 1 days for collecting information, preparation environment, demo, follow up after workshop. 4 days working with customers, helping them implement POC project.

DLA provides solutions that primarily covers:

- **Database Migrations**
- **Data Lake Creation**
- **Predictive Analytics**
- **Graph and microservices development**

关于 Onsite 面试流程:

On-Site 面试一共有 5 轮, 每轮会有 1-2 个人进行面试, 并且会有 Observer 在旁边观看整个流程, Observer 可能是新手面试官来学习如何面试的, 并不是来观察流程是否需公平公正的.

考察的内容主要两个大方面:

1. Leadership Principal Data points: 就是 Behavior Interview, 看你的做人做事, mindset, team player, leadership 等 soft skill
2. Functional Data points: 技术面, 就是与具体职位密切相关的硬技术.

其中 Leadership Principal 给了三个建议:

1. don't use same story multiple times, if have to, be frank to tell that "I am using the same story, but not from different aspect".
2. repeat phrase from Leadership Principal is allowed.
3. asking question when you need to, like re-define the questions, asking for more context information.

而 Functional 主要考察几个方面:

1. width, 技术广度, 看你的知识面
2. depth, 技术深度, 看你在某几个方面的技术深度, 可能是根据此职位的需求考察职位相关技能, 也可能是你自己挑选你自己最擅长的技能
3. 这个职位是 Data Lab Architect, 那么会考察相关的 Data Modeling, Big Data Solution.


Leadership Principal 准备
------------------------------------------------------------------------------


技术广度准备
------------------------------------------------------------------------------

我有下面这些核心技术, 每一项的经验都达到了一个接近或超过 Senior Level 的深度.

.. contents::
    :depth: 1
    :local:


Data Engineering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ETL
    - Transformation
    - Data Structure Conversion, Columnar Format
- Data Lake and Data Warehouse Creation
    - S3 as Data Lake, Partition and Bucketing
    - Athena / Redshift as Data Warehouse
    - Kinesis as data ingesting
    - Lambda as ETL pipeline
- Web Crawling
    - My distributive AWS Native Web Crawler framework. AWS Lambda + SQS + DynamoDB / MongoDB / RDS
    - My scheduled targeting web crawler framework, crawlib


Machine Learning and Data Analytics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Feature Engineer
- Predictive Modeling
    - Linear Regression
    - Logic Regression
    - Random Forest
    - Bayesian Network
    - Neural Network
    - MML
- Training, Testing
- Evaluation Metrics
    - Accuracy
    - AUG (False Positive, etc ...)
    - ROC
- HyperParameter Tuning
- Model Deployment


Cloud Architect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Computation
    - EC2
    - ECS
    - AWS Lambda
- Network
    - VPC
- Storage
    - S3
    - Dynamodb
    - RDS
    - Redshift
- MiddleWare
    - SQS
    - SNS
    - API Gateway
- Security
    - IAM
    - KMS
    - Secret Manager
- Monitor
    - Cloudwatch
    - Cloudtrail
- Big Data
    - Athena
    - Glue
    - Redshift
    - Kinesis
    - QuickSight
    - EMR


Microservice Architect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Microservice Architect Design
    - Client Side Code
    - Server Side Code
    - API Gateway
    - Service Registration
    - Deployment
    - Testing
    - Orchestration
    - Runtime Customization
- Microservice Practice on AWS
    - API Gateway
    - Deployment
    - Concurrency
    - Orchestration, Step Function
    - ETDC / Zookeeper
    - Chaos Engineering
- Development Framework
    - Serverless
    - Charlies
    - LbdRabbit


Software Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Web App Development
- Desktop App Development
- Backend Service
- Middleware
    - logging
    - message queue
    - pub-sub
- API Server
    - Rest API
    - GraphQL
- Software Design Pattern
    - Factory


DevOps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Linux Server
    - System Admin
    - Packer
- Docker Container
    - Docker Build
    - Docker Registration
    - Docker Compose
    - Docker Swarm, K8S, Farget
- CI/CD Pipeline
    - AWS Code Pipeline
    - CircleCI
    - Jenkins
- Config / Parameter Management
- Automation Script, Shell Scripting
- Command Line Tool Development
- Infrastructure as Code
    - Terraform
    - Troposphere_mate
- Deployment Pattern
    - Blue Green
    - Rolling Upgrade
    - Canary Deployment
    - Feature Toggle
    - A/B Test
    - Shadow Test


Database Engineer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Database Modeling
    - Normalized Data Modeling in Relation Database
    - De-normalized Data Schema
    - Index Strategy
    - Query Optimization
    - User Management
    - Backup Restore
- NonSQL
    - MongoDB
    - DynamoDB
    - Redis
    - Elastic Search
- OLAP
    - Redshift
        - Schema Design
        - Query Optimization
        - Compression
- Database for Hacker
    - Sqlite
    - ETCD
- Database Migration
    - DMS STC (Schema Transform Convertion), Source endpoint, Target endpoint, Replication Instance.


技术深度准备
------------------------------------------------------------------------------


Microservices Architect in general and AWS best Practice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Pro-Con
- Client Code Server Code
- API Gateway
- Error Hanlding
- Scaling
- Orchestration
- Monitoring
- Deployment Strategy
- Testing


Big Data Architect Data Collection, Data Warehouse, BI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Collection
- Storage
- Processing
- Analytics
- Visualization
- Security


Machine Learning Powered Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Classification, Regression
-


Story
------------------------------------------------------------------------------




Huron Consulting Group Data Platform Build Lab
------------------------------------------------------------------------------

Designed and implemented a centralized data pipeline and data lake that collect data from different source.

**S**:

I had a 1 Billion consulting firm customer. Their main consulting practices are healthcare, higher education, and data management & analytics. The Data platform team is supposed to be built in a more generic way to handle a majority of use cases from the practices.

**T**:

1. Advanced data security and access control, adding column and row level access management to existing security model. (AWS Lake Formation)
2. Improved fault tolerance and error tracing in data pipeline. Capability to replay ETL from last success. (Enable Glue Bookmark, Use Dynamodb to Store runtime data, state information)
3. Expand analytics capability, allowing analytic query on multiple state of the data. Now they can only visit the purpose-built (last state of the data) dataset in postgres but cannot query the intermediate(Add to Glue Catalog, Use Athena to query the data)
4. Reduce Ops effort and increase error visibility using serverless orchestration AWS service. (Use step function)

**A**:

1. There are too many principal and resources. Currently they are using Catalog Policy to define list of IAM Role (Principal) that can access the Catalog. But it doesn't scale, So I come up with a Tag based access control model using AWS Lake Formation. Also, data location permission is implemented to avoid cascade update (User who don't have direct access to certain dataset may create a data crawler to crawler those data into a data catalog that they already have access to.)
2. In AWS Glue, we enabled the bookmark strategy so we can replay from last success instead of start-over. Also I introduced using Dynamodb to store state information for each files, and also read and write runtime configuration data.
3. I created a cron job that run AWS Glue Crawler to update the Catalog Data Schema, and use the Hive ``MSCK REPAIR TABLE`` command to capture newly added partition. Now the customer can use AWS Athena to analyze the Data
4. They are having trouble connecting multiple ETL job together and implement the transition logic. They don't have enough engineer resource to maintain a dedicated orchestration. I introduced the AWS Step Function, gave customer a comprehend tutorial about how to implement orchestration pattern like conditional branching, forking for parallel, and merging.

**R**:

1. The pipeline has processed 300+ datasets from “Origin” to “Purpose-built” bucket using AWS Glue Job with in 24 hours.
2. The customer is able to query and join the two pre-defined datasets in purpose-built bucket, create a visualization chart in AWS QuickSight.
3. Successfully run the 3 steps ETL pipeline in AWS Step Function.


Capital One Decentralized Data Access in Data Mesh Project
------------------------------------------------------------------------------

**S**:

The customer has been all in AWS for 8 years. Currently they use centralized data infrastructure and data lake. However it no longer adapt fast growing requirement of data lake and data application. A new group will takes very long to adapt the existing infra. Also, managing data access and data sharing for mass amount of dataset and personal becomes a problem.

**T**:

The customer collected some documentations and suggestion from AWS about the best practice in AWS. They are looking for an AWS Partner helps them to implemented the pattern and help with the adoption.

1. implement the pattern
2. help with the adoption

**A**:

1. implement the pattern: I created a decentralized data mesh + data lake solution that sharing the data infrastructure automation across group. And allow individual team use their own account to build their own data lake and application. I create a Lake Formation strategy that allow data admins to securely share the data across teams / AWS Account.
2. help with the adoption:
    - I noticed that there are lots of existing data management pattern in different Data Team. Some of them are ready to adapt the new pattern some are not. I created an internal tools that helps them create the required AWS resources, test the new pattern, and delete the old method.
    - In order to spread the new pattern to the entire organization. I decide to start with introducing this pattern in several isolated business unit, such as credit card unit, banking unit, cash flow unit. Enabling this with in several "clusters", fully test this pattern. Then start raising inter-clusters connection. 如果单点测试, 根本测试不出来在数据网络连接状态下系统的行为. 如果联网测试, 错误的影响面太大了, 一旦出错, 影响范围太大. 所以我的方案是最 Balanced 的.

**Result**:

1. I helped the customer deploy this solution into credit card unit and ML product unit. Allow ML product unit to share demographic to credit card unit, and share to transaction status data to ML product unit.
2. Results in reduced technique overhead, improved productivity and data security.
3. They plan to spread this pattern to more business unit.


FirstGroup Sync App DynamoDB to Data Lake for Analytics and Business Report
------------------------------------------------------------------------------

**Situation**

The customer is the largest student transportation service provider in North America. They collects thousands of events each day from IoT sensors embedded in their school buses and from operational activities and stores them in DynamoDB as their data store. They are looking to build a Data Lake for their Analytics and Reporting needs and are looking for the recommended way of streaming data from DynamoDB into a Data Lake. They are looking for the best practices and recommendations, Q&A on DynamoDB data modelling, DynamoDB streams scaling, response-times, resiliency, error-handling and restart, etc.

**Task**

I am


**Action**

1. Decide the streaming method: Kinesis Stream vs Lambda vs Full Dump:
    - I evaluated their engineering resources, they are not mature enough to manage KCL for Kinesis, in term of sharding strategy, check point strategy.
    - I analyzed their data ingestion pattern, there are lots of write, lots of read, lots of updates, no deletion. So Full Dump doesn't provide timely data.
2. Optimization: I analytics their existing DynamoDB design, noticed that they use customer id as the hash key and the device id as the sort key. For every DynamoDB partition, there is a corresponding shard and a Lambda function poll for events in the stream (shard). Their workload is not very balanced because some customer may have super big traffic. Since the device id is randomly generated uuid and has high cardinality, so I came up with a optimized "Write Sharding" strategy that use device id as a surfix appended to customer id. So they can still access a record of an device easily, but the workload is evenly distributed.
3. I created a Lambda function that load the incremental data and CDC data into AWS ElasticSearch. And create a QuickSight dashboard to provide near real-time business report.

**Result**

1. Create a pipeline that sync the latest data to Analytics Data Store, enabling the analytic capability.
2. Create a dashboard app on AWS Quicksight to provide live report for Business Stakeholder.

Reference:

- https://aws.amazon.com/pt/blogs/database/dynamodb-streams-use-cases-and-design-patterns/
