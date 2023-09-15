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
from functools import reduce

args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                    'OUTPUT_BUCKET',
                                    'HUDI_INIT_SORT_OPTION',
                                    'HUDI_TABLE_NAME',
                                    'HUDI_DB_NAME',
                                    'CATEGORY_ID'
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
                             category_id
                            ):
    
   
    hudi_table_type =  'COPY_ON_WRITE'
        
  
    hudi_table_name = hudi_table_name.lower() + '_' + hudi_init_sort_option.lower()

    # create the schema for the ny trips raw data file in CSV format
    
    store_sales_schema = StructType(
            [ StructField("ss_sold_date_sk",IntegerType(),True), 
              StructField("ss_sold_time_sk",IntegerType(),True), 
              StructField("ss_item_sk",IntegerType(),True), 
              StructField("ss_customer_sk", IntegerType(), True), 
              StructField("ss_cdemo_sk", IntegerType(), True), 
              StructField("ss_hdemo_sk", IntegerType(), True), 
              StructField("ss_store_sk", IntegerType(), True), 
              StructField("ss_addr_sk", IntegerType(), True), 
              StructField("ss_promo_sk", IntegerType(), True), 
              StructField("ss_ticket_number", LongType(), True), 
              StructField("ss_quantity", IntegerType(), True), 
              StructField("ss_wholesale_cost", DoubleType(), True), 
              StructField("ss_list_price", DoubleType(), True), 
              StructField("ss_sales_price", DoubleType(), True), 
              StructField("ss_ext_discount_amt", DoubleType(), True), 
              StructField("ss_ext_sales_price", DoubleType(), True), 
              StructField("ss_ext_wholesale_cost", DoubleType(), True), 
              StructField("ss_ext_list_price", DoubleType(), True), 
              StructField("ss_ext_tax", DoubleType(), True), 
              StructField("ss_coupon_amt", DoubleType(), True), 
              StructField("ss_net_paid", DoubleType(), True), 
              StructField("ss_net_paid_inc_tax", DoubleType(), True), 
              StructField("ss_net_profit", DoubleType(), True)
               ])
    
    date_dim_schema = StructType(
            [ StructField("d_date_sk",IntegerType(),True),
              StructField("d_date_id",StringType(),True),
              StructField("d_date",DateType(),True),
              StructField("d_month_seq",IntegerType(),True),
              StructField("d_week_seq",IntegerType(),True),
              StructField("d_quarter_seq",IntegerType(),True),
              StructField("d_year",IntegerType(),True),
              StructField("d_dow",IntegerType(),True),
              StructField("d_moy",IntegerType(),True),
              StructField("d_dom",IntegerType(),True),
              StructField("d_qoy",IntegerType(),True),
              StructField("d_fy_year",IntegerType(),True),
              StructField("d_fy_quarter_seq",IntegerType(),True),
              StructField("d_fy_week_seq",IntegerType(),True),
              StructField("d_day_name", StringType(), True),
              StructField("d_quarter_name", StringType(), True),
              StructField("d_holiday", StringType(), True),
              StructField("d_weekend", StringType(), True),
              StructField("d_following_holiday", StringType(), True),
              StructField("d_first_dom",IntegerType(),True),
              StructField("d_last_dom",IntegerType(),True),
              StructField("d_same_day_ly",IntegerType(),True),
              StructField("d_same_day_lq",IntegerType(),True),
              StructField("d_current_day", StringType(), True),
              StructField("d_current_week", StringType(), True),
              StructField("d_current_month", StringType(), True),
              StructField("d_current_quarter", StringType(), True),
              StructField("d_current_year", StringType(), True)
              ]
              )

    df_date_dim = spark.read.schema(date_dim_schema).\
                format("csv").options(header=True,delimiter="|").\
                load("s3://redshift-downloads/TPC-DS/2.13/1TB/date_dim/")
    df_date_dim.createOrReplaceTempView("date_dim")
    
    store_sales_Df = spark.read.schema(store_sales_schema).\
                    format("csv").options(header=True,delimiter="|").\
                    load("s3://redshift-downloads/TPC-DS/2.13/1TB/store_sales/"). \
                    withColumn("ts", current_timestamp())
                    
    store_sales_Df.printSchema()
    store_sales_Df.createOrReplaceTempView("store_sales")

    # join the date dim with store sales to get the year and month values to create partitions for store sales

    if category_id.upper() == 'ALL':
        store_facts = spark.sql("select a.*, b.d_year year, b.d_moy month \
                                from store_sales a inner join date_dim b on a.ss_sold_date_sk = b.d_date_sk")
    else:
        store_facts = spark.sql("select a.*, c.i_category_id, b.d_year year \
                                from store_sales a \
                                        inner join date_dim b on a.ss_sold_date_sk = b.d_date_sk \
                                        inner join item c on a.ss_item_sk = c.i_item_sk \
                                  where c.i_category_id = {}".format(int(category_id)))
    store_facts.printSchema() 
    store_facts.createOrReplaceTempView("v_sales")
    RECORD_KEY = "ss_item_sk, ss_ticket_number"
    PARTITION_FIELD = "year,month"
    PRECOMBINE_FIELD = "ts"
    
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
        'hoodie.datasource.write.recordkey.field': RECORD_KEY,
        'hoodie.datasource.write.precombine.field': PRECOMBINE_FIELD,
        'hoodie.datasource.write.partitionpath.field': 'year:SIMPLE,month:SIMPLE',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.MultiPartKeysValueExtractor',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.partition_fields': PARTITION_FIELD,
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
        ,'hoodie.bulkinsert.shuffle.parallelism': 2000
        }
        

    table_path = 's3://{}/{}'.format(hudi_output_bucket, hudi_table_name)
    
    print('The path for Hudi table where data is stored', table_path)

    # only set this hudi parameter is a bulk insert sort option other than default is choosen
    if hudi_init_sort_option.upper() in ['PARTITION_SORT', 'NONE']:
        hudi_part_write_config['hoodie.bulkinsert.sort.mode'] = hudi_init_sort_option
        
    start_tm = datetime.now()
    print('The start time for the Bulk Insert :-' , start_tm)
    
    if category_id.upper() == 'ALL':
        store_facts.write.format("hudi").options(**hudi_part_write_config).mode("overwrite").save(table_path)
    else:
        # This is for parallel run scenario where the parallel jobs are run each category_id
        hudi_part_write_config['hoodie.datasource.write.partitionpath.field'] = 'i_category_id:SIMPLE, year:SIMPLE'
        hudi_part_write_config['hoodie.datasource.hive_sync.partition_fields'] = 'i_category_id, year'
        print('Hudi Conifguration Used for Partition Table: ', hudi_part_write_config)
        store_facts.write.format("hudi").options(**hudi_part_write_config).mode("append").save(table_path)
        
    end_tm = datetime.now()
    print('The End time for the Bulk Insert :-' , end_tm)
    time_diff = end_tm - start_tm
    print('The time it took for Bulk Insert operation :-' , time_diff)
    rows_inserted =  store_facts.count()
    print('Rows Inserted : ', rows_inserted)
     

if __name__ == "__main__":
    
    try:
        perform_hudi_bulk_insert(args['HUDI_INIT_SORT_OPTION'],
                                 args['OUTPUT_BUCKET'],
                                 args['HUDI_TABLE_NAME'],
                                 args['HUDI_DB_NAME'],
                                 args['CATEGORY_ID']
                            )
    except Exception as e:
        print(e)
        raise
                
job.commit()