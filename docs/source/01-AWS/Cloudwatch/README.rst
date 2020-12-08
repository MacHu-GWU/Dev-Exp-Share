
.. _aws-cloudwatch:

AWS CloudWatch
==============================================================================


- Cloudwatch Document Homepage: https://docs.aws.amazon.com/cloudwatch/index.html
- Cloudwatch: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
- Cloudwatch Event: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html
- Cloudwatch Log: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html



sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:

amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:config.json


sudo yum install amazon-cloudwatch-agent

