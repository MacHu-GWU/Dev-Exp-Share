# -*- coding: utf-8 -*-

import aws_cdk.core as core
import aws_cdk.aws_s3 as s3


env_eq_sanhe = core.Environment(region="us-east-1")

class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        s3.Bucket(self, "MyFirstWonderfulBucket", versioned=True)

app = core.App()

MyStack(app, "MyStack", env=env_eq_sanhe)

app.synth()
