AWS CloudWatch 5 min Tutorial
==============================================================================


What is CloudWatch?
------------------------------------------------------------------------------
1. centralized, cloud native log aggregation
2. event bridge, integrate with other service


Common Use case
------------------------------------------------------------------------------
1. logging + full text search
2. metrics monitoring
    - CPU / memory / disk usage
3. event bridge to connect other services
    - cron job
    - event trigger


How it Works?
------------------------------------------------------------------------------
For Native AWS Service, there are many built-in service and Cloudwatch agent are widely available on those service, you can use metrics out-of-the-box.

Cloudwatch agent is where the magic happen.

- monitor CPU / memory / GPU / disk
- monitor standard output / error


How it work with Other Service?
------------------------------------------------------------------------------
Cloudwatch + EC2 / EMR / Glue / Lambda / ECS / EKS / Sagemaker / RDS / Dynamodb ...


How to Custom it?
------------------------------------------------------------------------------
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_log_events
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_composite_alarm

.. code-block:: python

    import boto3

    client = boto3.client("logs")
    client.put_log_events(logGroupName="...", logStreamName="...", logEvents=...)


    client = boto3.client("cloudwatch")
    client.put_composite_alarm(AlarmRule=..., AlarmActions=...)
