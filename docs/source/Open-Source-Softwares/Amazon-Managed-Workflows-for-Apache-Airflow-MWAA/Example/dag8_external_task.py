# -*- coding: utf-8 -*-

"""
用来模拟外部任务. 在 invoke dag 之前请运行这个脚本, 然后再在 5 秒内 invoke dag.
"""

import time
import random
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)

s3path = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-data/"
    f"projects/mwaa-poc/dag8/task0.status.txt",
)


def run():
    """
    每 2 秒循环一次, 共循环 10 次, 每次循环有 5% 的概率失败. 如果 10 次循环都成功, 则任务成功.
    经过简单的概率计算, 10 次循环都成功的概率为 60%.

    在开始的时候就往 S3 中写入 doing, 任务成功后写入 succeeded, 任务失败后写入 failed.
    """
    s3path.write_text("doing")
    for i in range(1, 10 + 1):
        print(f"{i} / 10 th iteration")
        time.sleep(2)
        if random.randint(1, 100) <= 5:
            s3path.write_text("failed")
            print("failed")
            return
    print("succeeded")
    s3path.write_text("succeeded")


s3path.delete()
run()
