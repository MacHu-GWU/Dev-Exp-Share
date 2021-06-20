login.gov Data Architect Evolution
==============================================================================



1. None
------------------------------------------------------------------------------

Architect:

- EC2 + Auto Scaling Group + Load Balancer for Web Server
- Dump log to file periodically, use custom script to upload log file to S3
- RDS as backend Database

Problem:

- custom script is not stable when EC2 break or auto-restarted.
    - Hard to handle duplicate data
    - Hard to identify incremental data
    - Hard to implement "exact-once-deliver" upload behavior
- We can not consume / analyze the data
- We want to use log data for debug

Solution:

- **replace the local file log handler with aws cloudwatch put_log_events handler**. the library we use is called watchtower, it implements the buffer and batch upload to optimize throughput.
- use aws logs insights for searching.


2. Data Warehouse + Micro Batch
------------------------------------------------------------------------------

Architect:

- EC2 + ASG + ELB for Web Server
- Use log handler directly put log to AWS Cloudwatch
- Use AWS Cloudwatch Insight for Search

**Problems**:

- Perform Data Analytics for business reports is not easy.
- AWS Cloudwatch insights is expensive.

**Solution**:

- Setup a AWS Redshfit Cluster Datawarehouse
- Use awscloudwatch.create_export_task api periodically dump data to S3
- S3 put_object event triggers AWS Lambda function that transform the data and load to AWS Redshift
- Use aggregation, window function in SQL to query the AWS Redshift for business reports.


3. ETL Improvement
------------------------------------------------------------------------------

**Problems**:

1. AWS Lambda function may fail due to wrong implementation, wrong configuration. While we fixing the ETL, log data is still populating into AWS S3.
2. Sometime Redshift receive duplicate data. It because Redshift primary key restriction doesn't prevent the upload (Natively it is an OLAP). The duplicate may introduce error in our analytics.

**Solution**:

1. Setup a Dead letter queue to collect failed data event. Setup a new AWS Simple Queue to trigger the ETL lambda function. Once the lambda function is fixed, we transfer the data from Dead letter queue to Simple Queue. It triggers the AWS Lambda to "REDO" the failed data.
2. Developed a high performance and efficient customized script that locate duplicate data and precisely delete them.


4. Stream Data Process
------------------------------------------------------------------------------

**Architect**:


**Problems**:

- AWS Redshift is awesome for Data Analyst, but Elastic Search is better for full text search. We want to use ES as the Second Data Sink Target.
- awscloudwatch.create_export_task is not stable enough.
- We don't want to manage

**Solution**:

- Create AWS Kinesis Data Stream, subscribe AWS Cloudwatch Log Group
- Setup AWS Elastic Search Index
- Use Kinesis Firehose to trigger AWS Lambda function that performs ETL job, and eventually load data to Redshift and ElasticSearch.


