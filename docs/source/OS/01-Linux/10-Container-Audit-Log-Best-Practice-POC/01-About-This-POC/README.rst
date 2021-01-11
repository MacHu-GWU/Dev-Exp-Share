About This POC
==============================================================================

.. contents::
    :depth: 1
    :local:


What is Container Audit Log
------------------------------------------------------------------------------

Suppose we have many containerized application on a K8S cluster, we may care about these three types of log:

1. **VM System Log**: Each node has system log, including information like:
    - user login attempts
    - system command call
    - service information
2. **Container Runtime Log**: When running a container, it also invokes some system commands with in the container. Which is also called "container runtime log". For example, an application container usually has a ENTRY POINT command, and this commands may also invokes other system commands. If container is running with "detached" mode with "terminal" (option ``-dt``), user may enter the container shell. All these events are considered as "Container Runtime Log"

Note:

    However, since most of use of container are hitting the ENTRY POINT with some parameters, there should be very few system call event in the entire container life cycle.

3. **Application Log**: The application also generates a big amount of logs, for example, a web server may log who attempted to log in, and backend database call may also need to be logged, and error message and catched exception are very useful for debug.

For #2, specifically for K8S cluster, it allows us to identify unauthorized access to container, Container level system error

Usually #3 are handled by ELK (ElasticSearch + LogStash + Kibana), Splunk, AWS Cloudwatch or other log aggregation service. And #1 are handled by ``syslog``, by default you need additional effort to aggregate those log from Nodes. **In this POC project, we will cover the best practice of #2 Container Runtime Log**.

Note:

    We may also interested terminal command line logs, VM / Container performance metrics log. But we will not cover those topics in this POC project.


The Solution
------------------------------------------------------------------------------

K8S Structure::

    |--- K8S Cluster
        |---Node1
            |--- rsyslog service running on each node
            |--- fluent-bit Daemonset (pod)
            |--- service_1
                |--- pod1 ...
                    |--- container1 ...
                    |--- container2 ...
                    ...
            |--- service_2
                |--- pod1 ...
                    |--- containers ...
            ...
        |---Node2
            |--- rsyslog service running on each node
            |--- fluent-bit Daemonset (pod)
            |--- service_1
                |--- pod2 ...
                    |--- containers ...
            |--- service_2
                |--- pod2 ...
                    |--- containers ...
            ...

Log Lifecycle::

    containers (log driver = syslog)
    -> per Node rsyslog service
    -> per Node fluent-bit
    -> parser -> filter -> buffer -> routing
    -> send to customized output, AWS S3, ELK, etc ...

Description:

- rsyslog service are running on every single K8S nodes
- each node have a fluent-bit pod (daemon set) running on it
- all container running on the same node send container runtime log to node level syslog service
- fluent-bit is collecting log from rsyslog in realtime, parse, filter, and process it, then send to desired output.

Note

    fluent-bit supports not only syslog, it also works for all kinds of log. It support many different types of INPUT and OUTPUT.
    In this POC, the INPUT is ``syslog``.

Reference:

- Centralized Container Logging with Fluent Bit: https://aws.amazon.com/blogs/opensource/centralized-container-logging-fluent-bit/


Goal
------------------------------------------------------------------------------

- Understand How syslog and Fluent-bit works, how to configure and use it.
- Deploy Fluent-bit daemon set to K8S.
- Deploy application pods to K8S.
- Verify the logs been collected and stored on S3.
