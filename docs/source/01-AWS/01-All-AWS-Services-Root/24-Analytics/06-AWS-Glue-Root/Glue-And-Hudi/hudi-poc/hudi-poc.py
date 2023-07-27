import sys
import boto3
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

spark_ctx = SparkContext()
glue_ctx = GlueContext(spark_ctx)
spark_ses = glue_ctx.spark_session

aws_region = "us-east-1"
boto_ses = boto3.session.Session(region_name=aws_region)
aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]


additional_options={
    "hoodie.table.name": "mytable",
    "hoodie.datasource.write.storage.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.recordkey.field": "id",
    "hoodie.datasource.write.precombine.field": "ts",
    "hoodie.datasource.write.partitionpath.field": "year,month,day",
    "hoodie.datasource.write.hive_style_partitioning": "true",
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": "mydatabase",
    "hoodie.datasource.hive_sync.table": "mytable",
    "hoodie.datasource.hive_sync.partition_fields": "year,month,day",
    "hoodie.datasource.hive_sync.partition_extractor_class": "org.apache.hudi.hive.MultiPartKeysValueExtractor",
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.datasource.hive_sync.mode": "hms",
    "path": f"s3://{aws_account_id}-{aws_region}-data/projects/hudi-poc/databases/mydatabase/mytable"
}

df = spark_ses.createDataFrame(
    [
        ("id-1", "2000", "01", "01", "2000-01-01 00:00:00", 1),
        ("id-2", "2000", "01", "02", "2000-01-01 00:00:00", 2),
        ("id-3", "2000", "01", "03", "2000-01-01 00:00:00", 3),
    ],
    ("id", "year", "month", "day", "ts", "value"),
)

(
    df.write.format("hudi")
    .options(**additional_options)
    .mode("overwrite")
    .save()
)

job = Job(glue_ctx)
job.init(args['JOB_NAME'], args)
job.commit()