# -*- coding: utf-8 -*-

from io import StringIO
from pathlib import Path
from paramiko import AutoAddPolicy, SFTPClient, SSHClient
from paramiko import RSAKey


def sftp_connect(
    sftp_hostname: str,
    sftp_port: int,
    sftp_username: str,
    ssh_private_key: str,
    ssh_password: str,
) -> SFTPClient:
    # 读取 Private Key
    private_key = RSAKey.from_private_key(
        StringIO(ssh_private_key),
        password=ssh_password,
    )
    ssh_client = SSHClient()
    # 自动将 host 添加为 known host
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(
        hostname=sftp_hostname,
        username=sftp_username,
        port=sftp_port,
        pkey=private_key,
        allow_agent=False,
        look_for_keys=False,
    )
    sftp_client = ssh_client.open_sftp()
    return sftp_client


if __name__ == "__main__":
    host = "s-a1b2c3.server.transfer.${aws_region}.amazonaws.com"
    port = 22
    username = "username" # 你 SFTP 的用户名
    path_pk = Path.home().joinpath(".ssh", "id_rsa") # 你的私钥文件
    password = "password" # 你的 SSH key 的密码 (一般创建 SSH key pair 的时候设置的密码)
    sftp = sftp_connect(
        sftp_hostname=host,
        sftp_port=port,
        sftp_username=username,
        ssh_private_key=path_pk.read_text(),
        ssh_password=password,
    )

    # 你创建 SFTP server 的时候设置的后台 bucket 和 prefix
    bucket = "your_s3_bucket"
    prefix = "your_s3_prefix"
    if prefix.endswith("/"):
        prefix = prefix[:-1]
    if prefix:
        sftp_home_path = f"/{bucket}/{prefix}"
    else:
        sftp_home_path = f"/{bucket}"

    # write test.txt
    sftp.open(f"{sftp_home_path}/{username}/test.txt", "w").write("hello alice")
    # read test.txt
    print(sftp.open(f"{sftp_home_path}/{username}/test.txt", "r").read())

    # write test.txt
    sftp.open(f"{sftp_home_path}/{username}/test.txt", "w").write("hello bob")
    # read test.txt
    print(sftp.open(f"{sftp_home_path}/{username}/test.txt", "r").read())

    console_url = (
        f"https://console.aws.amazon.com/s3/buckets"
        f"/{bucket}?prefix={prefix}/{username}/"
    )
    print(f"preview the file on SFTP at: {console_url}")
