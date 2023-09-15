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


args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                    'OUTPUT_BUCKET',
                                    'HUDI_TABLE_NAME',
                                    'HUDI_DB_NAME'
                                    ])
print(args)
# print("The name of the bucket is :- ",  args['curated_bucket'])
ts_format = '%Y-%m-%d %H:%M:%S'
spark = SparkSession.builder.config('spark.serializer','org.apache.spark.serializer.KryoSerializer').config('spark.sql.hive.convertMetastoreParquet','false').config('spark.sql.legacy.pathOptionBehavior.enabled', 'true').getOrCreate()
sc = spark.sparkContext
glueContext = GlueContext(sc)
job = Job(glueContext)
logger = glueContext.get_logger()
job.init(args['JOB_NAME'], args)


def create_ins_records(hudi_db_name, hudi_table_name):
                                
    # get the max value of ss_ticket_number and year from the table.
    max_vals = spark.sql("select max(ss_ticket_number), max(year) from {}.{}".format(hudi_db_name, hudi_table_name))
    max_id = max_vals.collect()[0][0]
    print('Max ss_ticket_number : ', max_id)
    max_year =  max_vals.collect()[0][1]
    new_year = max_year + 1
    print('New Year : ', new_year)
    # create a new year and month by using data from year = 2002 and month = 01
    ins_tmp_df = spark.sql("select a.*, ss_ticket_number + {2} new_id, {3} new_year \
                                from {0}.{1} a where year = 2002 and month = 01 \
                             ".format(hudi_db_name, hudi_table_name, max_id, new_year))
                             
    drop_cols = ["ss_ticket_number", "year"]
    ins_df = ins_tmp_df.drop(*drop_cols) \
            .withColumnRenamed("new_id", "ss_ticket_number") \
            .withColumnRenamed("new_year", "year")
    
    print('Schema of Insert Recs DF')        
    ins_df.printSchema()
    return ins_df

    
def create_upd_records(hudi_db_name, hudi_table_name):
                                
    # update ss_list_price by 1 $ for all rows in year 2003 and month =1 
    upd_tmp_df = spark.sql("select a.*, ss_list_price + {2} new_list_price \
                                from {0}.{1} a where year = 2003 and month = 01 \
                             ".format(hudi_db_name, hudi_table_name, 1))
                             
    drop_cols = ["ss_list_price"]
    upd_df = upd_tmp_df.drop(*drop_cols).withColumnRenamed("new_list_price", "ss_list_price")
    print('Schema of Update Recs DF')
    upd_df.printSchema()
    return upd_df
    
    
def create_del_records(hudi_db_name, hudi_table_name):
                                
    
    # delete records for 1 month from year 2001 and month = 05
    del_df = spark.sql("select a.* from {0}.{1} a where year = 2001 and month = 05 \
                             ".format(hudi_db_name, hudi_table_name, 1))
    
    print('Schema of Delete Recs DF')                
    del_df.printSchema()
    return del_df
    
    
