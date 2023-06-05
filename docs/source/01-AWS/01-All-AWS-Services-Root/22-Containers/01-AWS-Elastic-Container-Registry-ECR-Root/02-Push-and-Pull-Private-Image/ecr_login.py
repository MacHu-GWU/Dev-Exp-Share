# -*- coding: utf-8 -*-

"""
This shell script automates docker login to AWS ECR.

Requirements:

- Python3.7+
- `fire>=0.1.3,<1.0.0 <https://pypi.org/project/fire/>`_

Usage:

.. code-block:: bash

    $ python ecr_login.py -h
"""

import typing as T
import boto3
import base64
import subprocess

import fire


def get_ecr_auth_token_v1(
    ecr_client,
    aws_account_id,
) -> str:
    """
    Get ECR auth token using boto3 SDK.
    """
    res = ecr_client.get_authorization_token(
        registryIds=[
            aws_account_id,
        ],
    )
    b64_token = res["authorizationData"][0]["authorizationToken"]
    user_pass = base64.b64decode(b64_token.encode("utf-8")).decode("utf-8")
    auth_token = user_pass.split(":")[1]
    return auth_token


def get_ecr_auth_token_v2(
    aws_region: str,
    aws_profile: T.Optional[str] = None,
):
    """
    Get ECR auth token using AWS CLI.
    """
    args = ["aws", "ecr", "get-login", "--region", aws_region, "--no-include-email"]
    if aws_profile is not None:
        args.extend(["--profile", aws_profile])
    response = subprocess.run(args, check=True, capture_output=True)
    text = response.stdout.decode("utf-8")
    auth_token = text.split(" ")[5]
    return auth_token


def docker_login(
    auth_token: str,
    registry_url: str,
) -> bool:
    """
    Login docker cli to AWS ECR.

    :return: a boolean flag to indicate if the login is successful.
    """
    pipe = subprocess.Popen(["echo", auth_token], stdout=subprocess.PIPE)
    response = subprocess.run(
        ["docker", "login", "-u", "AWS", registry_url, "--password-stdin"],
        stdin=pipe.stdout,
        capture_output=True,
    )
    text = response.stdout.decode("utf-8")
    return "Login Succeeded" in text


def main(
    aws_profile: T.Optional[str] = None,
    aws_account_id: T.Optional[str] = None,
    aws_region: T.Optional[str] = None,
):
    """
    Login docker cli to AWS ECR using boto3 SDK and AWS CLI.

    :param aws_profile: specify the AWS profile you want to use to login.
        usually this parameter is used on local laptop that having awscli
        installed and configured.
    :param aws_account_id: explicitly specify the AWS account id. if it is not
        given, it will use the sts.get_caller_identity() to get the account id.
        you can use this to get the auth token for cross account access.
    :param aws_region: explicitly specify the AWS region for boto3 session
        and ecr repo. usually you need to set this on EC2, ECS, Cloud9,
        CloudShell, Lambda, etc ...
    """
    boto_ses = boto3.session.Session(
        region_name=aws_region,
        profile_name=aws_profile,
    )
    ecr_client = boto_ses.client("ecr")
    if aws_account_id is None:
        sts_client = boto_ses.client("sts")
        res = sts_client.get_caller_identity()
        aws_account_id = res["Account"]

    print("get ecr auth token ...")
    auth_token = get_ecr_auth_token_v1(
        ecr_client=ecr_client,
        aws_account_id=aws_account_id,
    )
    if aws_region is None:
        aws_region = boto_ses.region_name
    print("docker login ...")
    flag = docker_login(
        auth_token=auth_token,
        registry_url=f"https://{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com",
    )
    if flag:
        print("login succeeded!")
    else:
        print("login failed!")


def run():
    fire.Fire(main)


if __name__ == "__main__":
    run()
