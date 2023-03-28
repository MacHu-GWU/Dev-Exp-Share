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

DataSource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options = {"paths": [ "s3://aws-data-lab-sanhe-vpc-endpoint-test/users.csv", ]},
    format="csv",
    format_options=dict(
        withHeader=True,
    ),
    transformation_ctx="DataSource"
)

DataSink = glueContext.write_dynamic_frame.from_options(
    frame=DataSource,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://aws-data-lab-sanhe-vpc-endpoint-test/users.json",
    },
    transformation_ctx="DataSink"
)
job.commit()
