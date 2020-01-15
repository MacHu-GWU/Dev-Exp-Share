# -*- coding: utf-8 -*-

from fabric2 import Connection
from invoke import Result
from paramiko import SFTPClient
from patchwork.transfers import rsync
from pathlib_mate import PathCls as Path

_ = Result
_ = SFTPClient


HOME = Path.home()
HERE = Path(__file__).parent


def initialize():
    Path(HERE, "data.json").remove()


initialize()

# config connection
with Connection(
    host="ec2-107-23-119-62.compute-1.amazonaws.com",
    user="ec2-user",
    connect_kwargs=dict(
        key_filename=[
            Path(HOME, "ec2-pem", "eq-sanhe-dev.pem").abspath,
        ]
    )
) as conn:
    # put file to remote
    conn.put(Path(HERE, "test.json"), "/tmp/test.json")

    # send command, see if the test.json file already on remote
    result = conn.run('cat /tmp/test.json', hide=True) # type: Result
    # print(result.stdout)
    # print(result.stderr)
    # print(result.encoding)
    # print(result.command)
    # print(result.shell)
    # print(result.env)
    # print(result.exited)

    # get file from remote
    conn.run('echo "{\\"name\\": \\"Bob\\"}" > /tmp/data.json') # create a temp file on remote
    conn.get("/tmp/data.json", Path(HERE, "data.json")) # get it from here

    # sync folder from local to remote, like google drive
    rsync(conn, source=Path(HERE, "test-folder"), target="/tmp")
    conn.run('cat /tmp/test-folder/index.html')

    # sync folder from remote to local, like google drive
    rsync(conn, source=HERE, target="/tmp/test-folder", remote_to_local=True) # will be available in 1.0.2
    conn.local('cat {}'.format(Path(HERE, "test-folder", "index.html").abspath))
