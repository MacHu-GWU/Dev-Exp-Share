Collect Metrics and Logs with Cloudwatch Agent
==============================================================================

This document is a summary of official doc https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html. The original document are highly break down into many small document. This document put most important steps all together.


.. contents::
    :depth: 1
    :local:

This document is based on Amazon Linux / RedHat. For equivalent command on other OS, the official docs anchor is attached near each step.


1. Install Cloudwatch Agent
------------------------------------------------------------------------------

1. check if it is installed. For Windows, see https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/troubleshooting-CloudWatch-Agent.html#CloudWatch-Agent-files-and-locations::

    ls /opt/aws
    ls /opt/aws | grep amazon-cloudwatch-agent
    ls /opt/aws/amazon-cloudwatch-agent/bin
    ls /opt/aws/amazon-cloudwatch-agent/bin | amazon-cloudwatch-agent-ctl

2. install it via command line, for other installation method, see https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-EC2-Instance.html:

    sudo yum install -y amazon-cloudwatch-agent

3. verify if it successfully installed::

    ls /opt/aws/amazon-cloudwatch-agent/bin


2. Create the CloudWatch Agent Configuration File
------------------------------------------------------------------------------

For the first time playing with it, I recommend using configuration wizard.


    /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard


1. manually edit config file

    sudo vi /opt/aws/amazon-cloudwatch-agent/etc/config.json

.. code-block:: javascript

    {
        "agent": {
            "metrics_collection_interval": 60,
            "run_as_user": "root"
        },
        "metrics": {
            "append_dimensions": {
                "AutoScalingGroupName": "${aws:AutoScalingGroupName}",
                "ImageId": "${aws:ImageId}",
                "InstanceId": "${aws:InstanceId}",
                "InstanceType": "${aws:InstanceType}"
            },
            "metrics_collected": {
                "collectd": {
                    "metrics_aggregation_interval": 60
                },
                "disk": {
                    "measurement": [
                        "used_percent"
                    ],
                    "metrics_collection_interval": 60,
                    "resources": [
                        "*"
                    ]
                },
                "mem": {
                    "measurement": [
                        "mem_used_percent"
                    ],
                    "metrics_collection_interval": 60
                },
                "statsd": {
                    "metrics_aggregation_interval": 60,
                    "metrics_collection_interval": 10,
                    "service_address": ":8125"
                }
            }
        }
    }


2. Install dependencies ``collectd``, https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-custom-metrics-collectd.html::

    which collectd
    sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    sudo yum install -y collectd

3. Start the cloudwatch agent::

    # start it
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json

    # check running status
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status

    # stop it
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a stop


cat /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log