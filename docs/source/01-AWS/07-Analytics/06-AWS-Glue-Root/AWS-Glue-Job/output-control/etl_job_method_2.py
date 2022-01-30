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

dataset_name = "events"

dyf_datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": [
            "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-01-25-output-control/events/",
        ],
    },
    format="json",
    transformation_ctx=f"datasource_{dataset_name}"
)
dyf_datasource_with_less_partitions = dyf_datasource.coalesce(1)

datasink = glueContext.write_dynamic_frame.from_options(
    frame=dyf_datasource_with_less_partitions,
    connection_type="s3",
    format="parquet",
    connection_options={
        "path": "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-01-25-output-control/events-output/",
        "partitionKeys": ["date"]
    },
    transformation_ctx=f"datasink_{dataset_name}"
)

job.commit()
