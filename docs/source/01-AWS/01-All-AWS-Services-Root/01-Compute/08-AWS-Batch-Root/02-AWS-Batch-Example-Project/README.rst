.. _aws-batch-example-project:

AWS Batch Example Project
==============================================================================
Keywords: AWS Batch Example Project


Summary
------------------------------------------------------------------------------
本文我在了解了 AWS Batch 的基本概念和功能后, 做的第一个实验性质的项目, 同时也为我今后做 AWS Batch Project 提供了参考.

在这个项目中我们创建了一个 Container App, 只要给定一个 Source S3 folder 和一个 Target S3 folder 作为参数, 就能将在 Source 下的所有文件拷贝到 Target 上.

首先我们来计划一下我们需要做什么:

1. 创建一个 ECR Repo, 然后把 App 的代码打包成容器.
2. 创建一个 Computer Environment
3. 创建一个 Job Queue
4. 创建一个 Job Definition, 其中指定使用我们的容器
5. 用创建的 Job Definition 提交一个 Job 到 Job Queue 中, 然后 Queue 会自动寻找可用的 Compute Environment 来运行这个 Job.

Reference:

- Components of AWS Batch: https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html#batch_components


Prepare Container Image
------------------------------------------------------------------------------
**App Code**

我们这个 App 非常简单. 它是用 Python 实现的, ``requirements.txt`` 定义了用到的依赖:

.. literalinclude:: ./requirements.txt

App 的源代码 ``main.py`` 文件:

.. literalinclude:: ./main.py
   :language: python
   :linenos:

``Dockerfile`` 的内容, 我们用的 base image 是 `Python <https://gallery.ecr.aws/docker/library/python>`_:

.. literalinclude:: Dockerfile

如果你想要在构建容器镜像之前本地运行一下 App, 你可以:

.. code-block:: bash

    # CD to where the main.py is
    # create a virtualenv at .venv folder
    virtualenv -p python3.9 .venv
    # activate virtualenv
    source .venv/bin/activate
    # install dependencies
    pip install -r requirements.txt
    # try to run the CLI
    python main.py --region ${aws_region} --s3uri_source s3://${aws_account_id}-${aws_region}-data/projects/lambda_project1/sbx/source/ --s3uri_target s3://${aws_account_id}-${aws_region}-data/projects/lambda_project1/sbx/final/

**Create ECR Repository**

- 进入 `AWS ECR Console <https://console.aws.amazon.com/ecr/repositories>`_
- 点击 Create Repository
- Visibility settings 选: Private
- Repository name 填: ``aws_batch_example``
- Tag immutability 选: disabled, 这样我们可以不断的覆盖特定的 Tag
- 其他选默认

**Build and Publish Container Image**





    ./cli -h

- CD 到 Dockerfile 所在的目录.
- 参考 ``./ecr_login`` 脚本的内容, 运行它用 Docker 对 AWS ECR 进行登录. 记得先用 ``chmod +x ecr_login`` 命令将其变为可执行文件. 脚本内容如下:

.. literalinclude:: ./ecr_login
   :language: python
   :linenos:

- 依次运行 ``./cli build-image``, ``./cli test-image``, ``./cli push-image``, 分别用来 构建, 测试, 发布. 记得先用 ``chmod +x cli`` 命令将其变为可执行文件. 脚本内容如下:

.. literalinclude:: ./cli
   :language: python
   :linenos:

现在我们的 Container 已经就绪了, 可以开始配置我们的 Batch Job 了.

Configuration
------------------------------------------------------------------------------


Computer Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们首先来配置计算环境.

- Step 1: Compute environment configuration
    - Compute environment configuration:
        - Platform: Fargate
        - Name: ``aws_batch_example``
        - Service role: use the default AWSServiceRoleForBatch
- Step 2: Instance configuration
    - Use Fargate Spot capacity: turn it on (to save cost)
    - Maximum vCPUs: 4 (make it small to save cost)
- Step 3: Network configuration
    - VPC and Subnet and Security Group: use your default VPC, public subnet, default security group


Job Queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
然后来配置 Job Queue

- Orchestration type: Fargate
- Name: ``aws_batch_example``
- Scheduling policy Amazon Resource Name (optional): leave it empty
- Connected compute environments: use the ``aws_batch_example`` you just created


Job Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
最后来配置 Job Definition

- Step 1: Job definition configuration
    - Orchestration type: Fargate
    - General configuration:
        - Name: ``aws_batch_example``
        - Execution timeout: 60 (seconds)
        - Scheduling priority: leave it empty, this is for advanced scheduling
    - Fargate platform configuration
        - Fargate platform version: LATEST (default)
        - (IMPORTANT) info=Infolabel=Assign public IP: turn it on.

            If it is on, then it allows your task to have outbound network access to the internet, so you can talk to ECR service endpoint to pull your image. If it is off, you have to ensure that you have a NatGateway on your VPC to route traffic to the internet (but it is expansive). If it is off and you don't have a NatGateway, then you cannot pull container image from ECR. You can also use ECR VPC Endpoint to create internal connection between your VPC and ECR service endpoint. See this discussion: https://repost.aws/knowledge-center/ecs-pull-container-api-error-ecr

        - Ephemeral storage:
        - Execution role:
        - Job attempts: 1
        - Retry strategy conditions: leave it empty
- Step 2: Container configuration
    - Image: ${aws_account_id}.dkr.ecr.${aws_region}.amazonaws.com/aws-batch-example:latest
    - Command syntax:
        - JSON: ``["--region","us-east-1","--s3uri_source","Ref::s3uri_source","--s3uri_target","Ref::s3uri_target"]``.
    - Parameters: add two parameter name ``s3uri_source`` and ``s3uri_target``.
    - Environment configuration:
        - Job role configuration:
        - vCPUs: 0.25
        - Memory: 0.5
- Step 3 (optional): Linux and logging settings
    - leave everything empty


Test by Submitting a Job
------------------------------------------------------------------------------
最后我们就可以来运行一个 Job 了.

- Step 1: Job configuration
    - Name: ``aws_batch_example``
    - Job definition: ``aws_batch_example:1``
    - Job queue: ``aws_batch_example``
- Step 2 (optional): Overrides
    - use default for Everything except:
    - Additional configuration -> Parameters: because we set two parameters in job definition, so we have to give them a value here.
        - s3uri_source: ``s3://${aws_account_id}-${aws_region}-data/projects/aws_batch_example/source/``
        - s3uri_target: ``s3://${aws_account_id}-${aws_region}-data/projects/aws_batch_example/target/``
