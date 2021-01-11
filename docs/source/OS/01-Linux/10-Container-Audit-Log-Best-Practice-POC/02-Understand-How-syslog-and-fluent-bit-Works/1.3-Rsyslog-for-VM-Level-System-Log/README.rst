Rsyslog for VM Level System Log
==============================================================================

.. contents::
    :depth: 1
    :local:

In this example, assuming you are a old fashion linux admin, you want to use ``rsyslog`` to collect system audit log.


Quick Start
------------------------------------------------------------------------------
To get started, launch an Amazon Linux EC2 and ssh into it.

Amazon Linux already have rsyslog installed and running as a service when start up.

Verify rsyslog is already installed as a service::

    systemctl list-unit-files --type service | grep rsyslog

Here's some commands to run, stop, restart, check status::

    # start
    systemctl start rsyslog

    # stop
    systemctl stop rsyslog

    # restart
    systemctl restart rsyslog

    # check status
    systemctl status rsyslog

The rsyslog configuration file locates at ``/etc/rsyslog.conf``, You should back up the default configure and then customize it with confidence::

    # view rsyslog config
    # to update configure, you can back the default file, change it,
    # and restart service with ``systemctl restart rsyslog``
    cat /etc/rsyslog.conf

    # backup rsyslog config file
    sudo cp /etc/rsyslog.conf /etc/rsyslog.config.bkp

By default, rsyslog will write different type of logs to different files in ``/var/log`` directory, most of system log are stored in ``/var/log/messages`` file::

    # browse log directory, by default, log files locate at /var/log directory
    # carefully read /etc/rsyslog.conf file to understand each file are storing what type of logs
    # most of common system log are stored in /var/log/messages
    ls /var/log -l

    # view last 10 line
    sudo tail -n 10 /var/log/messages

    # monitor new coming lines as live-stream
    sudo tail -f /var/log/messages

Again we should be aware that rsyslog is designed for system log. It WON't log your command line input output history, message sent to stdout/stderr that generated from your application. But you do can do some customization to enable that.

Now let's generate some logs to see if rsyslog captures it


Example.1 Manually Generate System Log and Sent to rsyslog
------------------------------------------------------------------------------

There's a built-in shell command interface allows you to send log to syslog, it is ``logger`` (https://linux.die.net/man/1/logger) ::

    # send dummy log to rsyslog
    logger -t myapp Hello World

    # view the log
    sudo tail -n 10 /var/log/messages


Example.2 Send log to rsyslog From Your Application
------------------------------------------------------------------------------
We can write a simple python script called ``rsyslog-example-app.py`` using Python Standard Library logging (https://docs.python.org/3/library/logging.handlers.html#sysloghandler) ::

    # -*- coding: utf-8 -*-
    # content of rsyslog-example-app.py file

    import sys
    import logging.handlers

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    syslog_handler = logging.handlers.SysLogHandler("/dev/log")
    syslog_handler.setLevel(logging.INFO)
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    msg = "Hello Amazon"
    logger.info(msg)

Then generate some log::

    # generate dummy log
    python rsyslog-example-app.py

    # view the log
    sudo tail -n 10 /var/log/messages

Note:

    by default (take a look at your ``/etc/rsyslog.conf`` file), rsyslog are listening the ``/dev/log``. These two line are commented out by default::

        $ModLoad imudp.so
        $UDPServerRun 514

    That's why we have ``syslog_handler = logging.handlers.SysLogHandler("/dev/log")`` is in our python code.

    If you want your rsyslog using UDP and listen to default port 514, you can simple ``systemctl stop rsyslog``, then uncomment the two lines above in ``/etc/rsyslog.conf`` file, and then ``systemctl start rsyslog``. Then change your python code to ``syslog_handler = logging.handlers.SysLogHandler()``. The ``logging.handlers.SysLogHandler()`` uses UDP 514 by default.


Example.3: Log your Command line input output history
------------------------------------------------------------------------------
Your can log the command line input output history with rsyslog as well. Just Follow this post https://askubuntu.com/questions/161935/how-do-i-log-all-input-and-output-in-a-terminal-session. The idea is send a copy of your shell history to rsyslog by adding some customization code in your ``.bashrc`` file.


Reference
------------------------------------------------------------------------------
- Rsyslog Official: https://www.rsyslog.com/
