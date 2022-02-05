# -*- coding: utf-8 -*-

from s3pathlib import S3Path
from pyathena import connect
import pandas as pd

# define the s3 foldter to store result
s3path_athena_result = S3Path(
    "aws-data-lab-sanhe-for-everything-us-east-2",
    "athena/results/"
)

# define connection, use AWS CLI named profile for authentication
conn = connect(
    s3_staging_dir=s3path_athena_result.uri,
    profile_name="aws_data_lab_sanhe",
    region_name="us-east-2",
)

# define the SQL statement, use ${database}.${table} as t to specify the table
sql = """
SELECT 
    t.category,
    AVG(t.value) as average_value  
FROM poc.events t
GROUP BY t.category
ORDER BY t.category
"""

# execute the SQL query, load result to pandas DataFrame
df = pd.read_sql_query(sql, conn)
print(df)
