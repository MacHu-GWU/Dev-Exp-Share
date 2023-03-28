# -*- coding: utf-8 -*-

import random
from loguru import logger
from datetime import datetime
from dateutil.parser import parse as parse_datetime
import pynamodb
from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import UnicodeAttribute

#
# class ItemOrderIndex(GlobalSecondaryIndex):
#     class Meta:
#         index = "item-and-order-index"
#         projection = KeysOnlyProjection
#
#     item_id = UnicodeAttribute(hash_key=True)
#     order_id = UnicodeAttribute(range_key=True)

class GlueJobLog(Model):
    class Meta:
        table_name = "glue_job_log"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    # define attributes
    run_id = UnicodeAttribute(hash_key=True)
    time = UnicodeAttribute(range_key=True)
    job_name = UnicodeAttribute()
    log = UnicodeAttribute()

    # associate index
    # item_order_index = ItemOrderIndex()


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

run_id = args["JOB_RUN_ID"]
job_name = args["JOB_NAME"]

logger.info(f"job_name = {job_name}, run_id = {run_id}")

dataset_name = "events"

class DynamoDBLogger:
    def __init__(self):
        self.connection = Connection()

    def write(self, log):
        gjl = GlueJobLog(
            run_id=run_id,
            time=str(datetime.utcnow()),
            job_name=job_name,
            log=log,
        )
        gjl.save()

dynamodb_logger = DynamoDBLogger()

dynamodb_logger.write("job start!")


logger.info("start: read source data")
df_in = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": [
            "s3://aws-data-lab-sanhe-for-everything/poc/2021-10-25-debug-best-practice-poc-dataset/events/"
        ]
    },
    format="json",
    transformation_ctx=f"DataSource_{dataset_name}"
)
logger.info("end: read source data")
# logger.info("df_in has {} rows".format(df_in.count()))

def per_row_transform(rec):
    rec["time"] = parse_datetime(rec["time"]).timestamp()
    if not isinstance(rec["value"], int):
        raise TypeError
    return rec

# options = [0, 1]
def per_row_transform_filter(rec):
    from loguru import logger
    # dynamodb_logger = DynamoDBLogger()
    try:
        # dynamodb_logger.write(str(rec))
        per_row_transform(rec)
        return True
    except Exception as e:
        logger.info("start try to log the error")
        logger.error(str(e))
        # print("failed to transform event_id = {} using 'per_row_transform()'".format(rec["id"]))
        return False

logger.info("start: filter good data")
df_tf_1 = Filter.apply(
    frame=df_in,
    f=per_row_transform_filter,
    transformation_ctx=f"Transform_1_{dataset_name}"
)
logger.info("end: filter good data")
# logger.info("df_tf_1 has {} rows".format(df_tf_1.count()))
# logger.info("df_tf_1 has {} error counts".format(df_tf_1.stageErrorsCount()))

logger.info("start: transform the data")
df_tf_2 = Map.apply(
    frame=df_tf_1,
    f=per_row_transform,
    transformation_ctx=f"Transform_2_{dataset_name}"
)
logger.info("end: transform the data")
df_tf_2.printSchema()
# logger.info("df_tf_2 has {} rows".format(df_tf_2.count()))
# logger.info("df_tf_2 has {} error counts".format(df_tf_2.stageErrorsCount()))

logger.info("start: store the output")
n_partition = df_tf_2.getNumPartitions()
logger.info(f"number of partition: {n_partition}")


df_tf_3 = df_tf_2.coalesce(1)
data_sink = glueContext.write_dynamic_frame.from_options(
    frame=df_tf_3,
    connection_type="s3",
    format="parquet",
    connection_options={
        "path": f"s3://aws-data-lab-sanhe-for-everything/poc/2021-10-25-debug-best-practice-poc-dataset/events_parquet/",
    },
    transformation_ctx=f"DataSink_{dataset_name}"
)
logger.info("end: store the output")

job.commit()
