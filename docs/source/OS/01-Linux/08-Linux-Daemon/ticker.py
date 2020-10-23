#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script demonstrate how to write a right daemon in python, it uses python-daemon=2.2.4.

This script is based on https://www.python.org/dev/peps/pep-3143/

How to run this script:

1. run ``sudo python ticker.py``

Check is is actually running:

1. run ``ls -l  /var/run | grep daemon-example-ticker`` there should be a ``.pid.lock`` file

How to kill this daemon:

1. run ``ps axj | grep ticker.py``, find the PID
2. run ``sudo kill $PID``
3. after you it is killed, ``ls -l  /var/run | grep daemon-example-ticker`` should returns nothing

中文文档:

如果你多次运行同一个 daemon script, 好像只有一个会起作用. 但是你可以在 ps axj 中看到多个守护进程. 而要彻底关掉这些守护进程, 需要将他们全部 kill 才行. 不知道 python-daemon 是如何实现重复运行一个 script 但只有一个起作用的.
"""

import os
import time
import datetime

import daemon
import signal
import grp
import lockfile


HERE = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(HERE, "ticker.log")

def initial_program_setup():
    pass


def do_main_program():
    while True:
        time.sleep(5)
        with open(log_file, "a") as f:
            f.write(str(datetime.datetime.utcnow()) + "\n")


def program_cleanup():
    pass


def reload_program_config():
    pass


context = daemon.DaemonContext(
    working_directory=HERE,
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/daemon-example-ticker.pid'),
)

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
}

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

initial_program_setup()

with context:
    do_main_program()
