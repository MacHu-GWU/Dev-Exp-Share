My AWS Help Community Post
------------------------------------------------------------------------------

Another "Unable to determine service/operation name to be authorized" Prob

Hi Genius!

I am building an API Gateway with Lambda Function

{code}https://<endpoint>/user?user_id=3{code}

I am following every single detail of the AWS Tutorial, Integration 1: Create a GET Method with Query Parameters to Call the Lambda Function: [https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-lambda.html#api-as-lambda-proxy-expose-get-method-with-query-strings-to-call-lambda-function]. *Carefully setup, IAM Role, Policy, Integration Request, Method Request Configuration, but still experiencing the "Unable to determine service/operation name to be authorized"* Error. I also have read this thread [https://forums.aws.amazon.com/thread.jspa?threadID=209420] but none of the solutions fixed the problem.

In the Method Execution, The Request is: /user?user_id=3

I think *the query string is properly transformed to the correct event json*:

{code}
Sun May 19 08:26:21 UTC 2019 : Endpoint request body after transformations: {
    "user_id": "3"
}
{code}

And finally it gives me the response:

{code}
<AccessDeniedException>
  <Message>Unable to determine service/operation name to be authorized</Message>
</AccessDeniedException>
{code}

I am pretty sure that:

1. In "Integration Request", the "Http Method" is Post
2. In "Integration Request", the "path override" is /2015-03-31/functions/arn:aws:lambda:us-east-1:<account-id>:function:<lambda-func-name>/invokations
3. The IAM Role for the Integration Request has API Gateway and Lambda as trusted relationship, and lambda invoke, lambda execution policy is properly configured based on the tutorial [https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-lambda.html#api-as-lambda-proxy-setup-iam-role-policies]

*Anyone could give me hint of WHAT COULD BE WRONG?*

Here's my configuration:

*Integration Request* Settings:

- Integration type :Lambda Function
- AWS Region: us-east-1
- AWS Service: Lambda
- AWS Subdomain: blank
- HTTP method: POST
- Path override: 2015-03-31/functions/arn:aws:lambda:us-east-1:<account-id>:function:<function-name>/invokations
- Execution role: arn:aws:iam::<account-id>:role/<role-name>
- Content Handling: Passthrough
- Use Default Timeout: True

*The Lambda Code*, function is not in VPC:

{code}
# python code
# just want want to see the event
def lambda_handler(event, context):
    return {'event': event}
{code}

*IAM Role - Trusted Relationship*

{code}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "apigateway.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
{code}

*Attached Policy*

- AmazonAPIGatewayPushToCloudWatchLogs: [https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs$jsonEditor]
- AWSLambdaExecute: [https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AWSLambdaExecute$jsonEditor]
- InvokeLambda:

{code}
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "*"
        }
    ]
}
{code}

I appreciate that you read all this. Thank you!