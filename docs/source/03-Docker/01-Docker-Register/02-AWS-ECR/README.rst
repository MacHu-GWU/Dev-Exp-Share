AWS ECR Docs
==============================================================================


使用 ECR 服务
------------------------------------------------------------------------------

只要你登录了 AWS ECR 服务, 那么之后的 push, pull 等命令都和 dockerhub 一致. 关于验证, 你需要先运行 ``aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>`` 获得一个 token, 然后使用 ``docker login -u AWS`` 命令手动输入密码后登录. 之所以不使用 ``-p`` 选项是因为命令行中输入的命令都有记录, 会有暴漏的风险. 对于希望使用自动化构建来将新构建好的镜像推送到 ECR 的情况, 请参考这篇文档: https://aws.amazon.com/blogs/devops/build-a-continuous-delivery-pipeline-for-your-container-images-with-amazon-ecr-as-source/

.. list-table:: Comparison
    :widths: 10 10 10
    :header-rows: 1

    * -
      - DockerHub
      - AWS ECR
    * - Login Command
      - .. code-block:: bash

            docker login
      - .. code-block:: bash

            aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>
            docker login -u AWS
    * - Repository
      - .. code-block:: bash

            <dockerhub-username>/<repo-name>
      - .. code-block:: bash

            <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<repo-name>
    * - Push Command
      - .. code-block:: bash

            docker push <dockerhub-username>/<repo-name>:<tag>
      - .. code-block:: bash

            docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<repo-name>:<tag>

参考资料:

- https://docs.aws.amazon.com/AmazonECR/latest/userguide/registries.html


AWS ECR 大坑之 如何使用 docker 登录 ecr
------------------------------------------------------------------------------

执行下面的命令获得一个 token 用于登录某个 aws account, 某个 aws region 下的 ecr::

    aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>

该命令会返回一个形如下面这样的字符串::

    docker login -u AWS -p <token-value> https://<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com.

其中 <token-value> 部分就是验证用的 token. 这个字符串就是登录命令, 可以直接拷贝到命令行中执行. 所以你甚至可以直接使用下面的命令执行它, 免去了复制粘贴的步骤::

    $(aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>)

根据 docker login 的文档 -p 命令是不安全的, 会将 token 暴漏在 cli 的命令历史记录中, 官方推荐使用 ``--password-stdin`` 选项传入 token. 所以最终的命令是这样的::

    AWS_REGION="us-east-1"
    AWS_PROFILE="my-aws-profile"
    ecr_uri="https://111122223333.dkr.ecr.${AWS_REGION}.amazonaws.com"
    aws ecr get-login --no-include-email --region ${AWS_REGION} --profile ${AWS_PROFILE} | awk '{printf $6}' | docker login -u AWS ${ecr_uri} --password-stdin

在这之后, ``docker pull`` 或是 ``docker push`` 就会有操作权限了.
