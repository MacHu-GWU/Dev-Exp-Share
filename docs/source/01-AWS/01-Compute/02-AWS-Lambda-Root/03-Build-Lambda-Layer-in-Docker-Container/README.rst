Build Lambda Layer in Docker Container
==============================================================================
Keywords: AWS, Lambda Function, Build, Layer, Docker, Container


Summary
------------------------------------------------------------------------------
由于 AWS Lambda 的运行环境是 Amazon Linux. 你在本地 Mac 电脑上或是 Redhat / Ubuntu CI 服务器上 build 的 Lambda Layer 可能是用不了的, 特别是一些用 C 实现的 Python 包. 所以一个比较稳定的方式是用和 Lambda Runtime 一致的 Docker Image 来 build layer 比较好.

这里我们选用的 `Docker Image <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html>`_ 是 AWS SAM 框架用来做 CI 的 image, 也是官方推荐适合用来 build layer 的 image. 而这个 Image 有 1.4 个 G, 会比较占用磁盘空间. 我不想浪费我 Mac 宝贵的磁盘, 所以我选用 AWS Cloud 9 来做宿主机来 build layer. Cloud 9 磁盘空间如果不够的化请参考这篇文档 `Resize an Amazon EBS volume used by an environment <https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize>`_ 来给 EBS 扩容. 请参考这篇文档 `Docker sample for AWS Cloud9 <https://docs.aws.amazon.com/cloud9/latest/user-guide/sample-docker.html>`_ 来在 Cloud 9 上安装 Docker.


Build Layer In Container Script
------------------------------------------------------------------------------
这里我们有一个脚本可以在 Mac / Linux 机器上构建 Lambda Layer:

.. literalinclude:: ./build_layer_in_container.py
   :language: python

构建完之后你就可以 upload 到 s3, 然后用 ``publish_layer_version`` API 来发布一个新的 Layer 了.


Reference
------------------------------------------------------------------------------
- 本文的知识主要来自于这篇官方文档, How do I create a Lambda layer using a simulated Lambda environment with Docker?: https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/
- AWS SAM's underlying ``amazon/aws-sam-cli-build-image`` Docker images, 这是 SAM 框架用来构建 Layer 的 Docker Image: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html
- Deploy Python Lambda functions with container images: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
- AWS ECR Gallery Lambda Python, 这是你 build 你自己的 Lambda Function docker container 时用的基础镜像, 当然也可以用来 build layer, 只不过复杂一点: https://gallery.ecr.aws/lambda/python
- Avoiding Permission Issues With Docker-Created Files: https://vsupalov.com/docker-shared-permissions/
- Can't Delete file created via Docker: https://stackoverflow.com/questions/42423999/cant-delete-file-created-via-docker