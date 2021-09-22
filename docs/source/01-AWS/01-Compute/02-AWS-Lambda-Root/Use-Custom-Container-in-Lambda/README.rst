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
- Using container images with Lambda: https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html


2. Example
------------------------------------------------------------------------------

Let's make a

.. code-block:: bash

    # Create virtualenv here at /venv
    virtualenv -p python3.8 venv

    # activate virtualenv
    source ./venv/bin/activate

    #


