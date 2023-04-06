
"""
https://us-east-1.console.aws.amazon.com/s3/buckets/awsglue-datasets?region=us-east-1&prefix=examples/us-legislators/&showversions=false
awsglue-datasets/examples/us-legislators

"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [format_options = {"quoteChar":"\"","escaper":"","withHeader":True,"separator":","}, connection_type = "s3", format = "csv", connection_options = {"paths": ["s3://eq-sanhe-for-everything/data/aws-glue-test/before/"], "recurse":True}, transformation_ctx = "DataSource0"]
## @return: DataSource0
## @inputs: []
DataSource0 = glueContext.create_dynamic_frame.from_options(format_options = {"quoteChar":"\"","escaper":"","withHeader":True,"separator":","}, connection_type = "s3", format = "csv", connection_options = {"paths": ["s3://eq-sanhe-for-everything/data/aws-glue-test/before/"], "recurse":True}, transformation_ctx = "DataSource0")
## @type: ApplyMapping
## @args: [mappings = [("id", "long", "id", "long"), ("name", "string", "name", "string")], transformation_ctx = "Transform0"]
## @return: Transform0
## @inputs: [frame = DataSource0]
Transform0 = ApplyMapping.apply(frame = DataSource0, mappings = [("id", "long", "id", "long"), ("name", "string", "name", "string")], transformation_ctx = "Transform0")
## @type: DataSink
## @args: [connection_type = "s3", format = "json", connection_options = {"path": "s3://eq-sanhe-for-everything/data/aws-glue-test/after/", "partitionKeys": ["id"]}, transformation_ctx = "DataSink0"]
## @return: DataSink0
## @inputs: [frame = Transform0]
DataSink0 = glueContext.write_dynamic_frame.from_options(frame = Transform0, connection_type = "s3", format = "json", connection_options = {"path": "s3://eq-sanhe-for-everything/data/aws-glue-test/after/", "partitionKeys": ["id"]}, transformation_ctx = "DataSink0")
job.commit()