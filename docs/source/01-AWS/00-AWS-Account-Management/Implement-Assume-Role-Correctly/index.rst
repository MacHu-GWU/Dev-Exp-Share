Implement Assume Role Correctly
==============================================================================

假设你需要用在 ``aws-account-a`` 上的 IAM User Assume ``aws-account-a`` 上的 IAM Role, 有两种方式可以控制这一权限.

1. 为 IAM User ``arn:aws:iam::aws-account-a:user/alice`` 添加 inline policy. 指定他可以 Assume 的 Role.

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": [
                    "arn:aws:iam::aws-account-b:role/my-assumed-role"
                ]
            }
        ]
    }

2. 为 IAM Role ``arn:aws:iam::aws-account-b:role/my-assumed-role`` 的 trusted entity 指定 Principal. 指定谁可以 Assume 这个 Role.

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::aws-account-a:user/alice"
                    ]
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    }

最好的实现方式是, 在完成 #1, #2 的情况下, 并且不给普通 IAM User 修改 IAM Permissions Management 的权限.

如果只做了 #1, 而在 #2 指定 ``arn:aws:iam::aws-account-a:root``. 那么任何在 ``aws-account-a`` 上拥有 ``sts:AssumeRole`` 的用户都可以 Assume 这个 Role. 这样是有潜在风险的.

而如果只做了 #2, 但如果 ``arn:aws:iam::aws-account-a:user/alice`` 被允许 Assume 了在 ``aws-account-b`` 上的其他 Role, 而如果这个 Role 恰巧有修改 IAM Role trusted entity 的权限, 那么 ``Alice`` 可以通过修改 trusted entity 的形式的给自己权限. 所以也是有潜在风险的.

所以要同时实现 #1, #2, 并且仅仅允许管理员 IAM User 通过修改其他 IAM User 的 inline policy 给予 Assume 指定的 IAM Role 的权限, 才可以保证完全安全.
