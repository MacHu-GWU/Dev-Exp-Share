Understand How syslog and fluent-bit Works
==============================================================================

This document aims to build knowledge base and hands on experience for syslog and fluent-bit.

The Learning Path looks like this:

- 1.1. Understand what is syslog (and rsyslog), what problem it solves, how does it solve the problem.
- 1.2. Installing rsyslog, understand files structure, how to manage the rsyslog service and configure it.
- 1.3. Use case 1, Use rsyslog for VM level system log.
- 1.4. Use case 2, Use rsyslog for Container level system log.
- 1.5. Use case 3, Dedicated rsyslog server, and collect logs via UDP/TCP.
- 1.6. More common use cases and variations of the configuration.
- 2.1. Understand what is fluent-bit (and fluentd), what problem it solves, how does it solve the problem.
- 2.2. Core concepts Pipeline, Input, Output
- 2.3. Fluent-bit conventional docker image
- 2.4. Use case 1.1, input=forward, output=standard out, deploy fluent-bit container to single Node, test with application container.
- 2.5. Use case 1.2, input=forward, output=file, deploy fluent-bit container to single Node, test with application container.
- 2.6. Use case 1.3, input=forward, output=aws s3, deploy fluent-bit container to single Node, test with application container.
- 2.7. Use case 2.1, input=syslog, output=standard out, deploy fluent-bit container to single Node, test with application container.
- 2.8. Use case 2.2, input=syslog, output=s3, deploy fluent-bit container to single Node, test with application container.
- 3.1. Understand fluent-bit deployment on K8S, AWS EKS.
- 3.2. Use case, deploy fluent-bit daemon set to EKS, input=syslog, output=aws s3, and deploy a test application.
- 3.3. To be continue ...

Before we get to real K8S Cluster, we use a Amazon Linux EC2 Instance to simulate single nodes on EKS. Once you are familiar with the configuration and deployment, then you will be ready to move on to K8S version of deployment.

EC2 properties:

- ami: amazon linux
- network: public subnet or private subnet + vpn, just make sure you can ssh in
- instance type: t2.medium
- disk: 8 gb is fine
- security group: allow ssh in from your ip
- iam role: AWS S3 read and write access to single test s3 bucket

SSH into it::

    EC2_USER="ec2-user"
    EC2_IP="111.111.111.111"
    EC2_PEM="/path-to-pem-file"
    echo EC2_PEM="${EC2_PEM}", EC2_USER="${EC2_USER}", EC2_IP="${EC2_IP}" && ssh -i ${EC2_PEM} ${EC2_USER}@${EC2_IP}


Table Of Content
------------------------------------------------------------------------------

- `<1.1-What-is-syslog/README.rst>`_
- `<1.3-Rsyslog-for-VM-Level-System-Log/README.rst>`_
- `<1.4-Rsyslog-for-Container-Level-System-Log/README.rst>`_
- `<2.1-What-is-fluent-bit/README.rst>`_
- `<2.2-Use-case-input-forward-output-standard-out/README.rst>`_
- `<2.3-Use-case-input-forward-output-file/README.rst>`_
- `<2.4-Use-case-input-forward-output-aws-s3/README.rst>`_
- `<2.8-Use-case-input-syslog-output-standard-out/README.rst>`_
- `<2.9-Use-case-input-syslog-output-s3/README.rst>`_
- `<3.2-Use-case-fluent-bit-syslog-s3-on-EKS/README.rst>`_
