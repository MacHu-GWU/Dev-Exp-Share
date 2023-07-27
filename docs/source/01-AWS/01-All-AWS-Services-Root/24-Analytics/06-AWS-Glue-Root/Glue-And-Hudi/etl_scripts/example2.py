import sys
import boto3

from pyspark.context import SparkContext

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

spark_ctx = SparkContext()
glue_ctx = GlueContext(spark_ctx)
spark_ses = glue_ctx.spark_session

aws_region = "us-east-1"
boto_ses = boto3.session.Session(region_name=aws_region)
aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]

# 这是一个标准的 Hudi table, 其中有一个字段是 time, 用作 hoodie.datasource.write.precombine.field
# Ref: https://hudi.apache.org/docs/configurations/#hoodiedatasourcewriteprecombinefield-1
# 在这个例子中我们没有 partition key, 所有的数据都在 root folder level
df = spark_ses.createDataFrame(
    [
        ("id-1", "2000-01-01 00:00:00", 1, "alice"),
        ("id-2", "2000-01-02 00:00:00", 2, "bob"),
        ("id-3", "2000-01-03 00:00:00", 3, "cathy"),
    ],
    ("id", "time", "value", "name"),
)

database = "mydatabase"
table = "mytable"
additional_options={
    "hoodie.table.name": "mytable",
    "hoodie.datasource.write.storage.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.recordkey.field": "id",
    "hoodie.datasource.write.precombine.field": "time",
    "hoodie.datasource.write.partitionpath.field": "", # 当没有 partition 的时候, 这个 option 设为 ""
    "hoodie.datasource.write.hive_style_partitioning": "true",
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": database,
    "hoodie.datasource.hive_sync.table": table,
    "hoodie.datasource.hive_sync.partition_fields": "", # 当没有 partition 的时候, 这个 option 设为 ""
    "hoodie.datasource.hive_sync.partition_extractor_class": "org.apache.hudi.hive.MultiPartKeysValueExtractor",
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.datasource.hive_sync.mode": "hms",
    "path": f"s3://{aws_account_id}-{aws_region}-data/projects/hudi-poc/databases/{database}/{table}"
}
(
    df.write.format("hudi")
    .options(**additional_options)
    .mode("overwrite")
    .save()
)

job = Job(glue_ctx)
job.init(args["JOB_NAME"], args)
job.commit()
