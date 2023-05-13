# -*- coding: utf-8 -*-

from io import StringIO
from paramiko import AutoAddPolicy, SFTPClient, SSHClient
from paramiko import RSAKey
import spurplus

def sftp_connect(
    sftp_hostname: str,
    sftp_username: str,
    sftp_port: int,
    ssh_private_key: str,
    ssh_password: str,
) -> SFTPClient:
    private_key = RSAKey.from_private_key(
        StringIO(ssh_private_key),
        password=ssh_password,
    )
    ssh_client = SSHClient()
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

from pathlib import Path
import spur
path_pk = Path.home().joinpath(".ssh", "id_rsa")

host = "s-0c8ef48cdf5e481bb.server.transfer.us-east-1.amazonaws.com"
sftp = sftp_connect(
    sftp_hostname=host,
    sftp_username="sanhe",
    sftp_port=22,
    ssh_private_key=path_pk.read_text(),
    ssh_password="sanhe",
)

print(sftp.open("/878625312159-us-east-1-data/sanhe/README.rst", "r").read())
print(sftp.open("/878625312159-us-east-1-data/sanhe/README.rst", "w").write("hello world"))
print(sftp.open("/878625312159-us-east-1-data/sanhe/README.rst", "r").read())

# with spurplus.connect_with_retries(
#     hostname=host,
#     port=22,
#     username="sanhe",
#     password="sanhe",
#     private_key_file=path_pk,
#     retries=0,
#     missing_host_key=spur.ssh.MissingHostKey.accept,
#     # load_system_host_keys=True,
# ) as shell:
#     p = Path("/878625312159-us-east-1-data/sanhe/README.rst")
#     print(shell.read_text(p))
#     shell.write_text(p, "hello world")
#     print(shell.read_text(p))
# for p in sftp.listdir("/878625312159-us-east-1-data/sanhe"):
#     print(p.read())



# sftp.put("README.rst", "/878625312159-us-east-1-data/sanhe/README.rst")