CREATE EXTERNAL TABLE IF NOT EXISTS fruit_sale (
    item STRING,
    price FLOAT,
    time STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ","
)
STORED AS TEXTFILE
LOCATION 's3://skymap-sandbox-learn-emr/data';

INSERT OVERWRITE DIRECTORY 's3://skymap-sandbox-learn-emr/result/' SELECT COUNT(*) count FROM fruit_sale;