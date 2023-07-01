import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "parameter1",
        "parameter2",
    ],
)
print("------ Arguments ------")
print(args)
job.commit()