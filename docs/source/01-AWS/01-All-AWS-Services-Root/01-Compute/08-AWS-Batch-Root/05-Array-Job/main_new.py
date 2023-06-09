# -*- coding: utf-8 -*-

import typing as T
import os
import json

import boto3
import fire


s3_client = boto3.client("s3")


def copy_s3_folder(s3uri_source: str, s3uri_target: str):
    """
    App 的核心逻辑
    """
    pass


def parse_array_index() -> int:
    """
    从环境变量中获得 Index 的数值
    """
    return int(os.environ["AWS_BATCH_JOB_ARRAY_INDEX"].split(":", 1)[1])


class Command:
    """
    CLI app 的入口
    """

    def copy_s3_folder(
        self,
        s3uri_source: T.Optional[str] = None,
        s3uri_target: T.Optional[str] = None,
        s3uri_kwargs: T.Optional[str] = None,
    ):
        """
        将同名的核心逻辑函数转换成 CLI App.

        在已有的参数基础上, 增加了一个参数 s3uri_kwargs, 用于从 S3 中读取参数.

        1. 如果 s3uri_kwargs 为 None, 则直接使用 s3uri_source 和 s3uri_target 作为参数.
            就像直接使用 :func:`copy_s3_folder` 一样.
        2. 如果 s3uri_kwargs 不为 None, 则从 S3 中的 JSON 文件中读取参数, 并使用这些参数作为参数.

        用法:

        ``python main.py copy-s3-folder --s3uri-source s3://my-bucket/source --s3uri-target s3://my-bucket/target``
        或 ``python main.py copy-s3-folder --s3uri-kwargs s3://my-bucket/kwargs``
        """
        if s3uri_kwargs is not None:
            _, _, bucket, prefix = s3uri_kwargs.split("/", 3)
            array_index = parse_array_index()
            response = s3_client.get_object(
                Bucket=bucket, Key=f"{prefix}/{array_index}.json"
            )
            kwargs = json.loads(response["Body"].read().decode("utf-8"))
            copy_s3_folder(
                s3uri_source=kwargs["s3uri_source"], s3uri_target=kwargs["s3uri_target"]
            )
        else:
            copy_s3_folder(s3uri_source=s3uri_source, s3uri_target=s3uri_target)


def run():
    """
    运行 CLI App
    """
    fire.Fire(Command)


if __name__ == "__main__":
    run()
