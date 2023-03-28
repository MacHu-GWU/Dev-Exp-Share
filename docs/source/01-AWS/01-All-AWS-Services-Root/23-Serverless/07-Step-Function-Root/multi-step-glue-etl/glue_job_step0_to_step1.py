# -*- coding: utf-8 -*-

import sys
from awsglue.transforms import ApplyMapping, Map
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

DataSource0 = glueContext.create_dynamic_frame.from_catalog(
    database="multi_step_glue_etl",
    table_name="step0",
    transformation_ctx="DataSource0"
)


def per_record_change(record):
    record["balance"] = record["balance"] + 1
    return record


Transform1 = Map.apply(
    frame=DataSource0,
    f=per_record_change,
    transformation_ctx="Transform1"
)


DataSink0 = glueContext.write_dynamic_frame.from_options(
    frame=Transform1,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://aws-data-lab-sanhe-for-everything/poc/2021-09-27-multi-step-glue-etl/step1/",
        "partitionKeys": []
    },
    transformation_ctx="DataSink0"
)
job.commit()
