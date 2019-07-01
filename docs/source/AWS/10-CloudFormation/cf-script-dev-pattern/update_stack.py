# -*- coding: utf-8 -*-

"""
我们的 cloudformation script 采用了一个 main stack ``my-service.json``, 多个 nested stack ``my-service-iam-role-tier.json``, ``my-service-s3-tier.json``, 然后再 main stack 中引用其他的 stack, 所有的 stack 共享一套参数 ``config.json``. 这样的架构.

其中所有的 nested stack 都是一串互相之间没有依赖关系的子 stack

我们希望每完成一个 child stack 时, 我们可以

- 传入的 parameters 必须要在 template 中进行声明
- template 中声明过的 parameters 没有被用到并没有关系
"""

import boto3
from superjson import json

from pathlib_mate import PathCls as Path

def pprint(data):
    print(json.dumps(data, sort_keys=True, indent=4))

aws_profile = "skymap_sandbox"
session = boto3.session.Session(profile_name=aws_profile)

cf = session.client("cloudformation")

p_parameters_input = Path(__file__).change(new_basename="config.json")
p_final_template = Path(__file__).change(new_basename="my-service-iam-role-tier.json")

config_data = json.loads(p_parameters_input.read_text("utf-8"))
stack_name = config_data["StackName"]
template_body = p_final_template.read_text("utf-8")
parameters = [
    {"ParameterKey": k, "ParameterValue": v}
    for k, v in config_data.items()
]

def create_stack(**kwargs):
    return cf.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=parameters,
        Capabilities=[
            "CAPABILITY_NAMED_IAM",
        ],
        **kwargs
    )

def update_stack(**kwargs):
    return cf.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=parameters,
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
    create_stack()
    # create_or_update()
    # delete_stack()