AWS ECR
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


aws ecr get-login --region us-east-1 --no-include-email --profile eq_sanhe

docker tag sanhe/cicd:awscli-python3.6.8-packer-slim 110330507156.dkr.ecr.us-east-1.amazonaws.com/aws-ls-docker:awscli-python3.6.8-packer-slim

docker push 110330507156.dkr.ecr.us-east-1.amazonaws.com/aws-ls-docker:awscli-python3.6.8-packer-slim