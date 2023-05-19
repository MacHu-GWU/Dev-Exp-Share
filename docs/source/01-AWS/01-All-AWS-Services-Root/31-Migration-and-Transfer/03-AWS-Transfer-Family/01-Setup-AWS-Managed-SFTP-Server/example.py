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
    host = "s-1a2b3c4d.server.transfer.us-east-1.amazonaws.com"
    port = 22
    username = "username"
    path_pk = Path.home().joinpath(".ssh", "id_rsa")
    password = "password"
    sftp = sftp_connect(
        sftp_hostname=host,
        sftp_port=port,
        sftp_username=username,
        ssh_private_key=path_pk.read_text(),
        ssh_password=password,
    )

    bucket = "your-bucket-name"

    sftp.open(f"/{bucket}/{username}/test.txt", "w").write("hello alice")
    print(sftp.open(f"/{bucket}/{username}/test.txt", "r").read())
    sftp.open(f"/{bucket}/{username}/test.txt", "w").write("hello bob")
    print(sftp.open(f"/{bucket}/{username}/test.txt", "r").read())
