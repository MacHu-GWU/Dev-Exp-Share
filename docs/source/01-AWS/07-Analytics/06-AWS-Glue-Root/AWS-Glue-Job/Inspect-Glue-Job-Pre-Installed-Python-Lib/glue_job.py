# -*- coding: utf-8 -*-

"""
This code can print the list of pre-installed python libraries in glue runtime.

Example:

1. Go to Glue Job Studio Console, create a job
2. Use "Visual with a blank canvas" mode
3. Choose the glue version you want to use
4. Go to Script tab, manually edit the tab
5. Copy and paste this script and Save
6. Click Run
7. Click "output logs" link and read the log
"""

import sys

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

# Since earlier versions of Spark or Pyspark, SparkContext (JavaSparkContext for Java)
# is an entry point to Spark programming with RDD and to connect to Spark Cluster,
# Since Spark 2.0 SparkSession has been introduced and became an entry point.
# And from Spark 3.0 + the SparkContext will be deprecated, however awsgluelib
# still need a SparkContext object to initialize the GlueContext object
# below is a codeblock that works for both pyspark 2.X and 3.X +
from pyspark import __version__ as pyspark_version
if int(pyspark_version.split(".")[0]) <= 2:
    from pyspark.context import SparkContext

    spark_ctx = SparkContext()
    glue_ctx = GlueContext(spark_ctx)
    spark_ses = glue_ctx.spark_session
else:
    from pyspark.sql import SparkSession

    spark_ses = SparkSession.builder.getOrCreate()
    print(spark_ses)
    spark_ctx = spark_ses.sparkContext
    print(spark_ctx)
    glue_ctx = GlueContext(spark_ctx)

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

job = Job(glue_ctx)
job.init(args["JOB_NAME"], args)

from pip._internal.operations import freeze

for pkg in freeze.freeze():
    print(pkg)

job.commit()