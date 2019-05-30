# -*- coding: utf-8 -*-

"""
cloudformation boto3 api:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#client
"""

import boto3
from superjson import json

from pathlib_mate import PathCls as Path

def pprint(data):
    print(json.dumps(data, sort_keys=True, indent=4))

aws_profile = "skymap_sandbox"
stack_name = "test-stack"
session = boto3.session.Session(profile_name=aws_profile)

cf = session.client("cloudformation")

p_final_template = Path(__file__).change(new_basename="test.json")
template_body = json.dumps(json.loads(p_final_template.read_text("utf-8"), ignore_comments=True))

def create_stack(**kwargs):
    return cf.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=[
            "CAPABILITY_NAMED_IAM",
        ],
        **kwargs
    )

def update_stack(**kwargs):
    return cf.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=[
            "CAPABILITY_NAMED_IAM",
        ],
        **kwargs
    )

def delete_stack(**kwargs):
    return cf.delete_stack(
        StackName=stack_name,
        **kwargs
    )


def create_or_update(**kwargs):
    try:
        _ = cf.describe_stacks(
            StackName=stack_name
        )
        return update_stack(**kwargs)
    except Exception as e:
        if "does not exist" in str(e):
            return create_stack(**kwargs)
        else:
            raise e


if __name__ == "__main__":
    """
    """
    # create_stack()
    # create_or_update()
    delete_stack()