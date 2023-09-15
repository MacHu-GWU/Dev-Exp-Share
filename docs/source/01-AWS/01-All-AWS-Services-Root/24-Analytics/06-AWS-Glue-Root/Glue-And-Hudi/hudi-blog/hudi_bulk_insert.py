import sys
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, to_timestamp, monotonically_increasing_id, to_date, when
from pyspark.sql.functions import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.types import *
from datetime import datetime
import boto3

args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                    'OUTPUT_BUCKET',
                                    'HUDI_INIT_SORT_OPTION',
                                    'HUDI_TABLE_NAME',
                                    'HUDI_DB_NAME',
                                    'SOURCE_FILE_YEAR'
                                    ])
print(args)
# print("The name of the bucket is :- ",  args['curated_bucket'])
job_start_ts = datetime.now()
ts_format = '%Y-%m-%d %H:%M:%S'
spark = SparkSession.builder.config('spark.serializer','org.apache.spark.serializer.KryoSerializer').config('spark.sql.hive.convertMetastoreParquet','false').config('spark.sql.legacy.pathOptionBehavior.enabled', 'true').getOrCreate()
sc = spark.sparkContext
glueContext = GlueContext(sc)
job = Job(glueContext)
logger = glueContext.get_logger()
job.init(args['JOB_NAME'], args)


def perform_hudi_bulk_insert(
                             hudi_init_sort_option,
                             hudi_output_bucket,
                             hudi_table_name,
                             hudi_db_name,
                             source_file_year
                            ):
    
   
    hudi_table_type =  'COPY_ON_WRITE'
        
  
    hudi_table_name = hudi_table_name.lower() + '_w_sort_' + hudi_init_sort_option.lower() + '_w_write_op_blk_insert'

    # create the schema for the ny trips raw data file in CSV format
    yellow_tripdata_schema = StructType(
            [ StructField("vendorid",LongType(),True), 
              StructField("tpep_pickup_datetime",TimestampType(),True), 
              StructField("tpep_dropoff_datetime",TimestampType(),True), 
              StructField("passenger_count", DoubleType(), True), 
              StructField("trip_distance", DoubleType(), True), 
              StructField("ratecodeid", DoubleType(), True), 
              StructField("store_and_fwd_flag", StringType(), True), 
              StructField("pulocationid", LongType(), True), 
              StructField("dolocationid", LongType(), True), 
              StructField("payment_type", LongType(), True), 
              StructField("fare_amount", DoubleType(), True), 
              StructField("extra", DoubleType(), True), 
              StructField("mta_tax", DoubleType(), True), 
              StructField("tip_amount", DoubleType(), True), 
              StructField("tolls_amount", DoubleType(), True), 
              StructField("improvement_surcharge", DoubleType(), True), 
              StructField("total_amount", DoubleType(), True), 
              StructField("congestion_surcharge", DoubleType(), True), 
              StructField("pk_id", LongType(), True)]) # add the primary key column
    
    # read the NY Taxi trip data for the years of 2018,2019 and 2020
    # CHanging the path from local to public bucket
    
    if source_file_year.upper() == 'ALL':
        inpfl = "s3://aws-bigdata-blog/artifacts/get-started-with-hudi-bestpractices-blog/data/yellow_tripdata_{2018,2019,2020}*.csv"
    else:
        inpfl = "s3://aws-bigdata-blog/artifacts/get-started-with-hudi-bestpractices-blog/data/yellow_tripdata_{0}*.csv".format(source_file_year)
    
    print("Input File: ", inpfl)
    
    inputDf = spark.read.schema(yellow_tripdata_schema).option("header", "true") \
                .csv(inpfl) \
                .withColumn("pk_id",monotonically_increasing_id() + 1) \
                .withColumn("year",year(col("tpep_pickup_datetime")).cast("integer")) \
                .withColumn("month",month(col("tpep_pickup_datetime")).cast("integer")) \


    inputDf.printSchema()
    # inputDf.show(5)
    curr_session = boto3.session.Session()
    curr_region = curr_session.region_name
    # set the hudi configuration 
    hudi_part_write_config = {
        'className': 'org.apache.hudi',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.use_jdbc':'false',
        'hoodie.datasource.hive_sync.support_timestamp': 'true',
        'hoodie.datasource.write.operation': 'bulk_insert',
        'hoodie.datasource.write.table.type': hudi_table_type,
        'hoodie.table.name': hudi_table_name,
        'hoodie.datasource.hive_sync.table': hudi_table_name,
        'hoodie.datasource.write.recordkey.field': 'pk_id',
        'hoodie.datasource.write.precombine.field': 'tpep_pickup_datetime',
        'hoodie.datasource.write.partitionpath.field': 'year:SIMPLE,month:SIMPLE',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.MultiPartKeysValueExtractor',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.partition_fields': 'year,month',
        'hoodie.datasource.hive_sync.database': hudi_db_name,
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.CustomKeyGenerator',
        'hoodie.write.concurrency.mode' : 'optimistic_concurrency_control'
        ,'hoodie.cleaner.policy.failed.writes' : 'LAZY'
        ,'hoodie.write.lock.provider' : 'org.apache.hudi.aws.transaction.lock.DynamoDBBasedLockProvider'
        ,'hoodie.write.lock.dynamodb.table' : 'hudi-blog-lock-table'
        ,'hoodie.write.lock.dynamodb.partition_key' : 'tablename'
        ,'hoodie.write.lock.dynamodb.region' : '{0}'.format(curr_region)
        ,'hoodie.write.lock.dynamodb.endpoint_url' : 'dynamodb.{0}.amazonaws.com'.format(curr_region)
        ,'hoodie.write.lock.dynamodb.billing_mode' : 'PAY_PER_REQUEST'
        }
        

    table_path = 's3://{}/{}'.format(hudi_output_bucket, hudi_table_name)
    
    print('The path for Hudi table where data is stored', table_path)

    # only set this hudi parameter is a bulk insert sort option other than default is choosen
    if hudi_init_sort_option.upper() in ['PARTITION_SORT', 'NONE']:
        hudi_part_write_config['hoodie.bulkinsert.sort.mode'] = hudi_init_sort_option
        
    start_tm = datetime.now()
    print('The start time for the Bulk Insert :-' , start_tm)
    print('Hudi Conifguration Used for Partition Table; ', hudi_part_write_config)
    inputDf.write.format("hudi").options(**hudi_part_write_config).mode("overwrite").save(table_path)
    end_tm = datetime.now()
    print('The End time for the Bulk Insert :-' , end_tm)
    time_diff = end_tm - start_tm
    print('The time it took for Bulk Insert operation :-' , time_diff)
    rows_inserted =  inputDf.count()
    print('Rows Inserted : ', rows_inserted)
     

if __name__ == "__main__":
    perform_hudi_bulk_insert(args['HUDI_INIT_SORT_OPTION'],
                             args['OUTPUT_BUCKET'],
                             args['HUDI_TABLE_NAME'],
                             args['HUDI_DB_NAME'],
                             args['SOURCE_FILE_YEAR']
                        )
                
job.commit()