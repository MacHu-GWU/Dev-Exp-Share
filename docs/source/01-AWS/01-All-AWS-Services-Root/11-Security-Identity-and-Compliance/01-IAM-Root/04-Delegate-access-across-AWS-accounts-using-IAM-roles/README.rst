Delegate access across AWS accounts using IAM roles
==============================================================================
Keywords: AWS, IAM Role, Cross Account Access, Assume Role.


Summary
------------------------------------------------------------------------------
位于 Account A (acc_A) 上的用户想要访问位于 acc_B 上的资源，但就为了这个需求而在 acc_B 上创建一个 IAM 用户, 这显然不是一个 secure 也不 scale 的做法. 为了解决这个问题, AWS 官方推荐使用 IAM Roles 来实现跨账号访问. 本文将介绍如何使用 IAM Roles 来实现跨账号访问.

Reference:

- IAM tutorial: Delegate access across AWS accounts using IAM roles: https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html


How it Works
------------------------------------------------------------------------------
首先我们定义我们的目标, 我们要实现 acc_A 上的用户访问 acc_B. 我们定义被访问的账号叫做 owner account, 而需要访问权限的账号叫做 grantee account.

简单来说实现这个的原理是:

- 在 owner account 上创建一个 IAM Role. trusted entity 里的要列出 grantee account 上需要访问权限的 principal. 这个 principal 可以是 Account Root, 也可以是特定的 IAM Group / User / Role, 也可以两种都用. 这两种方法各有优劣, 我们将在后面详细讨论.
- 在 grantee account 上给需要访问权限的 principal 必要的 IAM policy permission, 里面要允许它 assume 在前一步在 owner account 上创建的 IAM Role.
- 然后你在 grantee account 的 console 界面的右上角的 dropdown menu 里选择 Switch Role, 然后填写 owner account 的 account id 以及 role name 即可进入 owner account 的 console.
- 如果你要用 CLI 访问, 那么你先创建一个 boto session, 然后调用 `sts.assume_role <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html#>`_ API, 它会返回一些 token, 然后你再用这些 token 创建一个新的 boto session, 这个 session 就相当于是 owner account 上的 IAM Role 了.

下面是一些 IAM Policy 的例子:

Owner account 上的 IAM Role 的 trusted entity:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::${grantee_aws_account_id}:root",
                        "arn:aws:iam::${grantee_aws_account_id}:role/${iam_role_on_grantee_aws_account}",
                        "arn:aws:iam::${grantee_aws_account_id}:user/${iam_user_on_grantee_aws_account}",
                        "arn:aws:iam::${grantee_aws_account_id}:group/${iam_group_on_grantee_aws_account}"
                    ]
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    }

Grantee account 上的 Principal 所需要的 IAM Policy:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::${owner_account_id}:role/${iam_role_on_owner_aws_account}"
        }
    }

这里有个 best practice, 如果你的 Grantee account 上的 principal 配置了 ``sts:AssumeRole`` + ``*``. 那么会导致你可以 assume owner account 上的 role, 这相当于默认运行了. 这种 cross account 的行文肯定应该是默认不允许的, 所以在最佳实践上你应该给除了 Admin 之外的任何人都配置 explicit deny. 这个最好是通过 User Group 来实现. 下面这个是 explicit deny 的 IAM Policy:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Deny",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::${owner_account_id}:role/${iam_role_on_owner_aws_account}"
        }
    }


Best Practice
------------------------------------------------------------------------------
我开发了一个自动化脚本, 能够自动的为 1 个 grantee account 和多个 owner accounts 配好 cross account access. 这个 grantee account 上的 identity 可以是整个 Account, 或是一个给人用的 IAM User, 也可以是一个给机器用的 IAM Role. 而 owner accounts 上的 Role 的权限可以是各不相同的.

.. literalinclude:: ./cross_account_iam_role_access_manager.py
   :language: python
   :linenos:
