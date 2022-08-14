.. _aws-codebuild-trigger-build-job-with-boto3:

Trigger Build Job with boto3
==============================================================================
Keywords: AWS CodeBuild, Code Build, Python, Boto3

本篇文档介绍了如何用 boto3 启动一个 Build Job. 可以精准的指定 从哪个 Source pull 源代码 (CodeCommit, GitHub, GitLab, BitBucket), 用哪个 Branch 或是哪个 commit 来 build. 该操作常用于用 CodeCommit 的 event 来 trigger Lambda, 然后用 Lambda 来 trigger codebuild.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


With CodeCommit
------------------------------------------------------------------------------
下面是一个用 Python 启动一个 Build Job 的代码示例.

.. literalinclude:: ./start_build_with_codecommit.py
   :language: python

.. code-block:: python

    {
        'build': {
            'id': 'learn_codebuild_single:6abc5d92-075d-46f6-a9de-8ee871c18ee6',
            'arn': 'arn:aws:codebuild:us-east-2:669508176277:build/learn_codebuild_single:6abc5d92-075d-46f6-a9de-8ee871c18ee6',
            'buildNumber': 10,
            'startTime': datetime.datetime(2022, 5, 21, 14, 58, 34, 395000,
                                           tzinfo=tzlocal()),
            'currentPhase': 'QUEUED',
            'buildStatus': 'IN_PROGRESS',
            'sourceVersion': 'refs/heads/f3',
            'projectName': 'learn_codebuild_single',
            'phases': [
                {
                    'phaseType': 'SUBMITTED',
                    'phaseStatus': 'SUCCEEDED',
                    'startTime': datetime.datetime(2022, 5, 21, 14, 58, 34, 395000,
                                                   tzinfo=tzlocal()),
                    'endTime': datetime.datetime(2022, 5, 21, 14, 58, 34, 441000,
                                                 tzinfo=tzlocal()),
                    'durationInSeconds': 0
                },
                {
                    'phaseType': 'QUEUED',
                    'startTime': datetime.datetime(2022, 5, 21, 14, 58, 34, 441000,
                                                   tzinfo=tzlocal())
                }
            ],
            'source': {
                'type': 'CODECOMMIT',
                'location':
                    'https://git-codecommit.us-east-2.amazonaws.com/v1/repos/learn_codebuild',
                'gitCloneDepth': 1,
                'gitSubmodulesConfig': {'fetchSubmodules': False},
                'insecureSsl': False
            },
            'secondarySources': [],
            'secondarySourceVersions': [],
            'artifacts': {'location': ''},
            'secondaryArtifacts': [],
            'cache': {
                'type': 'S3',
                'location':
                    'aws-data-lab-sanhe-for-everything-us-east-2/codebuild/cache'
            },
            'environment': {
                'type': 'LINUX_CONTAINER',
                'image': 'aws/codebuild/amazonlinux2-x86_64-standard:3.0',
                'computeType': 'BUILD_GENERAL1_SMALL',
                'environmentVariables': [],
                'privilegedMode': False,
                'imagePullCredentialsType': 'CODEBUILD'
            },
            'serviceRole':
                'arn:aws:iam::669508176277:role/sanhe-codebuild-admin-access',
            'logs': {
                'deepLink': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-2#logEvent:group=null;stream=null',
                'cloudWatchLogsArn':
                    'arn:aws:logs:us-east-2:669508176277:log-group:null:log-stream:null',
                'cloudWatchLogs': {'status': 'ENABLED'},
                's3Logs': {'status': 'DISABLED', 'encryptionDisabled': False}
            },
            'timeoutInMinutes': 60,
            'queuedTimeoutInMinutes': 480,
            'buildComplete': False,
            'initiator': 'sanhe',
            'encryptionKey': 'arn:aws:kms:us-east-2:669508176277:alias/aws/s3'
        },
        'ResponseMetadata': {
            'RequestId': 'bf77acfd-f181-42c2-8901-5ad808e1639e',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': 'bf77acfd-f181-42c2-8901-5ad808e1639e',
                'content-type': 'application/x-amz-json-1.1',
                'content-length': '1716',
                'date': 'Sat, 21 May 2022 18:58:34 GMT'
            },
            'RetryAttempts': 0
        }
    }

