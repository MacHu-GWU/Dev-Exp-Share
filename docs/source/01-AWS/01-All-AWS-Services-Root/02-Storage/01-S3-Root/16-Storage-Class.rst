Using Amazon S3 storage classes
==============================================================================

What are storage classes:

- S3 Stardard
- S3 Standard - Infrequent Access (S3 Standard-IA) and S3 One Zone-Infrequent Access (S3 One Zone-IA): Long-lived, but less frequently accessed data
- Glacier: Long-term archive

S3 Standard:

- Data is replicated across at least 3 different availability zones.
- Low latency and high throughput

S3 Standard IA:

- For data that is accessed less frequently, but requires rapid access when needed.
- Data is replicated across 3 different AZs for high durability and availability.
- Cost less than S3-Standard; charges you for retrieving the data per GB (Not based on request)

S3 One Zone IA:

- Same as Standard IA
- Stored in only a single availability zone (AZ)
- 20% less than S3 Standard-IA

Glacier:

Three options for retrieving the archives:

1. Standard: access data in 3-5 hours, 0.01$ per GB
2. Expedited: access data in 1-5 min, 0.03$ per GB, 快, 贵, 急需一批数据时用
3. Bulk: access data in 5-12 hours, 0.0025$ per GB, 慢, 便宜, 不急着用, 可以慢慢获得一批数据时用.

参考资料:

- Archive Retrieval Options: https://docs.aws.amazon.com/amazonglacier/latest/dev/downloading-an-archive-two-steps.html#api-downloading-an-archive-two-steps-retrieval-options
- Access your Amazon Glacier data in minutes with new retrieval options: https://aws.amazon.com/about-aws/whats-new/2016/11/access-your-amazon-glacier-data-in-minutes-with-new-retrieval-options/

- `Using Amazon S3 storage classes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html>`_: