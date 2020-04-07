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