.. _aws-ecr-push-and-pull-private-image:

AWS ECR Push and Pull Private Image
==============================================================================
Keywords: AWS ECR, Docker, Login, Auth, Authentication, Push, Pull, Private, Image


What's the Problem?
------------------------------------------------------------------------------
AWS ECR 是一个私有的 Container Registry, 你当然是要鉴权才能够 Pull 和 Pull Container Image 了. AWS 支持用 Docker CLI 客户端来做这件事.


Overview
------------------------------------------------------------------------------
执行下面的命令获得一个 token 用于登录某个 aws account, 某个 aws region 下的 ecr::

    aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>

上面的命令会返回一个 token 字符串, 然后你就可以让你的 client login ECR 了::

    docker login -u AWS -p <token-value> https://<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com.

其中 <token-value> 部分就是验证用的 token. 这个字符串就是登录命令, 可以直接拷贝到命令行中执行. 所以你甚至可以直接使用下面的命令执行它, 免去了复制粘贴的步骤::

    $(aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>)

根据 docker login 的文档 -p 命令是不安全的, 会将 token 暴漏在 cli 的命令历史记录中, 官方推荐使用 ``--password-stdin`` 选项传入 token. 所以最终的命令是这样的::

    AWS_REGION="us-east-1"
    AWS_PROFILE="my-aws-profile"
    ecr_uri="https://111122223333.dkr.ecr.${AWS_REGION}.amazonaws.com"

    aws ecr get-login --no-include-email --region ${AWS_REGION} --profile ${AWS_PROFILE} | awk '{printf $6}' | docker login -u AWS ${ecr_uri} --password-stdin

在这之后, ``docker pull`` 或是 ``docker push`` 就会有操作权限了.


Shell Script
------------------------------------------------------------------------------
这里我写了一个脚本, 可以非常方便地让 docker cli login 到 ECR. 脚本内容如下:

.. literalinclude:: ./ecr_login.py
   :language: python
   :linenos:
