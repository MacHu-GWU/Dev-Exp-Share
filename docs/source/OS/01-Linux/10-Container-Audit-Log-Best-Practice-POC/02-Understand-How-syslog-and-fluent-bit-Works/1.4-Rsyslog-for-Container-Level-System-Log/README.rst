Rsyslog for Container Level System Log
==============================================================================

In this example, assuming you are managing a Server running many container applications. You want to use ``rsyslog`` to collect container audit log.

For ``rsyslog``, a ``rsyslog`` service is running on Server. And you need to change the config to allow it listen to UDP 514 port. Because your container won't have access to the ``/dev/log`` on the host, it has to use the network to talk to syslog on your host.

For docker, you need to specified ``log-driver=syslog`` when running your containers. Logs are stored on Host disk.

1. **Install and Run docker daemon**::

    # Install
    sudo amazon-linux-extras install docker

    # Run
    sudo service docker start

2. **Change rsyslog config**::

    # back up the default rsyslog.conf file
    sudo cp /etc/rsyslog.conf /etc/rsyslog.conf.bkp

    # change rsyslog.conf file
    vi /etc/rsyslog.conf

    # uncomment these two line, it should looks like
    $ModLoad imudp.so
    $UDPServerRun 514

3. **Run a test container using log driver** ``syslog``::

    # Reference: https://docs.docker.com/config/containers/logging/syslog/
    # invoke container system command, generate some log
    repo_name="ubuntu"
    sudo docker run --log-driver syslog --log-opt syslog-address=udp://127.0.0.1:514 ${repo_name} echo Hello World

    # view the most recent log
    sudo tail -n 10 /var/log/messages
