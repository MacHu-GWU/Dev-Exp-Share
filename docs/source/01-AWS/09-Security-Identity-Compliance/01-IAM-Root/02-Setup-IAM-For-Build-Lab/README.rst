Setup IAM For Build Lab
==============================================================================
- ``your-common-prefix``

::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "iam:AttachRolePolicy",
                    "iam:CreatePolicy",
                    "iam:CreatePolicyVersion",
                    "iam:CreateRole",
                    "iam:DeletePolicy",
                    "iam:DeletePolicyVersion",
                    "iam:DeleteRole",
                    "iam:DeleteRolePermissionsBoundary",
                    "iam:DeleteRolePolicy",
                    "iam:DetachRolePolicy",
                    "iam:PassRole",
                    "iam:PutRolePermissionsBoundary",
                    "iam:PutRolePolicy",
                    "iam:SetDefaultPolicyVersion",
                    "iam:UpdateAssumeRolePolicy",
                    "iam:UpdateRole",
                    "iam:UpdateRoleDescription"
                ],
                "Resource": [
                    "arn:aws:iam::279139072714:role/your-common-prefix*",
                    "arn:aws:iam::279139072714:policy/your-common-prefix*"
                ]
            }
        ]
    }