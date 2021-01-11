# -*- coding: utf-8 -*-
# content of rsyslog-example-app.py file

import sys
import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

syslog_handler = logging.handlers.SysLogHandler("/dev/log") # /dev/log is for default setting of rsyslog
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(formatter)
logger.addHandler(syslog_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

msg = "Hello World"
logger.info(msg)
