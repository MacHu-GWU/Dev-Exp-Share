#!/usr/bin/env python3

import aws_cdk as cdk
from learn_cdk_cross_account.stacks import MyCDKStack1, MyCDKStack2

app = cdk.App()
MyCDKStack1(app, "my-cdk-stack-1")
MyCDKStack2(app, "my-cdk-stack-2")
app.synth()