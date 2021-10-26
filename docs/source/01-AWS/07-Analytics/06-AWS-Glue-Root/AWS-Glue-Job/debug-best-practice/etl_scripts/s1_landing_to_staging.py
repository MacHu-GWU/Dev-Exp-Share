# -*- coding: utf-8 -*-

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

dataset_name = "bank_accounts"

DataSource = glueContext.create_dynamic_frame.from_catalog(
    database="multi_stage_etl_poc",
    table_name=f"landing_{dataset_name}",
    transformation_ctx="DataSource"
)

def get_mapping_by_dataset(dataset_name):
    mappings = [
        ("acc", "int", "acc", "int"),
        ("ssn", "str", "ssn", "str"),
        ("create_time", "str", "create_time", "str"),
        ("status", "str", "status", "str"),
    ]
    return mappings

mappings = get_mapping_by_dataset(dataset_name)

Transform = ApplyMapping.apply(
    frame=DataSource,
    mappings=mappings,
    transformation_ctx="Transform"
)

DataSink = glueContext.write_dynamic_frame.from_options(
    frame=Transform,
    connection_type="s3",
    format="parquet",
    connection_options={
        "path": f"s3://aws-data-lab-sanhe-for-everything/poc/2021-10-05-multi-stage-etl-job-poc-dataset/02-staging/{dataset_name}/",
    },
    transformation_ctx="DataSink"
)
job.commit()
