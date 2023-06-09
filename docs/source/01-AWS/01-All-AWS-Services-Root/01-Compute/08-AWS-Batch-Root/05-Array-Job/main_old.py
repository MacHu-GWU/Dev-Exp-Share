# -*- coding: utf-8 -*-

import boto3
import fire


s3_client = boto3.client("s3")


def copy_s3_folder(s3uri_source: str, s3uri_target: str):
    """
    App 的核心逻辑
    """
    pass


class Command:
    """
    CLI app 的入口
    """

    def copy_s3_folder(self, s3uri_source: str, s3uri_target: str):
        """
        将同名的核心逻辑函数转换成 CLI App.

        用法:

        ``python main.py copy-s3-folder --s3uri-source s3://my-bucket/source --s3uri-target s3://my-bucket/target``
        """
        copy_s3_folder(s3uri_source, s3uri_target)


def run():
    """
    运行 CLI App
    """
    fire.Fire(Command)


if __name__ == "__main__":
    run()
