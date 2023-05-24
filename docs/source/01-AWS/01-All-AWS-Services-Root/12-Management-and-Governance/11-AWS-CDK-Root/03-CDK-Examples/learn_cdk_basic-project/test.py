import os
import pytest
import aws_cdk as cdk
import aws_cdk.assertions as assertions

from learn_cdk_basic.stacks import MyCDKStack1, MyCDKStack2


def test_sqs_queue_created():
    app = cdk.App()
    stack = MyCDKStack1(app, "my-cdk-stack-1")
    template = assertions.Template.from_stack(stack)
    stack = MyCDKStack2(app, "my-cdk-stack-2")
    template = assertions.Template.from_stack(stack)


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
