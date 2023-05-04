# -*- coding: utf-8 -*-


class S3:
    def list_buckets(self):
        print("run s3 list_buckets")

    def describe_bucket(self, name: str):
        print(f"run s3 describe_bucket --name={name}")
