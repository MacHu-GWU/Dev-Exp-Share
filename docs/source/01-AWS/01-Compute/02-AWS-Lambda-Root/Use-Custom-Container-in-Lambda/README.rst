.. _use-custom-container-in-lambda:

Use Custom Container in Lambda
==============================================================================

.. contents::
    :depth: 1
    :local:


1. Overview
------------------------------------------------------------------------------

From Dec 2020, you can bring your own docker image / container to use with AWS Lambda.

Links:

- New for AWS Lambda – Container Image Support: https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
- AWS Lambda now supports container images as a packaging format: https://aws.amazon.com/about-aws/whats-new/2020/12/aws-lambda-now-supports-container-images-as-a-packaging-format/
- Using container images with Lambda: https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html


2. Example
------------------------------------------------------------------------------

.. code-block:: bash

    # build docker image
    docker build -t hello-world .

    # run container at port 9000 to take http request invokation
    docker run -p 9000:8080 hello-world

    # test lambda function locally
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

    # login to AWS ECR
    AWS_ACCOUNT_ID="$(aws sts get-caller-identity | jq '.Account' -r)"
    AWS_REGION="us-east-1"
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

    # create "hello-world" docker image repository
    aws ecr create-repository --repository-name hello-world --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

    # tag the newly built image
    docker tag hello-world:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/hello-world:latest

    # push to AWS ECR
    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/hello-world:latest

Then you can create a Lambda function from docker image and run test event.
