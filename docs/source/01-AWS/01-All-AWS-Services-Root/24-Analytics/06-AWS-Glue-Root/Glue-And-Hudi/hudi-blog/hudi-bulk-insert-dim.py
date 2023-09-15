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
                                    'HUDI_DB_NAME'
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
                             hudi_db_name
                            ):
    
   
    hudi_table_type =  'COPY_ON_WRITE'
        
 
    # create the schema for the ny trips raw data file in CSV format
    
    store_dim_schema = StructType(
            [StructField("s_store_sk",IntegerType(),True),
            StructField("s_store_id",StringType(),True),
            StructField("s_rec_start_date",DateType(),True),
            StructField("s_rec_end_date",DateType(),True),
            StructField("s_closed_date_sk",IntegerType(),True),
            StructField("s_store_name",StringType(),True),
            StructField("s_number_employees",IntegerType(),True),
            StructField("s_floor_space",IntegerType(),True),
            StructField("s_hours",StringType(),True),
            StructField("s_manager",StringType(),True),
            StructField("s_market_id",IntegerType(),True),
            StructField("s_geography_class",StringType(),True),
            StructField("s_market_desc",StringType(),True),
            StructField("s_market_manager",StringType(),True),
            StructField("s_division_id",IntegerType(),True),
            StructField("s_division_name",StringType(),True),
            StructField("s_company_id",IntegerType(),True),
            StructField("s_company_name",StringType(),True),
            StructField("s_street_number",StringType(),True),
            StructField("s_street_name",StringType(),True),
            StructField("s_street_type",StringType(),True),
            StructField("s_suite_number",StringType(),True),
            StructField("s_city",StringType(),True),
            StructField("s_county",StringType(),True),
            StructField("s_state",StringType(),True),
            StructField("s_zip",StringType(),True),
            StructField("s_country",StringType(),True),
            StructField("s_gmt_offset",DoubleType(),True),
            StructField("s_tax_precentage",DoubleType(),True)
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
    
    item_schema = StructType(
            [ StructField("i_item_sk",IntegerType(),True),
              StructField("i_item_id",StringType(),True),
              StructField("i_rec_start_date",DateType(),True),
              StructField("i_rec_end_date",DateType(),True),
              StructField("i_item_desc",StringType(),True),
              StructField("i_current_price",DoubleType(),True),
              StructField("i_wholesale_cost",DoubleType(),True),
              StructField("i_brand_id",IntegerType(),True),
              StructField("i_brand",StringType(),True),
              StructField("i_class_id",IntegerType(),True),
              StructField("i_class",StringType(),True),
              StructField("i_category_id",IntegerType(),True),
              StructField("i_category",StringType(),True),
              StructField("i_manufact_id",IntegerType(),True),
              StructField("i_manufact",StringType(),True),
              StructField("i_size",StringType(),True),
              StructField("i_formulation",StringType(),True),
              StructField("i_color",StringType(),True),
              StructField("i_units",StringType(),True),
              StructField("i_container",StringType(),True),
              StructField("i_manager_id",IntegerType(),True),
              StructField("i_product_name",StringType(),True),
              ]
              )

    df_date_dim = spark.read.schema(date_dim_schema).\
                format("csv").options(header=True,delimiter="|").\
                load("s3://redshift-downloads/TPC-DS/2.13/1TB/date_dim/"). \
                withColumn("ts", current_timestamp())
    df_date_dim.printSchema()
    
    df_item_dim = spark.read.schema(item_schema).\
                format("csv").options(header=True,delimiter="|").\
                load("s3://redshift-downloads/TPC-DS/2.13/1TB/item/"). \
                withColumn("ts", current_timestamp())
    df_item_dim.printSchema()
    
    df_store_dim = spark.read.schema(store_dim_schema).\
                    format("csv").options(header=True,delimiter="|").\
                    load("s3://redshift-downloads/TPC-DS/2.13/1TB/store/"). \
                    withColumn("ts", current_timestamp())
    df_store_dim.printSchema()
    
    curr_session = boto3.session.Session()
    curr_region = curr_session.region_name
    
    # set the hudi configuration 
    hudi_write_config = {
        'className': 'org.apache.hudi',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.use_jdbc':'false',
        'hoodie.datasource.hive_sync.support_timestamp': 'true',
        'hoodie.datasource.write.operation': 'bulk_insert',
        'hoodie.datasource.write.table.type': hudi_table_type,
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.MultiPartKeysValueExtractor',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.datasource.hive_sync.database': hudi_db_name,
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.CustomKeyGenerator'
        }
    
    PRECOMBINE_FIELD ="ts"  # common across all dim tables
    hudi_write_config['hoodie.datasource.write.precombine.field'] = PRECOMBINE_FIELD

    # create store dim table
    STORE_DIM_RECORD_KEY = "s_store_sk"
    STORE_DIM_PARTITION_FIELD = ""
    PRECOMBINE_FIELD = "ts"
    
    table_name = 'store' 
    print('Store Dim Table : ', table_name)
    table_path = 's3://{}/{}'.format(hudi_output_bucket, table_name)
    print('The path for Hudi table where data is stored', table_path)
    hudi_write_config['hoodie.datasource.write.recordkey.field'] = STORE_DIM_RECORD_KEY
    hudi_write_config['hoodie.table.name'] = table_name
    hudi_write_config['hoodie.datasource.hive_sync.table'] = table_name
    hudi_write_config['hoodie.datasource.write.partitionpath.field'] = ""
    
    start_ts = datetime.now()
    print('The start time for Store Dim :-' , start_ts)
    print('Hudi Conifguration Used ; ', hudi_write_config)
    df_store_dim.write.format("hudi").options(**hudi_write_config).mode("overwrite").save(table_path)
    end_ts = datetime.now()
    print('The End time for Store Dim :-' , end_ts)
    time_diff = end_ts - start_ts
    print('The time it took for Bulk Insert operation :-' , time_diff)
    rows_inserted =  df_item_dim.count()
    print(' Store Dim Rows Inserted : ', rows_inserted)
    
        
    
    # create date time table
    
    DATE_DIM_RECORD_KEY = "d_date_sk"
    DATE_DIM_PARTITION_FIELD = ""
    PRECOMBINE_FIELD = "ts"

    table_name = 'date_dim'
    print('Date Dim Table : ', table_name)
    table_path = 's3://{}/{}'.format(hudi_output_bucket, table_name)
    print('The path for Hudi table where data is stored', table_path)
    hudi_write_config['hoodie.datasource.write.recordkey.field'] = DATE_DIM_RECORD_KEY
    hudi_write_config['hoodie.table.name'] = table_name
    hudi_write_config['hoodie.datasource.hive_sync.table'] = table_name
    hudi_write_config['hoodie.datasource.write.partitionpath.field'] = ""
    
    start_ts = datetime.now()
    print('The start time for Date Dim :-' , start_ts)
    print('Hudi Conifguration Used ; ', hudi_write_config)
    df_date_dim.write.format("hudi").options(**hudi_write_config).mode("overwrite").save(table_path)
    end_ts = datetime.now()
    print('The End time for Date Dim :-' , end_ts)
    time_diff = end_ts - start_ts
    print('The time it took for Bulk Insert operation :-' , time_diff)
    rows_inserted =  df_date_dim.count()
    print(' Date Dim Rows Inserted : ', rows_inserted)
    
    
    # create Item dim table
    
    ITEM_DIM_RECORD_KEY = "i_item_sk"
    ITEM_DIM_PARTITION_FIELD = ""
    PRECOMBINE_FIELD = "ts"
    
    table_name = 'item'
    print('Item Dim Table : ', table_name)
    table_path = 's3://{}/{}'.format(hudi_output_bucket, table_name)
    print('The path for Hudi table where data is stored', table_path)
    hudi_write_config['hoodie.datasource.write.recordkey.field'] = ITEM_DIM_RECORD_KEY
    hudi_write_config['hoodie.table.name'] = table_name
    hudi_write_config['hoodie.datasource.hive_sync.table'] = table_name
    hudi_write_config['hoodie.datasource.write.partitionpath.field'] = ""
    
    start_ts = datetime.now()
    print('The start time for Item Dim :-' , start_ts)
    print('Hudi Conifguration Used ; ', hudi_write_config)
    df_item_dim.write.format("hudi").options(**hudi_write_config).mode("overwrite").save(table_path)
    end_ts = datetime.now()
    print('The End time for Item Dim :-' , end_ts)
    time_diff = end_ts - start_ts
    print('The time it took for Bulk Insert operation :-' , time_diff)
    rows_inserted =  df_item_dim.count()
    print(' Item Dim Rows Inserted : ', rows_inserted)
    

if __name__ == "__main__":
    perform_hudi_bulk_insert(args['HUDI_INIT_SORT_OPTION'],
                             args['OUTPUT_BUCKET'],
                             args['HUDI_DB_NAME']
                        )
                
job.commit()