# -*- coding: utf-8 -*-

from s3pathlib import S3Path, context
from pathlib_mate import Path
from boto_session_manager import BotoSesManager
from rich import print as rprint

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
project_name = "hudi-poc"
role = f"arn:aws:iam::{bsm.aws_account_id}:role/all-services-admin-role"
s3path = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-artifacts/projects/{project_name}/scripts/{project_name}.py"
)
path = Path.dir_here(__file__).joinpath(f"{project_name}.py")
context.attach_boto_session(bsm.boto_ses)

s3path.upload_file(path, overwrite=True)


def create_job():
    """
    Reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_job.html
    """
    bsm.glue_client.create_job(
        Name=project_name,
        LogUri="string",
        Role=role,
        ExecutionProperty={"MaxConcurrentRuns": 1},
        Command={
            "Name": "glueetl",
            "ScriptLocation": s3path.uri,
        },
        DefaultArguments={
            "--datalake-formats": "hudi",
            "--conf": "spark.serializer=org.apache.spark.serializer.KryoSerializer --conf spark.sql.hive.convertMetastoreParquet=false",
            "--enable-metrics": "true",
            "--spark-event-logs-path": "true",
            "--enable-spark-ui": f"s3://aws-glue-assets-{bsm.aws_account_id}-{bsm.aws_region}/sparkHistoryLogs/",
            "--enable-job-insights": "false",
            "--enable-glue-datacatalog": "true",
            "--enable-continuous-cloudwatch-log": "true",
            "--job-bookmark-option": "job-bookmark-disable",
            "--job-language": "python",
            "--TempDir": f"s3://aws-glue-assets-{bsm.aws_account_id}-{bsm.aws_region}/temporary/",
        },
        MaxRetries=1,
        GlueVersion="4.0",
        WorkerType="G.1X",
        NumberOfWorkers=2,
        Timeout=60,
    )


create_job()

# response = bsm.glue_client.get_job(JobName="hudi-poc-1")
# rprint(response)
