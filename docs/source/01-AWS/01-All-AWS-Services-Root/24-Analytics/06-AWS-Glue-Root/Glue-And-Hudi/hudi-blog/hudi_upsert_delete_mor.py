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
                                    'HUDI_DB_NAME',
                                    'COMPACTION'
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


def perform_hudi_upsert(
                             hudi_output_bucket,
                             hudi_table_name,
                             hudi_db_name,
                             compaction
                            ):
    src_table_name = hudi_table_name + '_ro'
    # get the max vendor_id to increment the value to create update records.
    max_vendor_id = spark.sql("""select max(pk_id) max_pk_id from `{}`.{} """. format(hudi_db_name, src_table_name)).first()[0]
    
    sql = """select * from `{}`.{} where year IN (2018) and month IN (4) and passenger_count = 1  """.format(hudi_db_name, src_table_name)

    print(sql)
    spark.sql(sql).createOrReplaceTempView("u_view")
    
    upd_recs_df = spark.sql("select \
                                {} + 1 vendorid, \
                                tpep_pickup_datetime, \
                                tpep_dropoff_datetime, \
                                passenger_count, \
                                trip_distance, \
                                ratecodeid , \
                                store_and_fwd_flag , \
                                pulocationid , \
                                dolocationid , \
                                payment_type , \
                                fare_amount , \
                                extra , \
                                mta_tax , \
                                tip_amount , \
                                tolls_amount , \
                                improvement_surcharge , \
                                total_amount , \
                                congestion_surcharge ,\
                                pk_id, \
                                year ,\
                                month\
                        from u_view a".format(max_vendor_id))
                        
    print('update rec count for the year IN (2018) and month IN (4) and passenger_count = 1 : ', upd_recs_df.count())
    
    
    # Generate insert data
    # get the max pk_id to increment and create insert records

    max_pk_id = spark.sql("""select max(pk_id) max_pk_id from `{}`.{}""". format(hudi_db_name,src_table_name)).first()[0]
    
    print('Value for max_pk_id', max_pk_id)
    
    sql = """select * from `{}`.{} where year IN (2018,2019,2020) and month IN (5,6,7)  and passenger_count = 1 """.format(hudi_db_name, src_table_name)
       
    print(sql)
    spark.sql(sql).createOrReplaceTempView("i_view")
    
    
    ins_recs_df = spark.sql("select \
                                vendorid, \
                                tpep_pickup_datetime, \
                                tpep_dropoff_datetime, \
                                passenger_count, \
                                trip_distance, \
                                ratecodeid , \
                                store_and_fwd_flag , \
                                pulocationid , \
                                dolocationid , \
                                payment_type , \
                                fare_amount , \
                                extra , \
                                mta_tax , \
                                tip_amount , \
                                tolls_amount , \
                                improvement_surcharge , \
                                total_amount , \
                                congestion_surcharge ,\
                                row_number() over (partition by year,month order by pk_id) + {0} pk_id,\
                                year ,\
                                month\
                        from i_view a".format(max_pk_id))
                        
    print('Insert rec count  for year IN (2018,2019,2020) and month IN (5,6,7) and passenger_count = 1: ', ins_recs_df.count())
       
    if upd_recs_df:                    
        update_cnt = upd_recs_df.count()
    if ins_recs_df:
        insert_cnt = ins_recs_df.count()
    
    upsert_df = upd_recs_df.union(ins_recs_df)
    
    
    # create delete records 
    sql = """select * from `{}`.{} where year IN (2018,2019,2020) and month IN  (9,10,11) and passenger_count = 1 """.format(hudi_db_name, src_table_name)
                            
    print(sql)
    spark.sql(sql).createOrReplaceTempView("d_view")
    
    delete_df = spark.sql("select \
                                vendorid, \
                                tpep_pickup_datetime, \
                                tpep_dropoff_datetime, \
                                passenger_count, \
                                trip_distance, \
                                ratecodeid , \
                                store_and_fwd_flag , \
                                pulocationid , \
                                dolocationid , \
                                payment_type , \
                                fare_amount , \
                                extra , \
                                mta_tax , \
                                tip_amount , \
                                tolls_amount , \
                                improvement_surcharge , \
                                total_amount , \
                                congestion_surcharge ,\
                                pk_id, \
                                year ,\
                                month\
                        from d_view a")
    
    delete_cnt = delete_df.count()                    
    print('delete rec count for year IN (2018,2019,2020) and month IN (9,10,11) and passenger_count = 1:  ', delete_cnt)
    
    # set the hudi configuration 
    hudi_write_config = {
        'className': 'org.apache.hudi',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.use_jdbc':'false',
        'hoodie.datasource.hive_sync.support_timestamp': 'true',
        'hoodie.datasource.write.operation': 'upsert',    ## Write Operation is upsert
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
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.CustomKeyGenerator'
        ,'hoodie.parquet.max.file.size' : 125829120
        ,'hoodie.parquet.small.file.limit': 104857600
        ,'hoodie.cleaner.policy': 'KEEP_LATEST_COMMITS'
        ,'hoodie.cleaner.commits.retained' : 4
        }
        
    # Set this when Compaction is SET to Y.
    if compaction.upper() == 'Y':
        hudi_write_config['hoodie.compact.inline.max.delta.commits'] = 1
    
    print('Printing the Hudi Config For the Upsert Operation' , hudi_write_config)
    
    table_path = 's3://{}/{}'.format(hudi_output_bucket, hudi_table_name)
    
    print('The path for Hudi table where data is stored', table_path)
    
    start_tm = datetime.now()
    
    print('The start time for the Upsert :-' , start_tm)
    
    hudi_write_config['hoodie.datasource.write.operation'] = 'upsert'
    
    print('Printing the Hudi Config For the Upsert Operation' , hudi_write_config)
    
    # upsert operation on the hudi table.
    upsert_df.write.format("hudi").options(**hudi_write_config).mode("append").save(table_path)
 
    end_tm = datetime.now()
    
    print('The End time for the Upsert :-' , end_tm)
    
    time_diff = end_tm - start_tm
    
    #td_mins = int(round(time_diff.total_seconds() / 60))
    
    print('The time it took for Upsert operation :-' , time_diff)
    

    ## Running the upsert operation
    
    #hudi_write_config['hoodie.datasource.write.operation'] = 'upsert'
    
    #print('Printing the Hudi Config For the upsert Operation' , hudi_write_config)
    
 
    #change the operation to delete to perform deletes.
    
    hudi_write_config['hoodie.datasource.write.operation'] = 'delete'
    
    print('Printing the Hudi Config For the Delete Operation' , hudi_write_config)
    
    start_tm = datetime.now()
    
    print('The start time for the delete :-' , start_tm)
    
    delete_df.write.format("hudi").options(**hudi_write_config).mode("append").save(table_path)
    
    end_tm = datetime.now()
    
    print('The End time for the delete :-' , end_tm)
    
    time_diff = end_tm - start_tm
    
    print('The time it took for delete operation :-' , time_diff)

   
    
if __name__ == "__main__":
    perform_hudi_upsert(
                             args['OUTPUT_BUCKET'],
                             args['HUDI_TABLE_NAME'],
                             args['HUDI_DB_NAME'],
                             args['COMPACTION']
                )
                
job.commit()