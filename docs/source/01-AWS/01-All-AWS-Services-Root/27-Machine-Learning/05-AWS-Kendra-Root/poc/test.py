# -*- coding: utf-8 -*-

from rich import print as rprint
from pathlib_mate import Path
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager, AwsServiceEnum

index_id = "a413e790-1467-45c5-8cac-1deca6eebca3"

bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_2")
context.attach_boto_session(bsm.boto_ses)

s3_client = bsm.get_client(AwsServiceEnum.S3)
kdr_client = bsm.get_client(AwsServiceEnum.kendra)

dir_here = Path.dir_here(__file__)
dir_data = dir_here.append_parts("data")
dir_meta = dir_here.append_parts("meta")

s3path_prefix_data = S3Path.from_s3_uri(
    "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-05-31-kendra/data").to_dir()
s3path_prefix_meta = S3Path.from_s3_uri(
    "s3://aws-data-lab-sanhe-for-everything-us-east-2/poc/2022-05-31-kendra/meta").to_dir()


def s1_create_data_source():
    res = kdr_client.create_data_source(
        IndexId=index_id,
        Type="S3",
        Name="word-doc",
        Configuration=dict(
            S3Configuration=dict(
                BucketName=s3path_prefix_data.bucket,
                InclusionPrefixes=[
                    s3path_prefix_data.key
                ],
                DocumentsMetadataConfiguration=dict(
                    S3Prefix=s3path_prefix_meta.key
                ),
            ),
        ),
        RoleArn="arn:aws:iam::669508176277:role/sanhe-for-everything-admin",
    )
    rprint(res)


def s2_upload_doc():
    s3path_prefix_data.delete_if_exists()
    s3path_prefix_data.upload_dir(dir_data.abspath)


def query_data():
    res = kdr_client.query(
        IndexId=index_id,
        QueryText="alice caddle",
    )
    rprint(res)


if __name__ == "__main__":
    # upload_data()
    # s1_create_data_source()
    # s2_upload_doc()
    query_data()
    pass
