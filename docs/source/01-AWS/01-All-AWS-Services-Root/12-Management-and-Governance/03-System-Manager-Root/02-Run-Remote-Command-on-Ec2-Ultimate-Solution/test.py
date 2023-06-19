# -*- coding: utf-8 -*-

import typing as T
import time
import json
import uuid
from pathlib_mate import Path
from s3pathlib import S3Path
from boto_session_manager import BotoSesManager
from send_command import (
    send_command,
    wait_until_command_succeeded,
)
from rich import print as rprint

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")


def run(
    bsm: BotoSesManager,
    instance_id: str,
    path_python: Path,
    code: str,
    s3_path: S3Path,
    args: T.List[str],
):
    """
    这是我们解决方案的主函数

    :param bsm: boto session manager 对象 (你可以不要这个对象, 直接用 ssm_client, s3_client 即可)
    :param instance_id: EC2 instance id
    :param path_python: 位于 EC2 上的 Python 解释器路径, 你可以选择用哪个 Python 解释器来运行这个命令
    :param code: 你要在 EC2 上执行的脚本的源代码的字符串
    :param s3_path: 你要将这个源代码上传到 S3 的哪里
    :param args: 这个 Python 脚本有没有额外的参数, 如果有, 请用列表的形式列出来, 就像你
        写 subprocess.run([...]) 一样.
    """
    s3path.write_text(code)

    # 生成一个随机的路径, 用于存放代码
    path_code = f"/tmp/{uuid.uuid4().hex}.py"
    # 用 aws cli 将代码下载到本地, 并且过滤掉日志
    command1 = f"/home/ubuntu/.pyenv/shims/aws s3 cp {s3_path.uri} {path_code} 2>&1 > /dev/null"
    # 组装最终命令
    args_ = [
        f"{path_python}",
        f"{path_code}",
    ]
    args_.extend(args)
    command2 = " ".join(args_)
    print(command1)
    print(command2)
    # 用 SSM 远程执行该命令
    command_id = send_command(
        ssm_client=bsm.ssm_client,
        instance_id=instance_id,
        commands=[
            command1,
            command2,
        ],
    )
    time.sleep(1) # 一定要等待 1 秒, 不然你立刻 get 是 get 不到的
    command_invocation = wait_until_command_succeeded(
        ssm_client=bsm.ssm_client,
        command_id=command_id,
        instance_id=instance_id,
    )
    rprint(command_invocation)
    # 解析 return code 和 standard output, parse 我们脚本输出的 JSON
    print(command_invocation.ResponseCode)
    lines = command_invocation.StandardOutputContent.splitlines()
    output_data = json.loads(lines[-1])
    rprint(output_data)


instance_id = "i-00f591fc972902fc5"
path_python = Path("/home/ubuntu/.pyenv/shims/python")
code = Path("script.py").read_text()
s3path = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-data/projects/dev-exp-share/script.py"
)
args = []
run(
    bsm=bsm,
    instance_id=instance_id,
    path_python=path_python,
    code=code,
    s3_path=s3path,
    args=[],
)
