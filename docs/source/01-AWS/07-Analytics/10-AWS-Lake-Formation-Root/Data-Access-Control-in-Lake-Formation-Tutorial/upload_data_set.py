# -*- coding: utf-8 -*-

"""
Upload everything in a local directory to a s3 folder.

Exmaple:

upload /path/to/source_folder/readme.txt -> s3://{bucket}/path/to/distination_folder/readme.txt
"""

from __future__ import print_function
import os
import boto3


def upload(s3_client, src_dir_path, bucket, dst_dir_key):
    if dst_dir_key.endswith("/"):
        dst_dir_key = dst_dir_key[:-1]
    for current_dir, _, filename_list in os.walk(src_dir_path):
        for filename in filename_list:
            fullpath = os.path.join(current_dir, filename)
            relpath = os.path.relpath(fullpath, src_dir_path)
            relpath = relpath.replace("\\", "/")
            s3_key = "{}/{}".format(dst_dir_key, relpath)
            print("upload {} -> s3://{}/{}".format(fullpath, bucket, s3_key))
            s3_client.upload_file(fullpath, bucket, s3_key)


if __name__ == "__main__":
    s3_client = boto3.session.Session().client("s3")
    here = os.path.dirname(__file__)
    upload(
        s3_client=s3_client,
        src_dir_path=os.path.join(here, "eshop"),
        bucket="aws-data-lab-sanhe-for-everything",
        dst_dir_key="poc/2021-10-04-lakeformation-access-control-poc-dataset/eshop",
    )
