.. _aws-ecr-core-concepts:

AWS ECR Core Concepts
==============================================================================


Overview
------------------------------------------------------------------------------
Registry: 相当于一个私有的 ``hub.docker.com``. 这个的技术难度并不高, 难点在于带宽费用很贵, 你完全可以自己搭建一个 dockerhub. 对于 Container 领域, registry 和包管理领域的 repository 是同一级的概念. 类似于 ``hub.docker.com`` = ``pypi.org``. AWS 的每个 Account 的 Region 都有一个 ECR Registry, 其 Endpoint 是 ``https://${aws_account_id}.dkr.ecr.${aws_region}.amazonaws.com``.

    An Amazon ECR private registry is provided to each AWS account; you can create one or more repositories in your registry and store images in them. For more information, see Amazon ECR private registry.

Authorization token: 这里简单的说一下 client, Docker CLI 是最流行的 client, 但是符合容器标准的 client 实现很多, 其中 Redhat 的 Podman 也是一个很好的选择, 因为 Docker 集成了太多东西, 你如果不需要 runtime (运行时, 就是真正运行容器的那个环境, 其中 docker daemon 就是 docker 公司实现的运行时), 完全可以选择更轻量的 Podman. AWS 是通过 IAM 来管理权限的, 简单来说就是你先用 AWS CLI 获得一个 token 然后把这个 token 给 client 就能够实现跟 ECR 推拉 Image 了.

    Your client must authenticate to Amazon ECR registries as an AWS user before it can push and pull images. For more information, see Private registry authentication.

Repository: 一个具体的仓库, 里面可以放一个 Image 的很多个版本. 这类似与一个 Python 包的概念.

    An Amazon ECR repository contains your Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts. For more information, see Amazon ECR private repositories.

Repository policy: 每个 Repository 都是一个 AWS Resource. AWS 上的 Resource 大多都有 Resource Policy. 这个类似于 S3 Bucket Policy, 能对访问进行更精细的控制.

    You can control access to your repositories and the images within them with repository policies. For more information, see Private repository policies.

Image: 一个具体的容器景象了, 你可以给它打 tag, 也可以不打, 当然更推荐打. 这个类似于一个 Python 包的版本.

    You can push and pull container images to your repositories. You can use these images locally on your development system, or you can use them in Amazon ECS task definitions and Amazon EKS pod specifications. For more information, see Using Amazon ECR images with Amazon ECS and Using Amazon ECR Images with Amazon EKS.


Tag Management
------------------------------------------------------------------------------
Stable tag vs Unique tag

- `https://learn.microsoft.com/en-us/azure/container-registry/container-registry-image-tag-version <Recommendations for tagging and versioning container images>`_: 微软的官方文档中关于给容器镜像打 Tag 的最佳实践.
