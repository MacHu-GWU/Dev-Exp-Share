# -*- coding: utf-8 -*-

from awacs.aws import (
    PolicyDocument,
    Principal,
    Statement,
    Allow,
    Deny,
    Action,
)
from awacs import (
    iam,
    sts,
)

trust_entity_policy = PolicyDocument(
    Version="2012-10-17",
    Id="trust-entity",
    Statement=[
        Statement(
            Sid="1",
            Effect=Allow,
            Principal=Principal("AWS", iam.ARN("user/sanhe")),
            Action=[
                sts.AssumeRole,
            ],
        )
    ]
)
print(trust_entity_policy.to_json())

admin_policy = PolicyDocument(
    Version="2012-10-17",
    Id="AdminPermission",
    Statement=[
        Statement(
            Sid="1",
            Effect=Allow,
            Action=[
                Action("*")
            ],
            Resource=[
                "*"
            ]
        )
    ]
)
print(admin_policy.to_json())
