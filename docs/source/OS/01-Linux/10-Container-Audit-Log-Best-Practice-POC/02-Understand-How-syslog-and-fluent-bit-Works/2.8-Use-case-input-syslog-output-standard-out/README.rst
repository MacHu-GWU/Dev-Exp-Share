Use case, Input forward, Output standard out
==============================================================================

In this example, we will use Single VM (Node), and run one fluent bit container to mock the Daemon set, and run another app container to mock the application. We use syslog to collect container runtime log.

**Update rsyslog configuration**:

1. Add a new file to your rsyslog config rules called ``60-fluent-bit.conf`` inside the directory ``/etc/rsyslog.d/``. It is like inheritance in any Objective oriented programming language. The child config will inherit all parent config at ``/etc/rsyslog.conf``. But overwrite part of them using ``/etc/rsyslog.d/60-fluent-bit.conf``. And place the following content::

    $ModLoad omuxsock
    $OMUxSockSocket /tmp/fluent-bit.sock
    *.* :omuxsock:

2. Restart rsyslog::

    sudo systemctl restart rsyslog

**Run fluent-bit service container**::

    # Setup variables
    repo_name="fluent/fluent-bit" # https://hub.docker.com/r/fluent/fluent-bit/
    container_name="fluent-bit-deamon-set"

    # Based on /etc/rsyslog.d/60-fluent-bit.conf file, rsyslog is sending log to the /tmp/fluent-bit.sock file on host
    # This file will be created by fluent-bit in its container at ``/tmp/fluent-bit.sock``,
    # which is defined as a parameter as ``-p path=/tmp/fluent-bit.sock``
    # so we need to mount the /tmp on host on /tmp of the fluent-bit container
    sudo docker run --rm --name "${container_name}" -p 127.0.0.1:24224:24224 --mount type=bind,source=/tmp,target=/tmp ${repo_name} /fluent-bit/bin/fluent-bit -R /fluent-bit/etc/parsers.conf -i syslog -p parser=syslog-rfc3164 -p path=/tmp/fluent-bit.sock -p mode=unix_udp -p unix_perm="0644" -o stdout -f 1

**Run app container, generate some logs**::

    # Setup variables
    repo_name="ubuntu" # https://hub.docker.com/_/ubuntu

    # Use log-driver=syslog, the application container won't feel the existence of
    # fluent-bit container, because app container send log to rsyslog,
    # then rsyslog send log to fluent-bit
    sudo docker run --log-driver syslog ${repo_name} echo Hello World

**Pitfalls**:

- Q: It gives me ``[in_syslog] parser not set`` error. From the fluent-bit syslog input plugin document (https://docs.fluentbit.io/manual/pipeline/inputs/syslog#configuration-file), it says I need to specify a parser file. But It doesn't say **WHAT IS THE PARSER FILE SHOULD LOOKS LIKE!**
- A: Since fluent-bit itself doens't generate any log, it just collect logs from other logging tools like ``syslog``, it always has to parser the source log into a structure format (https://docs.fluentbit.io/manual/concepts/key-concepts#structured-messages). There's an option called ``-R`` or ``--parser`` allow you to specify the path of the parser file regardless of what input you are using. fluent-bit team is maintaining a official parser file here https://github.com/fluent/fluent-bit/blob/master/conf/parsers.conf. When your fluent-bit ``input=syslog``, you could use one of ``syslog-rfc3164``, ``syslog-rfc3164-local`` and ``syslog-rfc5424`` in arguments like ``-p parser=syslog-rfc3164``. In production, you most likely are using a fluent-bit conventional docker image (https://hub.docker.com/r/fluent/fluent-bit/) running on every single nodes (VM). The ``Dockerfile`` indicates that the official ``parsers.conf`` file locates at ``/fluent-bit/etc/parsers.conf``, **this information is NOT MENTIONED anywhere**. In conclusion, when you are using fluent-bit conventional docker image, you have to specify ``--parser /fluent-bit/etc/parsers.conf``. When you are using other conventional docker image, you should look into their ``Dockerfile`` to figure out where it locates at.

- Q: In the previous use case, you are using ``log-driver=fluentd``, I cannot make the application container sending log to fluent-bit. How come?
- A: Since We are trying to collect container runtime log, which is generated from syslog. So fluent-bit INPUT has to be syslog. There's a OUTPUT fluent-bit plugin also called ``syslog``, which is not used here. The log pipeline is: docker daemon log-driver=syslog generates log from app container, log sent to VM level syslog, syslog forward it to fluent-bit, fluent-bit process it then send it to output. The app container no need to know the existence of fluent-bit container.
