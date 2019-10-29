Use MFA Protection
==============================================================================

.. contents::
    :depth: 1
    :local:


Why MFA
------------------------------------------------------------------------------


Force User to use MFA even for AWS CLI
------------------------------------------------------------------------------

Reference:

- Using Multi-Factor Authentication (MFA) in AWS: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html
- How do I use an MFA token to authenticate access to my AWS resources through the AWS CLI?: https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
- Get IAM User of an AWS Profile: https://docs.aws.amazon.com/cli/latest/reference/sts/get-access-key-info.html
- Get AWS Region of an AWS Profile: https://docs.aws.amazon.com/cli/latest/reference/configure/get.html


How to Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ManageMFA`` - Allow User to Manage their MFA Device:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowUsersToCreateDeleteTheirOwnVirtualMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:*VirtualMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/${aws:username}"
                ]
            },
            {
                "Sid": "AllowUsersToEnableSyncDisableTheirOwnMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:DeactivateMFADevice",
                    "iam:EnableMFADevice",
                    "iam:ListMFADevices",
                    "iam:ResyncMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowUsersToListVirtualMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:ListVirtualMFADevices"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/*"
                ]
            },
            {
                "Sid": "AllowUsersToListUsersInConsole",
                "Effect": "Allow",
                "Action": [
                    "iam:ListUsers"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/*"
                ]
            },
            {
                "Sid": "AllowUsersToChangePassword",
                "Effect": "Allow",
                "Action": [
                    "iam:ChangePassword",
                    "iam:GetAccountPasswordPolicy",
                    "iam:ListUserPolicies",
                    "iam:GetLoginProfile",
                    "iam:UpdateLoginProfile"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            }
        ]
    }

``ForceMFA`` - Force to use MFA for AWS Console and Cli:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAllUsersToListAccounts",
                "Effect": "Allow",
                "Action": [
                    "iam:ListAccountAliases",
                    "iam:ListUsers"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/*"
                ]
            },
            {
                "Sid": "AllowIndividualUserToSeeTheirAccountInformation",
                "Effect": "Allow",
                "Action": [
                    "iam:ChangePassword",
                    "iam:CreateLoginProfile",
                    "iam:DeleteLoginProfile",
                    "iam:GetAccountPasswordPolicy",
                    "iam:GetAccountSummary",
                    "iam:GetLoginProfile",
                    "iam:UpdateLoginProfile"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowIndividualUserToListTheirMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:ListVirtualMFADevices",
                    "iam:ListMFADevices"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/*",
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowIndividualUserToManageThierMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:CreateVirtualMFADevice",
                    "iam:DeactivateMFADevice",
                    "iam:DeleteVirtualMFADevice",
                    "iam:EnableMFADevice",
                    "iam:ResyncMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/${aws:username}",
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "DoNotAllowAnythingOtherThanAboveUnlessMFAd",
                "Effect": "Deny",
                "NotAction": "iam:*",
                "Resource": "*",
                "Condition": {
                    "Null": {
                        "aws:MultiFactorAuthAge": "true"
                    }
                }
            }
        ]
    }

``ReadOnly`` - Only allow to read / list aws resource:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "autoscaling:Describe*",
                    "cloudformation:DescribeStacks",
                    "cloudformation:DescribeStackEvents",
                    "cloudformation:DescribeStackResources",
                    "cloudformation:GetTemplate",
                    "cloudformation:List*",
                    "cloudtrail:DescribeTrails",
                    "cloudtrail:GetTrailStatus",
                    "cloudwatch:Describe*",
                    "cloudwatch:Get*",
                    "cloudwatch:List*",
                    "directconnect:Describe*",
                    "ec2:Describe*",
                    "elasticloadbalancing:Describe*",
                    "iam:List*",
                    "iam:Get*",
                    "redshift:Describe*",
                    "redshift:ViewQueriesInConsole",
                    "rds:Describe*",
                    "rds:ListTagsForResource",
                    "s3:Get*",
                    "s3:List*",
                    "ses:Get*",
                    "ses:List*",
                    "sns:Get*",
                    "sns:List*",
                    "sqs:GetQueueAttributes",
                    "sqs:ListQueues",
                    "sqs:ReceiveMessage"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

``Ec2RestrictAccess`` - Don't allow to touch set of EC2 instance:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Condition": {
                    "StringLike": {
                        "ec2:ResourceTag/Name": "CSR*"
                    }
                },
                "Action": [
                    "ec2:TerminateInstances",
                    "ec2:DeleteTags",
                    "ec2:StartInstances",
                    "ec2:CreateTags",
                    "ec2:StopInstances"
                ],
                "Resource": "arn:aws:ec2:us-east-1:*:instance/*",
                "Effect": "Deny"
            }
        ]
    }


``CreateIamRole`` - Allow to Create IAM Role:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeIamInstanceProfileAssociations",
                    "iam:GetRole",
                    "iam:GetPolicyVersion",
                    "iam:GetPolicy",
                    "iam:AttachUserPolicy",
                    "iam:ListEntitiesForPolicy",
                    "iam:CreateRole",
                    "iam:AttachRolePolicy",
                    "iam:ListInstanceProfiles",
                    "iam:CreatePolicy",
                    "iam:PassRole",
                    "iam:ListPolicyVersions",
                    "iam:GetUserPolicy",
                    "iam:ListAttachedRolePolicies",
                    "iam:AttachGroupPolicy",
                    "iam:GetGroupPolicy",
                    "iam:ListRolePolicies",
                    "iam:GetRolePolicy"
                ],
                "Resource": "*"
            }
        ]
    }


How to Use MFA to access AWS CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

