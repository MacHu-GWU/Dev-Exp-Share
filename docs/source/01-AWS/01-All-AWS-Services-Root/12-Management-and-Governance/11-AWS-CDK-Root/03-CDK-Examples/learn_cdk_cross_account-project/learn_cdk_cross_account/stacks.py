import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct


class MyCDKStack1(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam.CfnGroup(
            self,
            "IamGroup",
            group_name="my-cdk-stack-1-iam-group",

        )


class MyCDKStack2(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam.Group(
            self,
            "IamGroup",
            group_name="my-cdk-stack-2-iam-group",
        )