def perform_hudi_upsert(hudi_db_name, hudi_table_name, hudi_output_bucket):
    
    print('Performing Upsert / Delete For Table : {}.{}'.format(hudi_db_name, hudi_table_name))
    # create insert, update and delete records
    
    create_ins_records(hudi_db_name, hudi_table_name).createOrReplaceTempView("ins")
    ins_recs_df = spark.sql("select  \
                            ss_sold_date_sk,\
                            ss_sold_time_sk,\
                            ss_item_sk,\
                            ss_customer_sk,\
                            ss_cdemo_sk,\
                            ss_hdemo_sk,\
                            ss_store_sk,\
                            ss_addr_sk,\
                            ss_promo_sk,\
                            ss_ticket_number,\
                            ss_quantity,\
                            ss_wholesale_cost,\
                            ss_list_price,\
                            ss_sales_price,\
                            ss_ext_discount_amt,\
                            ss_ext_sales_price,\
                            ss_ext_wholesale_cost,\
                            ss_ext_list_price,\
                            ss_ext_tax,\
                            ss_coupon_amt,\
                            ss_net_paid,\
                            ss_net_paid_inc_tax,\
                            ss_net_profit,\
                            ts,\
                            year,\
                            month \
                    from ins "
                    )
    
    print('Insert record Count : ', ins_recs_df.count())
    
    create_upd_records(hudi_db_name, hudi_table_name).createOrReplaceTempView("upd")
    
    upd_recs_df = spark.sql("select  \
                            ss_sold_date_sk,\
                            ss_sold_time_sk,\
                            ss_item_sk,\
                            ss_customer_sk,\
                            ss_cdemo_sk,\
                            ss_hdemo_sk,\
                            ss_store_sk,\
                            ss_addr_sk,\
                            ss_promo_sk,\
                            ss_ticket_number,\
                            ss_quantity,\
                            ss_wholesale_cost,\
                            ss_list_price,\
                            ss_sales_price,\
                            ss_ext_discount_amt,\
                            ss_ext_sales_price,\
                            ss_ext_wholesale_cost,\
                            ss_ext_list_price,\
                            ss_ext_tax,\
                            ss_coupon_amt,\
                            ss_net_paid,\
                            ss_net_paid_inc_tax,\
                            ss_net_profit,\
                            ts,\
                            year,\
                            month \
                    from upd "
                    )
    
    print('Update record Count : ', upd_recs_df.count())
    
    del_recs_df = create_del_records(hudi_db_name, hudi_table_name)
    
    print('Delete record Count : ', del_recs_df.count())
    
    # set the hudi configuration 
    RECORD_KEY = "ss_item_sk, ss_ticket_number"
    PARTITION_FIELD = "year,month"
    PRECOMBINE_FIELD = "ts"
    
    hudi_write_config = {
        'className': 'org.apache.hudi',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.use_jdbc':'false',
        'hoodie.datasource.hive_sync.support_timestamp': 'true',
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
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.CustomKeyGenerator'
        ,'hoodie.parquet.max.file.size' : 125829120
        ,'hoodie.parquet.small.file.limit': 104857600
        ,'hoodie.cleaner.policy': 'KEEP_LATEST_COMMITS'
        ,'hoodie.cleaner.commits.retained' : 4
        ,'hoodie.upsert.shuffle.parallelism' : 2000
        }


    table_path = 's3://{}/{}'.format(hudi_output_bucket, hudi_table_name)
    
    print('The path for Hudi table where data is stored', table_path)
    

    ## Running the upsert operation
    
    hudi_write_config['hoodie.datasource.write.operation'] = 'upsert'
    
    print('Printing the Hudi Config For the upsert Operation' , hudi_write_config)
    
    start_tm = datetime.now()
    
    print('The start time for the upsert :-' , start_tm)
    upsert_recs_df = ins_recs_df.union(upd_recs_df)
    print("Schema of Upsert DF")
    upsert_recs_df.printSchema()
    upsert_recs_df.write.format("hudi").options(**hudi_write_config).mode("append").save(table_path)
    print('Upsert Record Count : ', upsert_recs_df.count())
    end_tm = datetime.now()
    
    print('The End time for the upsert :-' , end_tm)
    
    time_diff = end_tm - start_tm
    
    print('The Time Taken For Upsert Operation :-' , time_diff)
  
 
    #change the operation to delete to perform deletes.
    
    hudi_write_config['hoodie.datasource.write.operation'] = 'delete'
    hudi_write_config['hoodie.delete.shuffle.parallelism'] = 2000
    
    print('Printing the Hudi Config For the Delete Operation' , hudi_write_config)
    
    start_tm = datetime.now()
    
    print('The start time for the delete :-' , start_tm)
    
    del_recs_df.write.format("hudi").options(**hudi_write_config).mode("append").save(table_path)
    
    end_tm = datetime.now()
    
    print('The End time for the delete :-' , end_tm)
    
    time_diff = end_tm - start_tm
    
    print('The Taken For Delete Operation :-' , time_diff)
    
    
 
if __name__ == "__main__":
    
    
    perform_hudi_upsert(
                        args['HUDI_DB_NAME'],
                        args['HUDI_TABLE_NAME'],
                        args['OUTPUT_BUCKET']
)
                
job.commit()