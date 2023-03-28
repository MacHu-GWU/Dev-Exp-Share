IOT Rule Engine
==============================================================================

loT Rules allow your devices to interact with AWS services. Rules are analyzed and trigger actions based on the MQTT topic stream. Rules allow you to do things like:
 
- Save files to AmazorkS3
- Send information to SQS or SNS.
- Invoke a Lambda function to extract or process data.
- Process large numbers of messages with Amazon Kinesis.
- Integrate with a variety of other AWS services including CloudWatch, AML, Step Functions, DynamoDB, and the Amazon Elasticsearch Service.

Configuring loT Rules:

To use loT Rules, you'll need to go through a few different steps:

1. Configure the IAM permissions required for loT to access any relevant AWS services.
2. Create an loT Rule:
    a. Pick a rule name and optional description.
    b. Write an loT SQL statement to filter MQTT topic messages and push the data elsewhere.
    c. Select the version of loT SQL to use.
    d. Set one or more actions to take when executing the rule (send data to a DynamoDB table or write it to S3 for example).
    e. Set an error action just in case the earlier actions fail.
